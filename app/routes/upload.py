import csv
import io
import json
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    Response,
    session,
)
from app.csv_importer import CSVDatasetImporter

upload_bp = Blueprint("upload", __name__)


@upload_bp.route("/upload", methods=["GET", "POST"])
def upload_dataset():
    """
    Handle CSV upload, validate format, and display validation breakdown.
    """
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part in the request.", "danger")
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            flash("No file was selected for upload.", "warning")
            return redirect(request.url)

        if not file.filename.lower().endswith(".csv"):
            flash("Invalid file type. Please upload a .csv file.", "danger")
            return redirect(request.url)

        # Process and validate CSV
        importer = CSVDatasetImporter(file)
        is_valid_structure, error_msg, accepted_rows, rejected_rows = importer.validate_and_parse()

        if not is_valid_structure:
            flash(f"Upload failed: {error_msg}", "danger")
            return redirect(request.url)

        # Store validated rows in session for confirmation
        # Keep only required fields in session to stay within cookie size limits
        session["pending_accepted_rows"] = accepted_rows

        return render_template(
            "upload_result.html",
            filename=file.filename,
            total_rows=len(accepted_rows) + len(rejected_rows),
            accepted_rows=accepted_rows,
            rejected_rows=rejected_rows,
        )

    return render_template("upload.html")


@upload_bp.route("/upload/confirm", methods=["POST"])
def confirm_import():
    """
    Commit accepted rows from session into the database via atomic transaction.
    """
    accepted_rows = session.get("pending_accepted_rows", [])

    if not accepted_rows:
        flash("No pending rows to import or session expired.", "warning")
        return redirect(url_for("upload.upload_dataset"))

    importer = CSVDatasetImporter("")
    count, error = importer.commit_accepted_rows(accepted_rows)

    # Clear session data
    session.pop("pending_accepted_rows", None)

    if error:
        flash(f"Import error during transaction: {error}", "danger")
    else:
        flash(f"Successfully imported {count} crop records into the database!", "success")

    return redirect(url_for("main.records_list"))


@upload_bp.route("/download-template")
def download_template():
    """
    Generate and serve a standardized CSV template for users to populate.
    """
    headers = CSVDatasetImporter.get_template_headers()
    sample_rows = CSVDatasetImporter.get_template_sample_rows()

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=headers)
    writer.writeheader()
    for row in sample_rows:
        writer.writerow(row)

    csv_data = output.getvalue()
    output.close()

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=crop_production_template.csv"}
    )
