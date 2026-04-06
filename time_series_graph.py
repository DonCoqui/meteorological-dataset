"""
time_series_graph.py
====================
Create an interactive time-series graph from meteorological_data.json.

Default behaviour: plot ``climo_high_f`` (daily climatological high
temperature, °F) for the full data range (1941-06-17 → 2026-01-01).

Usage examples
--------------
python time_series_graph.py
python time_series_graph.py --metrics climo_high_f avg_feel max_dewpoint_f
python time_series_graph.py --metrics precip_in --output precip_graph.png
python time_series_graph.py --start-date 2000-01-01 --end-date 2026-01-01
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import List, Optional

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_DATA_FILE = os.path.join(os.path.dirname(__file__), "output", "meteorological_data.json")
FALLBACK_DATA_FILE = os.path.join(os.path.dirname(__file__), "meteorological_data.json")

DEFAULT_START_DATE = "1941-06-17"
DEFAULT_END_DATE = "2026-01-01"

AVAILABLE_METRICS: dict[str, str] = {
    "climo_high_f": "Climatological High Temperature (°F)",
    "avg_feel": "Average \"Feels Like\" Temperature (°F)",
    "max_dewpoint_f": "Maximum Dew Point (°F)",
    "precip_in": "Precipitation (in)",
    "avg_rh": "Average Relative Humidity (%)",
    "srad_mj": "Solar Radiation (MJ/m²)",
    "climo_precip_in": "Climatological Precipitation (in)",
}

DEFAULT_METRIC = "climo_high_f"

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def _locate_data_file(path: Optional[str]) -> Path:
    """Return the path to the data file, searching fallback locations."""
    if path:
        p = Path(path)
        if not p.exists():
            logger.error("Specified data file not found: %s", p)
            sys.exit(1)
        return p

    for candidate in (DEFAULT_DATA_FILE, FALLBACK_DATA_FILE):
        p = Path(candidate)
        if p.exists():
            return p

    logger.error(
        "Could not find meteorological_data.json. "
        "Expected at '%s' or '%s'. "
        "Run the data processor first, or pass --data <path>.",
        DEFAULT_DATA_FILE,
        FALLBACK_DATA_FILE,
    )
    sys.exit(1)


def load_data(data_path: Optional[str] = None) -> pd.DataFrame:
    """Load meteorological data from the JSON file into a DataFrame."""
    file_path = _locate_data_file(data_path)
    logger.info("Loading data from %s", file_path)

    try:
        with open(file_path, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
    except json.JSONDecodeError as exc:
        logger.error("Failed to parse JSON file: %s", exc)
        sys.exit(1)

    df = pd.DataFrame(raw)

    if "day" not in df.columns:
        logger.error("Expected a 'day' column in the data file but it was not found.")
        sys.exit(1)

    df["day"] = pd.to_datetime(df["day"], errors="coerce")
    invalid = df["day"].isna().sum()
    if invalid:
        logger.warning("%d row(s) with unparseable dates dropped.", invalid)
    df = df.dropna(subset=["day"])
    df = df.sort_values("day").reset_index(drop=True)

    logger.info(
        "Loaded %d records spanning %s → %s.",
        len(df),
        df["day"].min().date(),
        df["day"].max().date(),
    )
    return df


# ---------------------------------------------------------------------------
# Filtering
# ---------------------------------------------------------------------------

def filter_by_date(
    df: pd.DataFrame,
    start_date: Optional[str],
    end_date: Optional[str],
) -> pd.DataFrame:
    """Restrict the DataFrame to the requested date window."""
    start = pd.to_datetime(start_date or DEFAULT_START_DATE, errors="coerce")
    end = pd.to_datetime(end_date or DEFAULT_END_DATE, errors="coerce")

    if pd.isna(start):
        logger.error("Invalid --start-date value: %s", start_date)
        sys.exit(1)
    if pd.isna(end):
        logger.error("Invalid --end-date value: %s", end_date)
        sys.exit(1)
    if start > end:
        logger.error("--start-date (%s) must be before --end-date (%s).", start.date(), end.date())
        sys.exit(1)

    mask = (df["day"] >= start) & (df["day"] <= end)
    filtered = df.loc[mask].copy()

    if filtered.empty:
        logger.error("No data found between %s and %s.", start.date(), end.date())
        sys.exit(1)

    logger.info(
        "Date range filtered to %s → %s (%d records).",
        start.date(),
        end.date(),
        len(filtered),
    )
    return filtered


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

# Colours used for successive metrics on the same axes
_COLORS = [
    "#1f77b4",  # blue
    "#d62728",  # red
    "#2ca02c",  # green
    "#ff7f0e",  # orange
    "#9467bd",  # purple
    "#8c564b",  # brown
    "#e377c2",  # pink
]


def _ylabel_for_metrics(metrics: List[str]) -> str:
    """Build a concise y-axis label from the selected metrics."""
    units = {
        "climo_high_f": "°F",
        "avg_feel": "°F",
        "max_dewpoint_f": "°F",
        "precip_in": "in",
        "avg_rh": "%",
        "srad_mj": "MJ/m²",
        "climo_precip_in": "in",
    }
    unique_units = list(dict.fromkeys(units[m] for m in metrics if m in units))
    if len(unique_units) == 1:
        return unique_units[0]
    return " / ".join(unique_units)


def build_figure(
    df: pd.DataFrame,
    metrics: List[str],
    start_date: Optional[str],
    end_date: Optional[str],
) -> plt.Figure:
    """Build and return a matplotlib Figure for the requested metrics."""
    fig, ax = plt.subplots(figsize=(16, 6))

    date_range_str = (
        f"{(start_date or DEFAULT_START_DATE)} – {(end_date or DEFAULT_END_DATE)}"
    )

    for idx, metric in enumerate(metrics):
        label = AVAILABLE_METRICS.get(metric, metric)
        color = _COLORS[idx % len(_COLORS)]

        series = df.set_index("day")[metric] if metric in df.columns else pd.Series(dtype=float)
        # Drop NaN but keep the index intact for a continuous line
        valid = series.dropna()

        if valid.empty:
            logger.warning("Metric '%s' has no valid data in the selected range — skipped.", metric)
            continue

        missing_pct = 100.0 * series.isna().sum() / max(len(series), 1)
        if missing_pct > 0:
            logger.info(
                "Metric '%s': %.1f%% of values are missing (plotted where available).",
                metric,
                missing_pct,
            )

        ax.plot(
            valid.index,
            valid.values,
            label=label,
            color=color,
            linewidth=0.8,
            alpha=0.85,
        )

    # ---- Axes formatting ------------------------------------------------
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel(_ylabel_for_metrics(metrics), fontsize=12)

    title_metrics = (
        AVAILABLE_METRICS.get(metrics[0], metrics[0])
        if len(metrics) == 1
        else ", ".join(AVAILABLE_METRICS.get(m, m) for m in metrics)
    )
    ax.set_title(f"{title_metrics}\n{date_range_str}", fontsize=13, fontweight="bold")

    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend(loc="best", fontsize=10)

    fig.autofmt_xdate(rotation=30, ha="right")
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def save_or_show(
    fig: plt.Figure,
    output: Optional[str],
) -> None:
    """Either save the figure to a file or open an interactive window."""
    if output:
        out_path = Path(output)
        suffix = out_path.suffix.lower()
        supported = {".png", ".svg", ".pdf", ".jpg", ".jpeg"}
        if suffix not in supported:
            logger.warning(
                "Unrecognised output extension '%s'. Saving as PNG.", suffix
            )
            out_path = out_path.with_suffix(".png")

        out_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_path, dpi=300, bbox_inches="tight")
        logger.info("Graph saved → %s", out_path.resolve())
        print(f"Graph saved to: {out_path.resolve()}")
    else:
        plt.show()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="time_series_graph.py",
        description="Interactive time-series graph for meteorological data.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
available metrics:
  climo_high_f     Climatological High Temperature (°F)  [DEFAULT]
  avg_feel         Average "Feels Like" Temperature (°F)
  max_dewpoint_f   Maximum Dew Point (°F)
  precip_in        Precipitation (in)
  avg_rh           Average Relative Humidity (%)
  srad_mj          Solar Radiation (MJ/m²)
  climo_precip_in  Climatological Precipitation (in)

examples:
  python time_series_graph.py
  python time_series_graph.py --metrics climo_high_f avg_feel max_dewpoint_f
  python time_series_graph.py --metrics precip_in --output precip_graph.png
  python time_series_graph.py --start-date 2000-01-01 --end-date 2026-01-01
  python time_series_graph.py --metrics avg_rh --output humidity.svg
        """,
    )
    parser.add_argument(
        "--metrics",
        nargs="+",
        default=[DEFAULT_METRIC],
        metavar="METRIC",
        help="One or more metrics to plot (default: climo_high_f).",
    )
    parser.add_argument(
        "--start-date",
        default=None,
        metavar="YYYY-MM-DD",
        help=f"Start date (default: {DEFAULT_START_DATE}).",
    )
    parser.add_argument(
        "--end-date",
        default=None,
        metavar="YYYY-MM-DD",
        help=f"End date (default: {DEFAULT_END_DATE}).",
    )
    parser.add_argument(
        "--output",
        default=None,
        metavar="FILE",
        help="Save the graph to FILE (.png or .svg). If omitted the graph is displayed interactively.",
    )
    parser.add_argument(
        "--data",
        default=None,
        metavar="PATH",
        help="Path to meteorological_data.json (auto-detected if omitted).",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)

    # Validate metrics
    unknown = [m for m in args.metrics if m not in AVAILABLE_METRICS]
    if unknown:
        logger.error(
            "Unknown metric(s): %s. Available: %s",
            ", ".join(unknown),
            ", ".join(AVAILABLE_METRICS),
        )
        sys.exit(1)

    df = load_data(args.data)
    df = filter_by_date(df, args.start_date, args.end_date)
    fig = build_figure(df, args.metrics, args.start_date, args.end_date)
    save_or_show(fig, args.output)


if __name__ == "__main__":
    main()
