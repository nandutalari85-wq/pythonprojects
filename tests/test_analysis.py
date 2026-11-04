import pytest
from app.analysis import CropAnalysisEngine


@pytest.fixture
def sample_records():
    return [
        {
            "id": 1, "crop_name": "Wheat", "region_name": "Punjab", "year": 2021,
            "area_cultivated": 3000.0, "area_unit": "Hectares",
            "production_quantity": 15000.0, "production_unit": "Metric Tonnes",
            "annual_rainfall": 600.0
        },
        {
            "id": 2, "crop_name": "Wheat", "region_name": "Punjab", "year": 2022,
            "area_cultivated": 3100.0, "area_unit": "Hectares",
            "production_quantity": 16000.0, "production_unit": "Metric Tonnes",
            "annual_rainfall": 620.0
        },
        {
            "id": 3, "crop_name": "Rice", "region_name": "Maharashtra", "year": 2021,
            "area_cultivated": 2000.0, "area_unit": "Hectares",
            "production_quantity": 6000.0, "production_unit": "Metric Tonnes",
            "annual_rainfall": 1200.0
        },
        {
            "id": 4, "crop_name": "Rice", "region_name": "Maharashtra", "year": 2022,
            "area_cultivated": 2100.0, "area_unit": "Hectares",
            "production_quantity": 6500.0, "production_unit": "Metric Tonnes",
            "annual_rainfall": 1250.0
        },
    ]


def test_empty_analysis_engine():
    """Test analysis engine resilience when given empty records list."""
    engine = CropAnalysisEngine([])
    kpis = engine.get_kpis()
    assert kpis["total_records"] == 0
    assert kpis["total_production"] == 0.0
    assert kpis["average_yield"] == 0.0
    assert engine.get_crop_summary() == []
    assert engine.get_region_summary() == []
    assert engine.get_annual_trends() == []

    rain_corr = engine.get_rainfall_correlation()
    assert rain_corr["has_sufficient_data"] is False


def test_kpi_calculations(sample_records):
    """Test KPI aggregates on sample dataset."""
    engine = CropAnalysisEngine(sample_records)
    kpis = engine.get_kpis()

    assert kpis["total_records"] == 4
    assert kpis["total_crops"] == 2
    assert kpis["total_regions"] == 2
    assert kpis["year_min"] == 2021
    assert kpis["year_max"] == 2022
    assert kpis["year_range_str"] == "2021 - 2022"
    # Total production = 15000 + 16000 + 6000 + 6500 = 43500
    assert kpis["total_production"] == 43500.0
    assert kpis["production_unit"] == "Metric Tonnes"
    assert kpis["average_yield"] > 0


def test_crop_summary_statistics(sample_records):
    """Test grouped crop statistics (total, avg, min, max, yield)."""
    engine = CropAnalysisEngine(sample_records)
    summary = engine.get_crop_summary()

    assert len(summary) == 2
    wheat_summary = next(item for item in summary if item["crop_name"] == "Wheat")
    assert wheat_summary["record_count"] == 2
    assert wheat_summary["total_production"] == 31000.0
    assert wheat_summary["min_production"] == 15000.0
    assert wheat_summary["max_production"] == 16000.0
    assert wheat_summary["avg_production"] == 15500.0
    # Wheat yield: 15000/3000 = 5.0, 16000/3100 = 5.16 -> avg ~ 5.08
    assert round(wheat_summary["avg_yield"], 1) == 5.1


def test_annual_trends_and_yoy_changes(sample_records):
    """Test annual aggregation and YoY absolute and percentage change."""
    engine = CropAnalysisEngine(sample_records)
    trends = engine.get_annual_trends()

    assert len(trends) == 2
    # 2021: 15000 + 6000 = 21000
    t2021 = trends[0]
    assert t2021["year"] == 2021
    assert t2021["total_production"] == 21000.0
    assert t2021["abs_change"] == 0.0
    assert t2021["pct_change"] == 0.0

    # 2022: 16000 + 6500 = 22500
    t2022 = trends[1]
    assert t2022["year"] == 2022
    assert t2022["total_production"] == 22500.0
    assert t2022["abs_change"] == 1500.0  # 22500 - 21000
    # % change = (1500 / 21000) * 100 = 7.14%
    assert t2022["pct_change"] == 7.14


def test_rainfall_correlation_with_sufficient_data(sample_records):
    """Test Pearson correlation calculation when sample size >= 3."""
    engine = CropAnalysisEngine(sample_records)
    corr = engine.get_rainfall_correlation()

    assert corr["has_sufficient_data"] is True
    assert corr["sample_size"] == 4
    assert isinstance(corr["correlation_coefficient"], float)
    assert "Academic Note: Correlation" in corr["disclaimer"]


def test_rainfall_correlation_insufficient_data():
    """Test rainfall correlation returns insufficient data notice when < 3 records have rainfall."""
    sparse_records = [
        {"id": 1, "crop_name": "Wheat", "year": 2021, "area_cultivated": 100,
         "production_quantity": 500, "production_unit": "Metric Tonnes", "annual_rainfall": 500},
        {"id": 2, "crop_name": "Wheat", "year": 2022, "area_cultivated": 100,
         "production_quantity": 520, "production_unit": "Metric Tonnes", "annual_rainfall": None},
    ]
    engine = CropAnalysisEngine(sparse_records)
    corr = engine.get_rainfall_correlation()
    assert corr["has_sufficient_data"] is False
    assert corr["sample_size"] == 1
