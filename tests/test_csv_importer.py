from app.csv_importer import CSVDatasetImporter
from app.models import Crop, Region, CropRecord


def test_valid_csv_parsing(app, init_db):
    """Test that a well-formatted CSV string is parsed into accepted rows."""
    valid_csv = """crop_name,crop_category,region_name,state,year,area_cultivated,area_unit,production_quantity,production_unit,annual_rainfall,notes
Barley,Cereal,Rajasthan,Rajasthan,2023,1500.0,Hectares,4500.0,Metric Tonnes,450.0,Valid row 1
Mustard,Oilseed,Rajasthan,Rajasthan,2023,1200.0,Hectares,2400.0,Metric Tonnes,420.0,Valid row 2
"""
    with app.app_context():
        importer = CSVDatasetImporter(valid_csv)
        is_valid, err, accepted, rejected = importer.validate_and_parse()

        assert is_valid is True
        assert err is None
        assert len(accepted) == 2
        assert len(rejected) == 0

        # Commit accepted rows
        count, commit_err = importer.commit_accepted_rows(accepted)
        assert commit_err is None
        assert count == 2

        # Verify added to DB
        barley = Crop.query.filter_by(name="Barley").first()
        assert barley is not None
        assert barley.category == "Cereal"


def test_missing_required_headers(app):
    """Test rejection when required columns are absent."""
    bad_csv = "crop_name,year,area_cultivated\nWheat,2021,100"
    with app.app_context():
        importer = CSVDatasetImporter(bad_csv)
        is_valid, err, accepted, rejected = importer.validate_and_parse()
        assert is_valid is False
        assert "Missing required CSV columns" in err


def test_empty_csv_file(app):
    """Test handling of completely empty file."""
    with app.app_context():
        importer = CSVDatasetImporter("")
        is_valid, err, accepted, rejected = importer.validate_and_parse()
        assert is_valid is False
        assert "empty" in err.lower()


def test_row_level_validation_errors(app, init_db):
    """Test detection of invalid rows (negative area, negative production, invalid year, empty fields)."""
    csv_content = """crop_name,region_name,year,area_cultivated,production_quantity,annual_rainfall
,Punjab,2023,1000,5000,600
Wheat,,2023,1000,5000,600
Wheat,Punjab,invalid_year,1000,5000,600
Wheat,Punjab,2023,-500,5000,600
Wheat,Punjab,2023,1000,-200,600
Wheat,Punjab,2023,1000,5000,-100
"""
    with app.app_context():
        importer = CSVDatasetImporter(csv_content)
        is_valid, err, accepted, rejected = importer.validate_and_parse()

        assert is_valid is True
        assert len(accepted) == 0
        assert len(rejected) == 6

        # Check specific rejection reasons
        assert any("Crop name is required" in e for e in rejected[0]["errors"])
        assert any("Region name is required" in e for e in rejected[1]["errors"])
        assert any("Invalid integer value for year" in e for e in rejected[2]["errors"])
        assert any("Cultivated area must be strictly positive" in e for e in rejected[3]["errors"])
        assert any("Production quantity cannot be negative" in e for e in rejected[4]["errors"])
        assert any("Rainfall cannot be negative" in e for e in rejected[5]["errors"])


def test_duplicate_row_detection(app, init_db):
    """Test duplicate detection both within the file and against existing database rows."""
    csv_content = """crop_name,region_name,year,area_cultivated,production_quantity
Wheat,Punjab,2021,2000,8000
Soybean,Madhya Pradesh,2023,1500,3000
Soybean,Madhya Pradesh,2023,1500,3000
"""
    with app.app_context():
        importer = CSVDatasetImporter(csv_content)
        is_valid, err, accepted, rejected = importer.validate_and_parse()

        assert is_valid is True
        # Row 1 (Wheat-Punjab-2021) already exists in DB from conftest
        # Row 3 (Soybean-MP-2023) is duplicate of Row 2 within same file
        assert len(accepted) == 1
        assert len(rejected) == 2

        db_dup = rejected[0]
        assert any("already exists in database" in e for e in db_dup["errors"])

        file_dup = rejected[1]
        assert any("Duplicate entry within this CSV" in e for e in file_dup["errors"])
