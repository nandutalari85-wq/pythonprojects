from flask import Blueprint, jsonify, request
from sqlalchemy import text
from app.models import db, Crop, Region, CropRecord
from app.analysis import CropAnalysisEngine

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint returning system, application, and database status.
    """
    db_status = "connected"
    try:
        # Ping database with a lightweight select
        db.session.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unreachable ({str(e)})"

    return jsonify({
        "status": "healthy" if db_status == "connected" else "degraded",
        "service": "Agricultural Crop Production Analysis System",
        "version": "1.0.0",
        "database": db_status,
    }), 200 if db_status == "connected" else 503


@api_bp.route("/crops", methods=["GET"])
def get_crops():
    """List all registered crops."""
    crops = Crop.query.order_by(Crop.name).all()
    return jsonify({
        "status": "success",
        "count": len(crops),
        "data": [crop.to_dict() for crop in crops]
    }), 200


@api_bp.route("/regions", methods=["GET"])
def get_regions():
    """List all registered regions."""
    regions = Region.query.order_by(Region.name).all()
    return jsonify({
        "status": "success",
        "count": len(regions),
        "data": [region.to_dict() for region in regions]
    }), 200


@api_bp.route("/records", methods=["GET"])
def get_records():
    """
    Retrieve crop production records with optional filters.
    Query parameters:
    - crop_id (int)
    - region_id (int)
    - year (int)
    """
    crop_id = request.args.get("crop_id", type=int)
    region_id = request.args.get("region_id", type=int)
    year = request.args.get("year", type=int)

    query = CropRecord.query.join(Crop).join(Region)

    if crop_id is not None:
        query = query.filter(CropRecord.crop_id == crop_id)
    if region_id is not None:
        query = query.filter(CropRecord.region_id == region_id)
    if year is not None:
        query = query.filter(CropRecord.year == year)

    records = query.order_by(CropRecord.year.desc(), Crop.name.asc()).all()

    return jsonify({
        "status": "success",
        "count": len(records),
        "filters": {
            "crop_id": crop_id,
            "region_id": region_id,
            "year": year
        },
        "data": [record.to_dict() for record in records]
    }), 200


@api_bp.route("/analysis/summary", methods=["GET"])
def get_analysis_summary():
    """
    Retrieve comprehensive statistical summaries computed via Pandas & NumPy.
    Supports optional crop_id, region_id, and year query parameters.
    """
    crop_id = request.args.get("crop_id", type=int)
    region_id = request.args.get("region_id", type=int)
    year = request.args.get("year", type=int)

    query = CropRecord.query

    if crop_id:
        query = query.filter(CropRecord.crop_id == crop_id)
    if region_id:
        query = query.filter(CropRecord.region_id == region_id)
    if year:
        query = query.filter(CropRecord.year == year)

    records = query.all()
    records_data = [r.to_dict() for r in records]

    engine = CropAnalysisEngine(records_data)

    return jsonify({
        "status": "success",
        "kpis": engine.get_kpis(),
        "crop_summary": engine.get_crop_summary(),
        "region_summary": engine.get_region_summary(),
        "rainfall_correlation": engine.get_rainfall_correlation(),
    }), 200


@api_bp.route("/analysis/trends", methods=["GET"])
def get_analysis_trends():
    """
    Retrieve annual production trends and Year-over-Year changes.
    Supports optional crop_id and region_id query parameters.
    """
    crop_id = request.args.get("crop_id", type=int)
    region_id = request.args.get("region_id", type=int)

    query = CropRecord.query

    if crop_id:
        query = query.filter(CropRecord.crop_id == crop_id)
    if region_id:
        query = query.filter(CropRecord.region_id == region_id)

    records = query.all()
    records_data = [r.to_dict() for r in records]

    engine = CropAnalysisEngine(records_data)
    trends = engine.get_annual_trends()

    return jsonify({
        "status": "success",
        "count": len(trends),
        "trends": trends
    }), 200
