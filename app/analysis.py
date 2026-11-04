import numpy as np
import pandas as pd


class CropAnalysisEngine:
    """
    Agricultural Data Analysis Engine using Pandas and NumPy.
    Provides statistical summaries, yield computations, trend tracking,
    and environmental correlation analyses with strict unit safety.
    """

    def __init__(self, records_data):
        """
        Initialize engine with list of record dictionaries or QuerySet.
        Each dictionary should contain:
        [crop_name, region_name, year, area_cultivated, area_unit,
         production_quantity, production_unit, annual_rainfall]
        """
        if isinstance(records_data, pd.DataFrame):
            self.df = records_data.copy()
        elif records_data:
            self.df = pd.DataFrame(records_data)
        else:
            self.df = pd.DataFrame(columns=[
                "id", "crop_name", "crop_category", "region_name", "state",
                "year", "area_cultivated", "area_unit", "production_quantity",
                "production_unit", "annual_rainfall", "yield_per_hectare"
            ])

        # Prepare and clean data types if DataFrame is not empty
        self._prepare_dataframe()

    def _prepare_dataframe(self):
        """Standardize column types and compute derived metrics safely."""
        if self.df.empty:
            return

        # Numeric conversions
        self.df["year"] = pd.to_numeric(self.df["year"], errors="coerce")
        self.df["area_cultivated"] = pd.to_numeric(self.df["area_cultivated"], errors="coerce")
        self.df["production_quantity"] = pd.to_numeric(self.df["production_quantity"], errors="coerce")
        if "annual_rainfall" in self.df.columns:
            self.df["annual_rainfall"] = pd.to_numeric(self.df["annual_rainfall"], errors="coerce")
        else:
            self.df["annual_rainfall"] = np.nan

        # Unit compatibility & yield computation (Safe division: area > 0)
        # Yield = production / area (Metric Tonnes per Hectare)
        valid_area_mask = (self.df["area_cultivated"] > 0) & (self.df["production_quantity"] >= 0)
        self.df["yield_per_hectare"] = np.where(
            valid_area_mask,
            self.df["production_quantity"] / self.df["area_cultivated"],
            np.nan
        )

    def is_empty(self):
        return self.df.empty

    def get_kpis(self):
        """
        Compute top-level Key Performance Indicators (KPIs) for the dashboard.
        """
        if self.df.empty:
            return {
                "total_records": 0,
                "total_crops": 0,
                "total_regions": 0,
                "year_min": None,
                "year_max": None,
                "year_range_str": "N/A",
                "total_production": 0.0,
                "production_unit": "Metric Tonnes",
                "average_yield": 0.0,
                "has_incompatible_units": False,
            }

        # Check unit uniformity for production
        units = self.df["production_unit"].dropna().unique()
        has_incompatible_units = len(units) > 1
        primary_unit = units[0] if len(units) >= 1 else "Metric Tonnes"

        # Safe sum only if single unit or dominant unit
        if not has_incompatible_units:
            total_prod = float(self.df["production_quantity"].sum())
        else:
            # Sum only records matching primary unit to avoid invalid aggregation
            total_prod = float(self.df[self.df["production_unit"] == primary_unit]["production_quantity"].sum())

        valid_yields = self.df["yield_per_hectare"].dropna()
        avg_yield = float(valid_yields.mean()) if not valid_yields.empty else 0.0

        min_year = int(self.df["year"].min()) if pd.notna(self.df["year"].min()) else None
        max_year = int(self.df["year"].max()) if pd.notna(self.df["year"].max()) else None
        year_str = f"{min_year} - {max_year}" if min_year and max_year else "N/A"

        return {
            "total_records": int(len(self.df)),
            "total_crops": int(self.df["crop_name"].nunique()) if "crop_name" in self.df.columns else 0,
            "total_regions": int(self.df["region_name"].nunique()) if "region_name" in self.df.columns else 0,
            "year_min": min_year,
            "year_max": max_year,
            "year_range_str": year_str,
            "total_production": round(total_prod, 2),
            "production_unit": primary_unit,
            "average_yield": round(avg_yield, 2),
            "has_incompatible_units": has_incompatible_units,
        }

    def get_crop_summary(self):
        """
        Calculate summary statistics grouped by crop:
        Total, Mean, Min, Max, and Average Yield per crop.
        """
        if self.df.empty:
            return []

        grouped = self.df.groupby("crop_name")
        summary_list = []

        for crop_name, group in grouped:
            unit = group["production_unit"].iloc[0] if "production_unit" in group.columns else "Metric Tonnes"
            total_prod = float(group["production_quantity"].sum())
            avg_prod = float(group["production_quantity"].mean())
            min_prod = float(group["production_quantity"].min())
            max_prod = float(group["production_quantity"].max())
            
            valid_yields = group["yield_per_hectare"].dropna()
            avg_yield = float(valid_yields.mean()) if not valid_yields.empty else 0.0

            summary_list.append({
                "crop_name": str(crop_name),
                "record_count": int(len(group)),
                "total_production": round(total_prod, 2),
                "avg_production": round(avg_prod, 2),
                "min_production": round(min_prod, 2),
                "max_production": round(max_prod, 2),
                "avg_yield": round(avg_yield, 2),
                "production_unit": str(unit),
            })

        # Sort descending by total production
        summary_list.sort(key=lambda x: x["total_production"], reverse=True)
        return summary_list

    def get_region_summary(self):
        """
        Calculate summary statistics grouped by region:
        Total production, average area, average yield, and record count.
        """
        if self.df.empty:
            return []

        grouped = self.df.groupby("region_name")
        summary_list = []

        for region_name, group in grouped:
            unit = group["production_unit"].iloc[0] if "production_unit" in group.columns else "Metric Tonnes"
            total_prod = float(group["production_quantity"].sum())
            avg_prod = float(group["production_quantity"].mean())
            min_prod = float(group["production_quantity"].min())
            max_prod = float(group["production_quantity"].max())

            valid_yields = group["yield_per_hectare"].dropna()
            avg_yield = float(valid_yields.mean()) if not valid_yields.empty else 0.0

            summary_list.append({
                "region_name": str(region_name),
                "record_count": int(len(group)),
                "total_production": round(total_prod, 2),
                "avg_production": round(avg_prod, 2),
                "min_production": round(min_prod, 2),
                "max_production": round(max_prod, 2),
                "avg_yield": round(avg_yield, 2),
                "production_unit": str(unit),
            })

        summary_list.sort(key=lambda x: x["total_production"], reverse=True)
        return summary_list

    def get_annual_trends(self):
        """
        Calculate annual production trends with Year-over-Year (YoY)
        absolute and percentage changes.
        """
        if self.df.empty:
            return []

        # Group by year
        annual_df = self.df.groupby("year").agg(
            total_production=("production_quantity", "sum"),
            total_area=("area_cultivated", "sum"),
            avg_yield=("yield_per_hectare", "mean"),
            record_count=("id", "count")
        ).reset_index().sort_values("year")

        trends = []
        prev_production = None

        for _, row in annual_df.iterrows():
            current_prod = float(row["total_production"])
            year = int(row["year"])
            avg_yield = float(row["avg_yield"]) if pd.notna(row["avg_yield"]) else 0.0

            if prev_production is None:
                abs_change = 0.0
                pct_change = 0.0
            else:
                abs_change = current_prod - prev_production
                # Safe percentage calculation
                if prev_production > 0:
                    pct_change = (abs_change / prev_production) * 100.0
                else:
                    pct_change = 0.0

            trends.append({
                "year": year,
                "total_production": round(current_prod, 2),
                "avg_yield": round(avg_yield, 2),
                "record_count": int(row["record_count"]),
                "abs_change": round(abs_change, 2),
                "pct_change": round(pct_change, 2),
            })

            prev_production = current_prod

        return trends

    def get_rainfall_correlation(self):
        """
        Analyze statistical correlation between annual rainfall and production.
        Filters out missing rainfall values.
        Requires at least 3 paired observations.
        Includes academic disclaimer emphasizing correlation != causation.
        """
        disclaimer = (
            "Academic Note: Correlation measures statistical co-movement, not causal proof. "
            "Agricultural yields depend on an interconnected system including irrigation, "
            "fertilizer management, soil microbiology, pest attacks, and ambient temperature."
        )

        if self.df.empty or "annual_rainfall" not in self.df.columns:
            return {
                "has_sufficient_data": False,
                "sample_size": 0,
                "correlation_coefficient": None,
                "correlation_strength": "Insufficient data",
                "disclaimer": disclaimer,
            }

        # Filter complete pairs
        valid_pairs = self.df.dropna(subset=["annual_rainfall", "production_quantity"])
        # Further ensure positive rainfall and production
        valid_pairs = valid_pairs[(valid_pairs["annual_rainfall"] >= 0) & (valid_pairs["production_quantity"] >= 0)]

        sample_size = len(valid_pairs)
        if sample_size < 3:
            return {
                "has_sufficient_data": False,
                "sample_size": sample_size,
                "correlation_coefficient": None,
                "correlation_strength": "Insufficient data (minimum 3 records required)",
                "disclaimer": disclaimer,
            }

        # Calculate Pearson correlation coefficient using NumPy
        x = valid_pairs["annual_rainfall"].values
        y = valid_pairs["production_quantity"].values

        # If variance is zero in x or y, correlation is undefined
        if np.std(x) == 0 or np.std(y) == 0:
            corr_coef = 0.0
        else:
            corr_matrix = np.corrcoef(x, y)
            corr_coef = float(corr_matrix[0, 1])

        # Categorize correlation
        if np.isnan(corr_coef):
            corr_coef = 0.0

        abs_r = abs(corr_coef)
        if abs_r >= 0.7:
            strength = "Strong Positive" if corr_coef > 0 else "Strong Negative"
        elif abs_r >= 0.3:
            strength = "Moderate Positive" if corr_coef > 0 else "Moderate Negative"
        else:
            strength = "Weak or No Linear Correlation"

        return {
            "has_sufficient_data": True,
            "sample_size": sample_size,
            "correlation_coefficient": round(corr_coef, 4),
            "correlation_strength": strength,
            "disclaimer": disclaimer,
        }
