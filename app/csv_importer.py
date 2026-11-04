import csv
import io
import re
from app.models import db, Crop, Region, CropRecord


class CSVDatasetImporter:
    """
    Validates, parses, and safely imports agricultural CSV datasets.
    Tracks accepted vs. rejected rows with detailed diagnostic error messages.
    Uses atomic database transactions to ensure consistency.
    """

    REQUIRED_COLUMNS = [
        "crop_name",
        "region_name",
        "year",
        "area_cultivated",
        "production_quantity",
    ]

    OPTIONAL_COLUMNS = [
        "area_unit",
        "production_unit",
        "annual_rainfall",
        "crop_category",
        "state",
        "notes",
    ]

    @staticmethod
    def get_template_headers():
        return [
            "crop_name",
            "crop_category",
            "region_name",
            "state",
            "year",
            "area_cultivated",
            "area_unit",
            "production_quantity",
            "production_unit",
            "annual_rainfall",
            "notes"
        ]

    @staticmethod
    def get_template_sample_rows():
        return [
            {
                "crop_name": "Wheat",
                "crop_category": "Cereal",
                "region_name": "Punjab",
                "state": "Punjab",
                "year": 2023,
                "area_cultivated": 3500.0,
                "area_unit": "Hectares",
                "production_quantity": 17500.0,
                "production_unit": "Metric Tonnes",
                "annual_rainfall": 620.5,
                "notes": "Optimal winter monsoon"
            },
            {
                "crop_name": "Rice",
                "crop_category": "Cereal",
                "region_name": "Maharashtra",
                "state": "Maharashtra",
                "year": 2023,
                "area_cultivated": 2800.0,
                "area_unit": "Hectares",
                "production_quantity": 9800.0,
                "production_unit": "Metric Tonnes",
                "annual_rainfall": 1150.0,
                "notes": "Good kharif harvest"
            }
        ]

    def __init__(self, file_storage_or_content):
        """
        Accepts either a Werkzeug FileStorage object or a raw string/bytes.
        """
        self.raw_content = ""
        self._load_content(file_storage_or_content)

    def _load_content(self, source):
        if hasattr(source, "read"):
            content_bytes = source.read()
            if isinstance(content_bytes, bytes):
                # Try UTF-8 decoding, fallback to latin-1
                try:
                    self.raw_content = content_bytes.decode("utf-8-sig")
                except UnicodeDecodeError:
                    self.raw_content = content_bytes.decode("latin-1", errors="replace")
            else:
                self.raw_content = str(content_bytes)
        elif isinstance(source, bytes):
            try:
                self.raw_content = source.decode("utf-8-sig")
            except UnicodeDecodeError:
                self.raw_content = source.decode("latin-1", errors="replace")
        else:
            self.raw_content = str(source)

    def validate_and_parse(self):
        """
        Parse CSV and validate each row.
        Returns a tuple: (is_valid_structure, error_message, accepted_rows, rejected_rows)
        """
        if not self.raw_content or not self.raw_content.strip():
            return False, "The uploaded file is empty.", [], []

        # Filter out leading comment lines starting with '#' or empty lines before header
        lines = self.raw_content.splitlines()
        content_lines = [line for line in lines if line.strip() and not line.strip().startswith("#")]
        if not content_lines:
            return False, "The uploaded file contains no data rows or headers.", [], []

        cleaned_csv_content = "\n".join(content_lines)

        # Read CSV rows using standard csv reader
        try:
            stream = io.StringIO(cleaned_csv_content, newline=None)
            reader = csv.DictReader(stream)
        except Exception as e:
            return False, f"Malformed CSV file: {str(e)}", [], []

        if not reader.fieldnames:
            return False, "CSV contains no header row.", [], []

        # Normalize column header names (strip spaces, lowercase, remove quotes)
        normalized_fieldnames = {col: col.strip().lower() for col in reader.fieldnames if col}
        reader.fieldnames = [normalized_fieldnames.get(col, col) for col in reader.fieldnames]

        # Check for required headers
        missing_columns = [col for col in self.REQUIRED_COLUMNS if col not in reader.fieldnames]
        if missing_columns:
            return False, f"Missing required CSV columns: {', '.join(missing_columns)}", [], []

        accepted_rows = []
        rejected_rows = []

        # Pre-load existing database records for duplicate detection: (crop_name.lower(), region_name.lower(), year)
        existing_db_records = set()
        for rec in CropRecord.query.join(Crop).join(Region).all():
            existing_db_records.add((rec.crop.name.strip().lower(), rec.region.name.strip().lower(), rec.year))

        seen_in_batch = set()

        for row_index, row in enumerate(reader, start=2):  # Start at line 2 (line 1 is header)
            row_errors = []
            
            # 1. Clean strings
            crop_name = (row.get("crop_name") or "").strip()
            crop_category = (row.get("crop_category") or "Cereal").strip()
            region_name = (row.get("region_name") or "").strip()
            state_name = (row.get("state") or region_name).strip()
            area_unit = (row.get("area_unit") or "Hectares").strip()
            production_unit = (row.get("production_unit") or "Metric Tonnes").strip()
            notes = (row.get("notes") or "").strip()

            if not crop_name:
                row_errors.append("Crop name is required and cannot be empty.")
            if not region_name:
                row_errors.append("Region name is required and cannot be empty.")

            # 2. Validate Year
            year_val = None
            raw_year = (row.get("year") or "").strip()
            if not raw_year:
                row_errors.append("Year is required.")
            else:
                try:
                    year_val = int(raw_year)
                    if year_val < 1900 or year_val > 2100:
                        row_errors.append(f"Year '{year_val}' out of valid range (1900-2100).")
                except ValueError:
                    row_errors.append(f"Invalid integer value for year: '{raw_year}'.")

            # 3. Validate Area Cultivated
            area_val = None
            raw_area = (row.get("area_cultivated") or "").strip()
            if not raw_area:
                row_errors.append("Cultivated area is required.")
            else:
                try:
                    area_val = float(raw_area)
                    if area_val <= 0:
                        row_errors.append(f"Cultivated area must be strictly positive (> 0), got '{area_val}'.")
                except ValueError:
                    row_errors.append(f"Invalid numeric value for cultivated area: '{raw_area}'.")

            # 4. Validate Production Quantity
            prod_val = None
            raw_prod = (row.get("production_quantity") or "").strip()
            if not raw_prod:
                row_errors.append("Production quantity is required.")
            else:
                try:
                    prod_val = float(raw_prod)
                    if prod_val < 0:
                        row_errors.append(f"Production quantity cannot be negative, got '{prod_val}'.")
                except ValueError:
                    row_errors.append(f"Invalid numeric value for production: '{raw_prod}'.")

            # 5. Validate Annual Rainfall (Optional)
            rainfall_val = None
            raw_rain = (row.get("annual_rainfall") or "").strip()
            if raw_rain:
                try:
                    rainfall_val = float(raw_rain)
                    if rainfall_val < 0:
                        row_errors.append(f"Rainfall cannot be negative, got '{rainfall_val}'.")
                except ValueError:
                    row_errors.append(f"Invalid numeric value for rainfall: '{raw_rain}'.")

            # 6. Check Duplicate within Batch and in Database
            if crop_name and region_name and year_val:
                key = (crop_name.lower(), region_name.lower(), year_val)
                if key in seen_in_batch:
                    row_errors.append(f"Duplicate entry within this CSV file for {crop_name} in {region_name} ({year_val}).")
                elif key in existing_db_records:
                    row_errors.append(f"Record for {crop_name} in {region_name} ({year_val}) already exists in database.")
                else:
                    seen_in_batch.add(key)

            # Record outcome
            row_summary = {
                "row_number": row_index,
                "crop_name": crop_name,
                "crop_category": crop_category,
                "region_name": region_name,
                "state": state_name,
                "year": year_val,
                "area_cultivated": area_val,
                "area_unit": area_unit,
                "production_quantity": prod_val,
                "production_unit": production_unit,
                "annual_rainfall": rainfall_val,
                "notes": notes,
                "errors": row_errors,
            }

            if row_errors:
                rejected_rows.append(row_summary)
            else:
                accepted_rows.append(row_summary)

        return True, None, accepted_rows, rejected_rows

    def commit_accepted_rows(self, accepted_rows):
        """
        Safely insert validated records into the database within an atomic transaction.
        Creates Region and Crop objects if they do not exist.
        Rolls back transaction on any database error.
        """
        if not accepted_rows:
            return 0, "No valid rows to commit."

        try:
            records_created = 0

            # Cache lookup dictionaries to minimize DB queries
            crops_cache = {c.name.lower(): c for c in Crop.query.all()}
            regions_cache = {r.name.lower(): r for r in Region.query.all()}

            for row in accepted_rows:
                c_name = row["crop_name"].strip()
                r_name = row["region_name"].strip()

                # Get or create Crop
                crop = crops_cache.get(c_name.lower())
                if not crop:
                    crop = Crop(
                        name=c_name,
                        category=row.get("crop_category") or "Cereal",
                        default_unit=row.get("production_unit") or "Metric Tonnes"
                    )
                    db.session.add(crop)
                    db.session.flush()  # Assigns crop.id
                    crops_cache[c_name.lower()] = crop

                # Get or create Region
                region = regions_cache.get(r_name.lower())
                if not region:
                    region = Region(
                        name=r_name,
                        state=row.get("state") or r_name,
                        climate_zone="Subtropical"
                    )
                    db.session.add(region)
                    db.session.flush()  # Assigns region.id
                    regions_cache[r_name.lower()] = region

                # Create CropRecord
                record = CropRecord(
                    crop_id=crop.id,
                    region_id=region.id,
                    year=row["year"],
                    area_cultivated=row["area_cultivated"],
                    area_unit=row["area_unit"],
                    production_quantity=row["production_quantity"],
                    production_unit=row["production_unit"],
                    annual_rainfall=row["annual_rainfall"],
                    notes=row.get("notes") or "Imported via CSV upload"
                )
                db.session.add(record)
                records_created += 1

            # Commit all operations atomically
            db.session.commit()
            return records_created, None

        except Exception as e:
            db.session.rollback()
            return 0, f"Database transaction failed: {str(e)}"
