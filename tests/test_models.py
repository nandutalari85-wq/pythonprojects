import pytest
from sqlalchemy.exc import IntegrityError
from app.models import Crop, Region, CropRecord


def test_create_crop_and_region(app, init_db):
    """Test creating Crop and Region models."""
    with app.app_context():
        crop = Crop(name="Cotton", category="Commercial", default_unit="Metric Tonnes")
        region = Region(name="Gujarat", state="Gujarat", climate_zone="Semi-Arid")
        init_db.session.add(crop)
        init_db.session.add(region)
        init_db.session.commit()

        assert crop.id is not None
        assert crop.name == "Cotton"
        assert region.id is not None
        assert region.name == "Gujarat"


def test_crop_record_yield_property(app, init_db):
    """Test yield_per_hectare calculation and safety with zero area."""
    with app.app_context():
        # Valid calculation: 10000 / 2000 = 5.0
        rec = CropRecord(crop_id=1, region_id=1, year=2023,
                         area_cultivated=2000.0, area_unit="Hectares",
                         production_quantity=10000.0, production_unit="Metric Tonnes")
        assert rec.yield_per_hectare == 5.0

        # Safe handling with zero area
        rec_zero_area = CropRecord(crop_id=1, region_id=1, year=2024,
                                   area_cultivated=0.0, area_unit="Hectares",
                                   production_quantity=100.0, production_unit="Metric Tonnes")
        assert rec_zero_area.yield_per_hectare is None


def test_unique_constraint_crop_region_year(app, init_db):
    """Test that duplicate crop + region + year raises an IntegrityError."""
    with app.app_context():
        # Wheat (id=1) in Punjab (id=1) for 2021 already seeded in conftest
        duplicate = CropRecord(
            crop_id=1, region_id=1, year=2021,
            area_cultivated=2000.0, area_unit="Hectares",
            production_quantity=9000.0, production_unit="Metric Tonnes"
        )
        init_db.session.add(duplicate)
        with pytest.raises(IntegrityError):
            init_db.session.commit()
        init_db.session.rollback()


def test_cascade_delete(app, init_db):
    """Test that deleting a crop cascades and deletes all associated records."""
    with app.app_context():
        wheat = Crop.query.filter_by(name="Wheat").first()
        wheat_id = wheat.id
        init_db.session.delete(wheat)
        init_db.session.commit()

        # Records linked to wheat should be removed
        linked_records = CropRecord.query.filter_by(crop_id=wheat_id).all()
        assert len(linked_records) == 0


def test_model_to_dict_serialization(app, init_db):
    """Test that to_dict returns properly structured dictionary."""
    with app.app_context():
        rec = CropRecord.query.first()
        data = rec.to_dict()
        assert "id" in data
        assert "crop_name" in data
        assert "region_name" in data
        assert "yield_per_hectare" in data
        assert data["year"] in [2021, 2022]
