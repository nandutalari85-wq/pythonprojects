import pytest
from app import create_app
from app.models import db, Crop, Region, CropRecord


@pytest.fixture(scope="session")
def app():
    """Create and configure a Flask application instance for testing."""
    app = create_app("testing")
    yield app


@pytest.fixture(scope="function")
def client(app):
    """A test client for sending HTTP requests to the application."""
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="function")
def init_db(app):
    """
    Set up an isolated in-memory database with test data for each test function.
    """
    with app.app_context():
        db.create_all()

        # Seed test crops
        wheat = Crop(name="Wheat", category="Cereal", default_unit="Metric Tonnes")
        rice = Crop(name="Rice", category="Cereal", default_unit="Metric Tonnes")
        maize = Crop(name="Maize", category="Cereal", default_unit="Metric Tonnes")
        db.session.add_all([wheat, rice, maize])

        # Seed test regions
        punjab = Region(name="Punjab", state="Punjab", climate_zone="Subtropical Humid")
        maharashtra = Region(name="Maharashtra", state="Maharashtra", climate_zone="Tropical Semi-Arid")
        db.session.add_all([punjab, maharashtra])
        db.session.commit()

        # Seed test crop records
        records = [
            CropRecord(crop_id=wheat.id, region_id=punjab.id, year=2021,
                       area_cultivated=3000.0, area_unit="Hectares",
                       production_quantity=15000.0, production_unit="Metric Tonnes",
                       annual_rainfall=600.0, notes="Test record 1"),
            CropRecord(crop_id=wheat.id, region_id=punjab.id, year=2022,
                       area_cultivated=3100.0, area_unit="Hectares",
                       production_quantity=15810.0, production_unit="Metric Tonnes",
                       annual_rainfall=620.0, notes="Test record 2"),
            CropRecord(crop_id=rice.id, region_id=maharashtra.id, year=2021,
                       area_cultivated=2500.0, area_unit="Hectares",
                       production_quantity=7500.0, production_unit="Metric Tonnes",
                       annual_rainfall=1200.0, notes="Test record 3"),
            CropRecord(crop_id=rice.id, region_id=maharashtra.id, year=2022,
                       area_cultivated=2600.0, area_unit="Hectares",
                       production_quantity=8060.0, production_unit="Metric Tonnes",
                       annual_rainfall=1250.0, notes="Test record 4"),
        ]
        db.session.add_all(records)
        db.session.commit()

        yield db

        db.session.remove()
        db.drop_all()
