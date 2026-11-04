import os
from pathlib import Path
from app.charts import ChartGenerator
from app.analysis import CropAnalysisEngine


def test_chart_generation(tmp_path):
    """Test generating all 4 Matplotlib charts and saving to directory."""
    records = [
        {"id": 1, "crop_name": "Wheat", "region_name": "Punjab", "year": 2021,
         "area_cultivated": 3000.0, "area_unit": "Hectares",
         "production_quantity": 15000.0, "production_unit": "Metric Tonnes",
         "annual_rainfall": 600.0},
        {"id": 2, "crop_name": "Wheat", "region_name": "Punjab", "year": 2022,
         "area_cultivated": 3100.0, "area_unit": "Hectares",
         "production_quantity": 16000.0, "production_unit": "Metric Tonnes",
         "annual_rainfall": 620.0},
        {"id": 3, "crop_name": "Rice", "region_name": "Maharashtra", "year": 2021,
         "area_cultivated": 2000.0, "area_unit": "Hectares",
         "production_quantity": 6000.0, "production_unit": "Metric Tonnes",
         "annual_rainfall": 1200.0},
    ]

    engine = CropAnalysisEngine(records)
    generator = ChartGenerator(output_dir=tmp_path)
    charts = generator.generate_all_charts(engine)

    assert "trend_chart" in charts
    assert "region_chart" in charts
    assert "yield_chart" in charts
    assert "rainfall_chart" in charts

    # Verify PNG files exist on disk
    assert (tmp_path / "trend_chart.png").exists()
    assert (tmp_path / "region_chart.png").exists()
    assert (tmp_path / "yield_chart.png").exists()
    assert (tmp_path / "rainfall_chart.png").exists()


def test_chart_generation_empty_data(tmp_path):
    """Test that empty data does not throw exceptions and creates fallback notice charts."""
    engine = CropAnalysisEngine([])
    generator = ChartGenerator(output_dir=tmp_path)
    charts = generator.generate_all_charts(engine)

    assert charts["trend_chart"]["is_valid"] is False
    assert (tmp_path / "trend_chart.png").exists()
