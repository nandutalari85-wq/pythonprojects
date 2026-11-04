import json


def test_api_health(client, init_db):
    """Test /api/health endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
    assert "version" in data


def test_api_crops(client, init_db):
    """Test /api/crops endpoint."""
    response = client.get("/api/crops")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["count"] >= 3
    crop_names = [c["name"] for c in data["data"]]
    assert "Wheat" in crop_names


def test_api_regions(client, init_db):
    """Test /api/regions endpoint."""
    response = client.get("/api/regions")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["count"] >= 2
    region_names = [r["name"] for r in data["data"]]
    assert "Punjab" in region_names


def test_api_records_filtered(client, init_db):
    """Test /api/records endpoint with query filters."""
    # Filter by crop_id=1 (Wheat)
    response = client.get("/api/records?crop_id=1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["filters"]["crop_id"] == 1
    assert data["count"] == 2
    for item in data["data"]:
        assert item["crop_name"] == "Wheat"


def test_api_analysis_summary(client, init_db):
    """Test /api/analysis/summary endpoint."""
    response = client.get("/api/analysis/summary")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert "kpis" in data
    assert "crop_summary" in data
    assert "region_summary" in data
    assert "rainfall_correlation" in data
    assert data["kpis"]["total_records"] == 4


def test_api_analysis_trends(client, init_db):
    """Test /api/analysis/trends endpoint."""
    response = client.get("/api/analysis/trends")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert "trends" in data
    assert len(data["trends"]) == 2
