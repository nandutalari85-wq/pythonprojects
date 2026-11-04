from pathlib import Path
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_file,
    current_app,
    abort,
)
from app.models import db, Crop, Region, CropRecord
from app.forms import FormValidator
from app.analysis import CropAnalysisEngine
from app.charts import ChartGenerator

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def dashboard():
    """
    Main Dashboard View:
    - Filters: crop_id, region_id, year
    - KPIs: total records, crops, regions, year range, total production, average yield
    - Matplotlib visual charts with download links
    - Tabular summaries for crops, regions, and annual trends
    """
    selected_crop_id = request.args.get("crop_id", type=int)
    selected_region_id = request.args.get("region_id", type=int)
    selected_year = request.args.get("year", type=int)

    # Base query
    query = CropRecord.query

    if selected_crop_id:
        query = query.filter(CropRecord.crop_id == selected_crop_id)
    if selected_region_id:
        query = query.filter(CropRecord.region_id == selected_region_id)
    if selected_year:
        query = query.filter(CropRecord.year == selected_year)

    records = query.order_by(CropRecord.year.desc()).all()
    records_data = [r.to_dict() for r in records]

    # Run analysis engine
    engine = CropAnalysisEngine(records_data)
    kpis = engine.get_kpis()
    crop_summary = engine.get_crop_summary()
    region_summary = engine.get_region_summary()
    annual_trends = engine.get_annual_trends()
    rainfall_analysis = engine.get_rainfall_correlation()

    # Generate charts
    chart_gen = ChartGenerator(output_dir=current_app.config["CHARTS_DIR"])
    charts_info = chart_gen.generate_all_charts(engine)

    # Filter dropdown choices
    all_crops = Crop.query.order_by(Crop.name).all()
    all_regions = Region.query.order_by(Region.name).all()
    all_years = [
        y[0] for y in db.session.query(CropRecord.year).distinct().order_by(CropRecord.year.desc()).all()
    ]

    return render_template(
        "dashboard.html",
        kpis=kpis,
        crop_summary=crop_summary,
        region_summary=region_summary,
        annual_trends=annual_trends,
        rainfall_analysis=rainfall_analysis,
        charts_info=charts_info,
        crops=all_crops,
        regions=all_regions,
        years=all_years,
        selected_crop_id=selected_crop_id,
        selected_region_id=selected_region_id,
        selected_year=selected_year,
        recent_records=records[:10],
    )


# ====================================================================
# Crop Records Management (CRUD)
# ====================================================================

