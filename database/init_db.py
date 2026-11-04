import os
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app
from app.models import db, Crop, Region, CropRecord
from app.csv_importer import CSVDatasetImporter

def initialize_database():
    """
    Initialize database schema and populate with synthetic agricultural dataset.
    Works for both MySQL and SQLite environments.
    """
    print("=" * 70)
    print("Agricultural Crop Production Analysis System - Database Initializer")
    print("=" * 70)

    app = create_app()

    with app.app_context():
        db_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
        print(f">> Target Database URI: {db_uri}")

        try:
            print(">> Dropping existing tables (clean reset)...")
            db.drop_all()

            print(">> Creating database tables according to schema...")
            db.create_all()
            print(">> Tables created: regions, crops, crop_records.")

            # Load synthetic dataset
            dataset_path = PROJECT_ROOT / "data" / "crop_production_synthetic.csv"
            if not dataset_path.exists():
                print(f">> ERROR: Synthetic dataset not found at {dataset_path}")
                return False

            print(f">> Ingesting synthetic records from: {dataset_path.name}...")
            with open(dataset_path, "r", encoding="utf-8") as f:
                content = f.read()

            importer = CSVDatasetImporter(content)
            is_valid, err, accepted, rejected = importer.validate_and_parse()

            if not is_valid:
                print(f">> CSV Validation Error: {err}")
                return False

            print(f">> Valid rows detected: {len(accepted)} | Rejected: {len(rejected)}")
            count, db_err = importer.commit_accepted_rows(accepted)

            if db_err:
                print(f">> Ingestion error: {db_err}")
                return False

            # Verify totals
            total_crops = Crop.query.count()
            total_regions = Region.query.count()
            total_records = CropRecord.query.count()

            print("\n" + "-" * 70)
            print(">> SUCCESS: Database populated successfully!")
            print(f">> - Crops Registered:    {total_crops}")
            print(f">> - Regions Registered:  {total_regions}")
            print(f">> - Observation Records: {total_records}")
            print("-" * 70)
            return True

        except Exception as e:
            print(f"\n>> FATAL INITIALIZATION ERROR: {str(e)}")
            print(">> If MySQL is unreachable, start MySQL Service or set USE_SQLITE=true in .env")
            return False

if __name__ == "__main__":
    success = initialize_database()
    sys.exit(0 if success else 1)
