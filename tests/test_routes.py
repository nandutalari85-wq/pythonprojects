import io


def test_dashboard_route(client, init_db):
    """Test dashboard loads with HTTP 200 and displays title."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Crop Production Dashboard" in response.data
    assert b"Total Records" in response.data


def test_records_list_route(client, init_db):
    """Test records listing page."""
    response = client.get("/records")
    assert response.status_code == 200
    assert b"Crop Production Records" in response.data
    assert b"Wheat" in response.data


def test_add_record_valid(client, init_db):
    """Test adding a new crop record successfully."""
    form_payload = {
        "crop_id": 1,
        "region_id": 1,
        "year": 2023,
        "area_cultivated": 3200.0,
        "area_unit": "Hectares",
        "production_quantity": 16500.0,
        "production_unit": "Metric Tonnes",
        "annual_rainfall": 640.0,
        "notes": "Route test insertion"
    }
    response = client.post("/records/add", data=form_payload, follow_redirects=True)
    assert response.status_code == 200
    assert b"Crop record added successfully!" in response.data


def test_add_record_duplicate_validation(client, init_db):
    """Test adding duplicate record returns validation error."""
    # Wheat in Punjab for 2021 already seeded in conftest
    form_payload = {
        "crop_id": 1,
        "region_id": 1,
        "year": 2021,
        "area_cultivated": 3000.0,
        "production_quantity": 15000.0,
    }
    response = client.post("/records/add", data=form_payload)
    assert response.status_code == 200
    assert b"A record already exists for this crop, region, and year" in response.data


def test_record_detail_and_edit(client, init_db):
    """Test viewing and editing single record."""
    detail_res = client.get("/records/1")
    assert detail_res.status_code == 200
    assert b"Observation Record #1" in detail_res.data

    edit_res = client.post("/records/1/edit", data={
        "crop_id": 1, "region_id": 1, "year": 2021,
        "area_cultivated": 3050.0, "area_unit": "Hectares",
        "production_quantity": 15200.0, "production_unit": "Metric Tonnes",
        "annual_rainfall": 605.0, "notes": "Updated note"
    }, follow_redirects=True)
    assert edit_res.status_code == 200
    assert b"Crop record updated successfully!" in edit_res.data


def test_record_delete(client, init_db):
    """Test deleting a record."""
    del_res = client.post("/records/1/delete", follow_redirects=True)
    assert del_res.status_code == 200
    assert b"deleted" in del_res.data


def test_crops_management_routes(client, init_db):
    """Test crops list and adding a new crop."""
    get_res = client.get("/crops")
    assert get_res.status_code == 200
    assert b"Crops Catalog" in get_res.data

    post_res = client.post("/crops", data={
        "name": "Chickpea", "category": "Pulse", "default_unit": "Metric Tonnes"
    }, follow_redirects=True)
    assert post_res.status_code == 200
    assert b"Chickpea" in post_res.data


def test_regions_management_routes(client, init_db):
    """Test regions list and adding a new region."""
    get_res = client.get("/regions")
    assert get_res.status_code == 200
    assert b"Regions" in get_res.data

    post_res = client.post("/regions", data={
        "name": "Gujarat", "state": "Gujarat", "climate_zone": "Tropical Semi-Arid"
    }, follow_redirects=True)
    assert post_res.status_code == 200
    assert b"Gujarat" in post_res.data


def test_download_template(client):
    """Test downloading the CSV template."""
    response = client.get("/download-template")
    assert response.status_code == 200
    assert response.mimetype == "text/csv"
    assert b"crop_name" in response.data


def test_upload_csv_flow(client, init_db):
    """Test uploading a CSV dataset and previewing results."""
    csv_bytes = b"""crop_name,region_name,year,area_cultivated,production_quantity
Barley,Punjab,2023,1200,4800
"""
    data = {"file": (io.BytesIO(csv_bytes), "test_crops.csv")}
    response = client.post("/upload", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    assert b"Dataset Ingestion Validation Report" in response.data
    assert b"1 Valid Rows Ready to Import" in response.data

    # Confirm import
    confirm_res = client.post("/upload/confirm", follow_redirects=True)
    assert confirm_res.status_code == 200
    assert b"Successfully imported" in confirm_res.data


def test_404_not_found(client):
    """Test custom 404 page for non-existent routes."""
    response = client.get("/non-existent-page-url")
    assert response.status_code == 404
    assert b"Resource or Page Not Found" in response.data