@main_bp.route("/records")
def records_list():
    """List crop records with filtering and pagination."""
    selected_crop_id = request.args.get("crop_id", type=int)
    selected_region_id = request.args.get("region_id", type=int)
    selected_year = request.args.get("year", type=int)
    page = request.args.get("page", 1, type=int)
    per_page = 15

    query = CropRecord.query.join(Crop).join(Region)

    if selected_crop_id:
        query = query.filter(CropRecord.crop_id == selected_crop_id)
    if selected_region_id:
        query = query.filter(CropRecord.region_id == selected_region_id)
    if selected_year:
        query = query.filter(CropRecord.year == selected_year)

    pagination = query.order_by(CropRecord.year.desc(), Crop.name.asc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    all_crops = Crop.query.order_by(Crop.name).all()
    all_regions = Region.query.order_by(Region.name).all()
    all_years = [
        y[0] for y in db.session.query(CropRecord.year).distinct().order_by(CropRecord.year.desc()).all()
    ]

    return render_template(
        "records/list.html",
        pagination=pagination,
        records=pagination.items,
        crops=all_crops,
        regions=all_regions,
        years=all_years,
        selected_crop_id=selected_crop_id,
        selected_region_id=selected_region_id,
        selected_year=selected_year,
    )


@main_bp.route("/records/add", methods=["GET", "POST"])
def record_add():
    """Create a new crop record with server validation."""
    all_crops = Crop.query.order_by(Crop.name).all()
    all_regions = Region.query.order_by(Region.name).all()

    if not all_crops or not all_regions:
        flash("Please add at least one crop and one region before adding production records.", "warning")

    if request.method == "POST":
        is_valid, errors, cleaned = FormValidator.validate_crop_record(request.form)
        if is_valid:
            record = CropRecord(
                crop_id=cleaned["crop_id"],
                region_id=cleaned["region_id"],
                year=cleaned["year"],
                area_cultivated=cleaned["area_cultivated"],
                area_unit=cleaned["area_unit"],
                production_quantity=cleaned["production_quantity"],
                production_unit=cleaned["production_unit"],
                annual_rainfall=cleaned["annual_rainfall"],
                notes=cleaned["notes"],
            )
            db.session.add(record)
            db.session.commit()
            flash("Crop record added successfully!", "success")
            return redirect(url_for("main.records_list"))
        else:
            return render_template(
                "records/form.html",
                crops=all_crops,
                regions=all_regions,
                record=None,
                errors=errors,
                form_data=request.form,
                action_title="Add Crop Record",
            )

    return render_template(
        "records/form.html",
        crops=all_crops,
        regions=all_regions,
        record=None,
        errors={},
        form_data={},
        action_title="Add Crop Record",
    )


@main_bp.route("/records/<int:record_id>")
def record_detail(record_id):
    """View details of a single record."""
    record = db.get_or_404(CropRecord, record_id)
    return render_template("records/detail.html", record=record)


@main_bp.route("/records/<int:record_id>/edit", methods=["GET", "POST"])
def record_edit(record_id):
    """Edit an existing crop record."""
    record = db.get_or_404(CropRecord, record_id)
    all_crops = Crop.query.order_by(Crop.name).all()
    all_regions = Region.query.order_by(Region.name).all()

    if request.method == "POST":
        is_valid, errors, cleaned = FormValidator.validate_crop_record(request.form, record_id=record.id)
        if is_valid:
            record.crop_id = cleaned["crop_id"]
            record.region_id = cleaned["region_id"]
            record.year = cleaned["year"]
            record.area_cultivated = cleaned["area_cultivated"]
            record.area_unit = cleaned["area_unit"]
            record.production_quantity = cleaned["production_quantity"]
            record.production_unit = cleaned["production_unit"]
            record.annual_rainfall = cleaned["annual_rainfall"]
            record.notes = cleaned["notes"]
            db.session.commit()
            flash("Crop record updated successfully!", "success")
            return redirect(url_for("main.records_list"))
        else:
            return render_template(
                "records/form.html",
                crops=all_crops,
                regions=all_regions,
                record=record,
                errors=errors,
                form_data=request.form,
                action_title="Edit Crop Record",
            )

    form_data = {
        "crop_id": record.crop_id,
        "region_id": record.region_id,
        "year": record.year,
        "area_cultivated": record.area_cultivated,
        "area_unit": record.area_unit,
        "production_quantity": record.production_quantity,
        "production_unit": record.production_unit,
        "annual_rainfall": record.annual_rainfall if record.annual_rainfall is not None else "",
        "notes": record.notes or "",
    }
    return render_template(
        "records/form.html",
        crops=all_crops,
        regions=all_regions,
        record=record,
        errors={},
        form_data=form_data,
        action_title="Edit Crop Record",
    )


@main_bp.route("/records/<int:record_id>/delete", methods=["POST"])
def record_delete(record_id):
    """Delete a crop record."""
    record = db.get_or_404(CropRecord, record_id)
    crop_name = record.crop.name
    year = record.year
    db.session.delete(record)
    db.session.commit()
    flash(f"Record for '{crop_name}' ({year}) was deleted.", "info")
    return redirect(url_for("main.records_list"))


# ====================================================================
# Crops Management (CRUD)
# ====================================================================

@main_bp.route("/crops", methods=["GET", "POST"])
def crops_list():
    """List all crops and provide creation form."""
    if request.method == "POST":
        is_valid, errors, cleaned = FormValidator.validate_crop(request.form)
        if is_valid:
            crop = Crop(
                name=cleaned["name"],
                category=cleaned["category"],
                default_unit=cleaned["default_unit"],
            )
            db.session.add(crop)
            db.session.commit()
            flash(f"Crop '{crop.name}' added successfully!", "success")
            return redirect(url_for("main.crops_list"))
        else:
            crops = Crop.query.order_by(Crop.name).all()
            return render_template("crops/list.html", crops=crops, errors=errors, form_data=request.form)

    crops = Crop.query.order_by(Crop.name).all()
    return render_template("crops/list.html", crops=crops, errors={}, form_data={})


@main_bp.route("/crops/<int:crop_id>/edit", methods=["POST"])
def crop_edit(crop_id):
    """Edit crop details."""
    crop = db.get_or_404(Crop, crop_id)
    is_valid, errors, cleaned = FormValidator.validate_crop(request.form, crop_id=crop.id)
    if is_valid:
        crop.name = cleaned["name"]
        crop.category = cleaned["category"]
        crop.default_unit = cleaned["default_unit"]
        db.session.commit()
        flash(f"Crop '{crop.name}' updated successfully!", "success")
    else:
        err_msg = next(iter(errors.values())) if errors else "Validation failed."
        flash(f"Error updating crop: {err_msg}", "danger")
    return redirect(url_for("main.crops_list"))


@main_bp.route("/crops/<int:crop_id>/delete", methods=["POST"])
def crop_delete(crop_id):
    """Delete a crop and cascade delete associated records."""
    crop = db.get_or_404(Crop, crop_id)
    name = crop.name
    db.session.delete(crop)
    db.session.commit()
    flash(f"Crop '{name}' and all associated records deleted.", "info")
    return redirect(url_for("main.crops_list"))


# ====================================================================
# Regions Management (CRUD)
# ====================================================================

@main_bp.route("/regions", methods=["GET", "POST"])
def regions_list():
    """List all regions and provide creation form."""
    if request.method == "POST":
        is_valid, errors, cleaned = FormValidator.validate_region(request.form)
        if is_valid:
            region = Region(
                name=cleaned["name"],
                state=cleaned["state"],
                climate_zone=cleaned["climate_zone"],
            )
            db.session.add(region)
            db.session.commit()
            flash(f"Region '{region.name}' added successfully!", "success")
            return redirect(url_for("main.regions_list"))
        else:
            regions = Region.query.order_by(Region.name).all()
            return render_template("regions/list.html", regions=regions, errors=errors, form_data=request.form)

    regions = Region.query.order_by(Region.name).all()
    return render_template("regions/list.html", regions=regions, errors={}, form_data={})


@main_bp.route("/regions/<int:region_id>/edit", methods=["POST"])
def region_edit(region_id):
    """Edit region details."""
    region = db.get_or_404(Region, region_id)
    is_valid, errors, cleaned = FormValidator.validate_region(request.form, region_id=region.id)
    if is_valid:
        region.name = cleaned["name"]
        region.state = cleaned["state"]
        region.climate_zone = cleaned["climate_zone"]
        db.session.commit()
        flash(f"Region '{region.name}' updated successfully!", "success")
    else:
        err_msg = next(iter(errors.values())) if errors else "Validation failed."
        flash(f"Error updating region: {err_msg}", "danger")
    return redirect(url_for("main.regions_list"))


@main_bp.route("/regions/<int:region_id>/delete", methods=["POST"])
def region_delete(region_id):
    """Delete a region and cascade delete associated records."""
    region = db.get_or_404(Region, region_id)
    name = region.name
    db.session.delete(region)
    db.session.commit()
    flash(f"Region '{name}' and all associated records deleted.", "info")
    return redirect(url_for("main.regions_list"))


# ====================================================================
# Chart Download Endpoint
# ====================================================================

@main_bp.route("/download-chart/<filename>")
def download_chart(filename):
    """Allow downloading high-resolution chart images."""
    allowed_files = {"trend_chart.png", "region_chart.png", "yield_chart.png", "rainfall_chart.png"}
    if filename not in allowed_files:
        abort(404)

    file_path = current_app.config["CHARTS_DIR"] / filename
    if not file_path.exists():
        abort(404)

    return send_file(
        file_path,
        as_attachment=True,
        download_name=f"crop_analysis_{filename}",
        mimetype="image/png"
    )
