import os
from pathlib import Path
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend safe for Flask & web servers
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class ChartGenerator:
    """
    Generates academic-quality Matplotlib charts for agricultural data.
    Saves outputs as PNGs with proper axis formatting, labels, and grids.
    """

    def __init__(self, output_dir=None):
        if output_dir is None:
            self.output_dir = Path(__file__).resolve().parent / "static" / "charts"
        else:
            self.output_dir = Path(output_dir)
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._set_style()

    def _set_style(self):
        """Configure clean, modern academic chart styling."""
        plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
        plt.rcParams.update({
            "font.family": "sans-serif",
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.titleweight": "bold",
            "axes.labelsize": 11,
            "axes.labelweight": "bold",
            "figure.titlesize": 14,
            "figure.dpi": 150,
        })

    def _draw_insufficient_data(self, title, message="Insufficient data to generate chart"):
        """Draw an informative banner when data is missing or insufficient."""
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.text(0.5, 0.5, f"{title}\n\n{message}", 
                ha="center", va="center", fontsize=11, color="#6c757d",
                bbox=dict(boxstyle="round,pad=0.8", facecolor="#f8f9fa", edgecolor="#ced4da"))
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_visible(False)
        plt.tight_layout()
        return fig

    def generate_annual_trend_chart(self, trends_list):
        """
        Chart 1: Annual Production Trend (Line Chart).
        """
        filename = "trend_chart.png"
        filepath = self.output_dir / filename

        if not trends_list or len(trends_list) < 2:
            fig = self._draw_insufficient_data("Annual Production Trend", "At least 2 years of data are required to plot trends.")
            fig.savefig(filepath, dpi=150, bbox_inches="tight")
            plt.close(fig)
            return filename, False

        years = [item["year"] for item in trends_list]
        productions = [item["total_production"] for item in trends_list]

        fig, ax = plt.subplots(figsize=(7, 4.2))
        ax.plot(years, productions, marker="o", linewidth=2.5, color="#198754", markersize=8, label="Production (Tonnes)")
        
        # Add data point labels
        for x, y in zip(years, productions):
            ax.annotate(f"{y:,.0f}", (x, y), textcoords="offset points", xytext=(0, 10), ha="center", fontsize=9, fontweight="bold", color="#157347")

        ax.set_title("Annual Crop Production Trend", pad=15)
        ax.set_xlabel("Year")
        ax.set_ylabel("Total Production (Metric Tonnes)")
        ax.set_xticks(years)
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.set_ylim(bottom=0, top=max(productions) * 1.18 if productions else 100)
        ax.legend(loc="upper left")

        plt.tight_layout()
        fig.savefig(filepath, dpi=150, bbox_inches="tight")
        plt.close(fig)
        return filename, True

    def generate_regional_comparison_chart(self, region_summary):
        """
        Chart 2: Regional Production Comparison (Bar Chart).
        """
        filename = "region_chart.png"
        filepath = self.output_dir / filename

        if not region_summary:
            fig = self._draw_insufficient_data("Regional Production Comparison", "No regional records available to display.")
            fig.savefig(filepath, dpi=150, bbox_inches="tight")
            plt.close(fig)
            return filename, False

        regions = [item["region_name"] for item in region_summary]
        productions = [item["total_production"] for item in region_summary]

        fig, ax = plt.subplots(figsize=(7, 4.2))
        colors = ["#0d6efd", "#20c997", "#fd7e14", "#6f42c1", "#ffc107"]
        bar_colors = [colors[i % len(colors)] for i in range(len(regions))]

        bars = ax.bar(regions, productions, color=bar_colors, width=0.55, edgecolor="#333333", linewidth=0.8)

        # Bar value annotations
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f"{height:,.0f}",
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 5), textcoords="offset points",
                        ha="center", va="bottom", fontsize=9, fontweight="bold")

        ax.set_title("Regional Crop Production Comparison", pad=15)
        ax.set_xlabel("Region")
        ax.set_ylabel("Total Production (Metric Tonnes)")
        ax.grid(axis="y", linestyle="--", alpha=0.6)
        ax.set_ylim(bottom=0, top=max(productions) * 1.15 if productions else 100)

        plt.tight_layout()
        fig.savefig(filepath, dpi=150, bbox_inches="tight")
        plt.close(fig)
        return filename, True

    def generate_crop_yield_chart(self, crop_summary):
        """
        Chart 3: Crop-wise Yield Comparison (Bar Chart: Tonnes / Hectare).
        """
        filename = "yield_chart.png"
        filepath = self.output_dir / filename

        if not crop_summary:
            fig = self._draw_insufficient_data("Crop-wise Yield Comparison", "No crop records available to calculate yield.")
            fig.savefig(filepath, dpi=150, bbox_inches="tight")
            plt.close(fig)
            return filename, False

        crops = [item["crop_name"] for item in crop_summary]
        yields = [item["avg_yield"] for item in crop_summary]

        fig, ax = plt.subplots(figsize=(7, 4.2))
        bars = ax.barh(crops, yields, color="#0dcaf0", edgecolor="#0aa2c0", height=0.55)

        for bar in bars:
            width = bar.get_width()
            ax.annotate(f"{width:.2f} T/Ha",
                        xy=(width, bar.get_y() + bar.get_height() / 2),
                        xytext=(8, 0), textcoords="offset points",
                        ha="left", va="center", fontsize=9, fontweight="bold", color="#055160")

        ax.set_title("Average Yield Comparison by Crop", pad=15)
        ax.set_xlabel("Average Productivity (Metric Tonnes / Hectare)")
        ax.set_ylabel("Crop")
        ax.grid(axis="x", linestyle="--", alpha=0.6)
        ax.set_xlim(left=0, right=max(yields) * 1.25 if yields else 5)

        plt.tight_layout()
        fig.savefig(filepath, dpi=150, bbox_inches="tight")
        plt.close(fig)
        return filename, True

    def generate_rainfall_scatter_chart(self, df):
        """
        Chart 4: Rainfall vs. Production Scatter Plot with regression trendline.
        Requires at least 3 paired records.
        """
        filename = "rainfall_chart.png"
        filepath = self.output_dir / filename

        if df.empty or "annual_rainfall" not in df.columns:
            fig = self._draw_insufficient_data("Rainfall vs. Production Analysis", "No rainfall records available.")
            fig.savefig(filepath, dpi=150, bbox_inches="tight")
            plt.close(fig)
            return filename, False

        valid_df = df.dropna(subset=["annual_rainfall", "production_quantity"])
        valid_df = valid_df[(valid_df["annual_rainfall"] >= 0) & (valid_df["production_quantity"] >= 0)]

        if len(valid_df) < 3:
            fig = self._draw_insufficient_data(
                "Rainfall vs. Production Analysis",
                f"Insufficient paired data ({len(valid_df)}/3 required).\nPlease add records with documented rainfall."
            )
            fig.savefig(filepath, dpi=150, bbox_inches="tight")
            plt.close(fig)
            return filename, False

        x = valid_df["annual_rainfall"].values
        y = valid_df["production_quantity"].values

        fig, ax = plt.subplots(figsize=(7, 4.2))
        ax.scatter(x, y, color="#e63946", alpha=0.8, edgecolors="#9b2226", s=60, label="Observed Records")

        # Trendline using NumPy linear polyfit
        if np.std(x) > 0:
            slope, intercept = np.polyfit(x, y, 1)
            x_line = np.linspace(x.min(), x.max(), 100)
            y_line = slope * x_line + intercept
            ax.plot(x_line, y_line, color="#1d3557", linestyle="--", linewidth=2, label="Trendline")

        ax.set_title("Rainfall vs. Crop Production (Observational)", pad=15)
        ax.set_xlabel("Annual Rainfall (mm)")
        ax.set_ylabel("Production (Metric Tonnes)")
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.legend(loc="best")

        plt.tight_layout()
        fig.savefig(filepath, dpi=150, bbox_inches="tight")
        plt.close(fig)
        return filename, True

    def generate_all_charts(self, engine):
        """
        Helper method to generate all charts from a CropAnalysisEngine instance.
        """
        trends = engine.get_annual_trends()
        regions = engine.get_region_summary()
        crops = engine.get_crop_summary()

        c1, c1_valid = self.generate_annual_trend_chart(trends)
        c2, c2_valid = self.generate_regional_comparison_chart(regions)
        c3, c3_valid = self.generate_crop_yield_chart(crops)
        c4, c4_valid = self.generate_rainfall_scatter_chart(engine.df)

        return {
            "trend_chart": {"file": c1, "is_valid": c1_valid},
            "region_chart": {"file": c2, "is_valid": c2_valid},
            "yield_chart": {"file": c3, "is_valid": c3_valid},
            "rainfall_chart": {"file": c4, "is_valid": c4_valid},
        }
