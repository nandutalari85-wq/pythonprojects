from app.models import db, Crop, Region, CropRecord


class FormValidator:
    """
    Server-side form input validation for CRUD operations.
    Validates data integrity, ranges, and uniqueness constraints.
    """

    @staticmethod
    def validate_crop_record(form_data, record_id=None):
        """
        Validate data for adding or editing a CropRecord.
        """
        errors = {}

        # 1. Validate Crop ID
        crop_id = form_data.get("crop_id")
        if not crop_id:
            errors["crop_id"] = "Crop selection is required."
        else:
            try:
                crop = db.session.get(Crop, int(crop_id))
                if not crop:
                    errors["crop_id"] = "Selected crop does not exist."
            except (ValueError, TypeError):
                errors["crop_id"] = "Invalid crop identifier."

        # 2. Validate Region ID
        region_id = form_data.get("region_id")
        if not region_id:
            errors["region_id"] = "Region selection is required."
        else:
            try:
                region = db.session.get(Region, int(region_id))
                if not region:
                    errors["region_id"] = "Selected region does not exist."
            except (ValueError, TypeError):
                errors["region_id"] = "Invalid region identifier."

        # 3. Validate Year
        raw_year = form_data.get("year")
        year = None
        if not raw_year:
            errors["year"] = "Year is required."
        else:
            try:
                year = int(raw_year)
                if year < 1900 or year > 2100:
                    errors["year"] = "Year must be between 1900 and 2100."
            except (ValueError, TypeError):
                errors["year"] = "Year must be a valid integer."

        # 4. Validate Area Cultivated
        raw_area = form_data.get("area_cultivated")
        area = None
        if not raw_area:
            errors["area_cultivated"] = "Cultivated area is required."
        else:
            try:
                area = float(raw_area)
                if area <= 0:
                    errors["area_cultivated"] = "Cultivated area must be greater than zero."
            except (ValueError, TypeError):
                errors["area_cultivated"] = "Cultivated area must be a valid number."

        # 5. Validate Production Quantity
        raw_prod = form_data.get("production_quantity")
        prod = None
        if raw_prod is None or raw_prod == "":
            errors["production_quantity"] = "Production quantity is required."
        else:
            try:
                prod = float(raw_prod)
                if prod < 0:
                    errors["production_quantity"] = "Production cannot be negative."
            except (ValueError, TypeError):
                errors["production_quantity"] = "Production must be a valid number."

        # 6. Validate Annual Rainfall (Optional)
        raw_rain = form_data.get("annual_rainfall")
        rainfall = None
        if raw_rain is not None and str(raw_rain).strip() != "":
            try:
                rainfall = float(raw_rain)
                if rainfall < 0:
                    errors["annual_rainfall"] = "Rainfall cannot be negative."
            except (ValueError, TypeError):
                errors["annual_rainfall"] = "Rainfall must be a valid number if specified."

        # 7. Check Duplicate (Crop + Region + Year)
        if not errors and crop_id and region_id and year:
            query = CropRecord.query.filter_by(
                crop_id=int(crop_id),
                region_id=int(region_id),
                year=year
            )
            # If editing an existing record, exclude itself from uniqueness check
            if record_id:
                query = query.filter(CropRecord.id != int(record_id))
            
            existing = query.first()
            if existing:
                errors["general"] = f"A record already exists for this crop, region, and year ({year})."

        cleaned_data = {
            "crop_id": int(crop_id) if crop_id and "crop_id" not in errors else None,
            "region_id": int(region_id) if region_id and "region_id" not in errors else None,
            "year": year,
            "area_cultivated": area,
            "area_unit": (form_data.get("area_unit") or "Hectares").strip(),
            "production_quantity": prod,
            "production_unit": (form_data.get("production_unit") or "Metric Tonnes").strip(),
            "annual_rainfall": rainfall,
            "notes": (form_data.get("notes") or "").strip(),
        }

        return len(errors) == 0, errors, cleaned_data

    @staticmethod
    def validate_crop(form_data, crop_id=None):
        """Validate Crop creation or update."""
        errors = {}
        name = (form_data.get("name") or "").strip()
        category = (form_data.get("category") or "Cereal").strip()
        default_unit = (form_data.get("default_unit") or "Metric Tonnes").strip()

        if not name:
            errors["name"] = "Crop name is required."
        elif len(name) < 2 or len(name) > 100:
            errors["name"] = "Crop name must be between 2 and 100 characters."
        else:
            query = Crop.query.filter(Crop.name.ilike(name))
            if crop_id:
                query = query.filter(Crop.id != int(crop_id))
            if query.first():
                errors["name"] = f"A crop named '{name}' already exists."

        cleaned_data = {
            "name": name,
            "category": category,
            "default_unit": default_unit,
        }
        return len(errors) == 0, errors, cleaned_data

    @staticmethod
    def validate_region(form_data, region_id=None):
        """Validate Region creation or update."""
        errors = {}
        name = (form_data.get("name") or "").strip()
        state = (form_data.get("state") or "").strip()
        climate_zone = (form_data.get("climate_zone") or "Subtropical").strip()

        if not name:
            errors["name"] = "Region name is required."
        elif len(name) < 2 or len(name) > 100:
            errors["name"] = "Region name must be between 2 and 100 characters."
        else:
            query = Region.query.filter(Region.name.ilike(name))
            if region_id:
                query = query.filter(Region.id != int(region_id))
            if query.first():
                errors["name"] = f"A region named '{name}' already exists."

        if not state:
            errors["state"] = "State is required."

        cleaned_data = {
            "name": name,
            "state": state,
            "climate_zone": climate_zone,
        }
        return len(errors) == 0, errors, cleaned_data
