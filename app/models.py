from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

db = SQLAlchemy()


def utc_now():
    """Return timezone-aware current UTC time."""
    return datetime.now(timezone.utc)


class Region(db.Model):
    """
    Region Model: Stores geographical and climate information.
    """
    __tablename__ = "regions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    state = db.Column(db.String(100), nullable=False)
    climate_zone = db.Column(db.String(100), nullable=True, default="Subtropical")
    created_at = db.Column(db.DateTime, default=utc_now, nullable=False)

    # Relationship to crop records
    records = db.relationship(
        "CropRecord",
        backref="region",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        """Serialize region for JSON API responses."""
        return {
            "id": self.id,
            "name": self.name,
            "state": self.state,
            "climate_zone": self.climate_zone,
            "record_count": len(self.records),
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
        }

    def __repr__(self):
        return f"<Region id={self.id} name='{self.name}'>"


class Crop(db.Model):
    """
    Crop Model: Stores crop taxonomy and standard measurement units.
    """
    __tablename__ = "crops"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    category = db.Column(db.String(50), nullable=False, default="Cereal")
    default_unit = db.Column(db.String(50), nullable=False, default="Metric Tonnes")
    created_at = db.Column(db.DateTime, default=utc_now, nullable=False)

    # Relationship to crop records
    records = db.relationship(
        "CropRecord",
        backref="crop",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        """Serialize crop for JSON API responses."""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "default_unit": self.default_unit,
            "record_count": len(self.records),
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
        }

    def __repr__(self):
        return f"<Crop id={self.id} name='{self.name}'>"


class CropRecord(db.Model):
    """
    CropRecord Model: Stores annual agricultural production facts.
    Enforces a unique constraint across (crop_id, region_id, year).
    """
    __tablename__ = "crop_records"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    crop_id = db.Column(db.Integer, db.ForeignKey("crops.id", ondelete="CASCADE"), nullable=False, index=True)
    region_id = db.Column(db.Integer, db.ForeignKey("regions.id", ondelete="CASCADE"), nullable=False, index=True)
    year = db.Column(db.Integer, nullable=False, index=True)
    
    # Cultivated area
    area_cultivated = db.Column(db.Float, nullable=False)
    area_unit = db.Column(db.String(30), nullable=False, default="Hectares")

    # Production quantity
    production_quantity = db.Column(db.Float, nullable=False)
    production_unit = db.Column(db.String(30), nullable=False, default="Metric Tonnes")

    # Environmental indicator (nullable to model real-world missing data)
    annual_rainfall = db.Column(db.Float, nullable=True)

    # Additional notes / remarks
    notes = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now, nullable=False)

    # Unique constraint preventing duplicate crop + region + year entries
    __table_args__ = (
        UniqueConstraint("crop_id", "region_id", "year", name="uq_crop_region_year"),
    )

    @property
    def yield_per_hectare(self):
        """
        Calculate productivity (Yield = Production / Area).
        Returns None if area is zero or non-positive, or if units are non-standard.
        """
        if self.area_cultivated is not None and self.area_cultivated > 0:
            if self.production_quantity is not None and self.production_quantity >= 0:
                return round(float(self.production_quantity) / float(self.area_cultivated), 4)
        return None

    def to_dict(self):
        """Serialize record for JSON API responses."""
        return {
            "id": self.id,
            "crop_id": self.crop_id,
            "crop_name": self.crop.name if self.crop else None,
            "crop_category": self.crop.category if self.crop else None,
            "region_id": self.region_id,
            "region_name": self.region.name if self.region else None,
            "state": self.region.state if self.region else None,
            "year": self.year,
            "area_cultivated": float(self.area_cultivated),
            "area_unit": self.area_unit,
            "production_quantity": float(self.production_quantity),
            "production_unit": self.production_unit,
            "yield_per_hectare": self.yield_per_hectare,
            "annual_rainfall": float(self.annual_rainfall) if self.annual_rainfall is not None else None,
            "notes": self.notes,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
        }

    def __repr__(self):
        return f"<CropRecord id={self.id} crop_id={self.crop_id} region_id={self.region_id} year={self.year}>"
