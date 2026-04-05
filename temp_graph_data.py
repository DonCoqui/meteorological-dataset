"""
temp_graph_data.py
==================
Generate a JSON file containing meteorological measurements indexed by station
and date.

This script reads the ``daily.xlsx`` Excel file located in the same directory
and creates ``temp_graph_data.json`` with a hierarchical structure:

.. code-block:: json

    {
      "STATION_ID": {
        "YYYY-MM-DD": {
          "max_dewpoint_f": <float|null>,
          "precip_in":      <float|null>,
          "avg_rh":         <float|null>,
          "avg_feel":       <float|null>,
          "srad_mj":        <float|null>,
          "climo_high_f":   <float|null>,
          "climo_precip_in":<float|null>
        },
        ...
      },
      ...
    }

Missing values (``NaN`` or the sentinel string ``"M"``) are serialised as
``null``.

Usage
-----
::

    python temp_graph_data.py

The output file ``temp_graph_data.json`` is written to the same directory as
this script.
"""

import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd

# ---------------------------------------------------------------------------
# Paths – resolved relative to this script so it works from any working dir
# ---------------------------------------------------------------------------

_HERE = Path(__file__).parent.resolve()
EXCEL_FILE = _HERE / "daily.xlsx"
OUTPUT_FILE = _HERE / "temp_graph_data.json"

# ---------------------------------------------------------------------------
# Column definitions
# ---------------------------------------------------------------------------

DATE_COLUMN = "day"
STATION_COLUMN = "station"

# Measurement columns to include in the output
DATA_COLUMNS = [
    "max_dewpoint_f",
    "precip_in",
    "avg_rh",
    "avg_feel",
    "srad_mj",
    "climo_high_f",
    "climo_precip_in",
]

# Sentinel string used in the source data to represent missing values
_MISSING_SENTINEL = "M"

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------


def _setup_logging() -> logging.Logger:
    """Return a logger that writes INFO+ messages to stdout."""
    log = logging.getLogger("temp_graph_data")
    if log.handlers:
        return log  # avoid duplicate handlers on re-import

    log.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    log.addHandler(handler)
    return log


logger = _setup_logging()

# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------


def read_excel(path: Path) -> pd.DataFrame:
    """Load the Excel workbook into a DataFrame."""
    logger.info("Reading Excel file: %s", path)
    if not path.exists():
        raise FileNotFoundError(
            f"Excel file not found: {path}\n"
            "Please place daily.xlsx in the same directory as this script."
        )
    try:
        df = pd.read_excel(path, engine="openpyxl")
    except Exception as exc:
        raise RuntimeError(f"Failed to read Excel file '{path}': {exc}") from exc

    logger.info("Loaded %d rows.", len(df))
    return df


def validate_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise column names and confirm all required columns are present."""
    df.columns = [str(c).strip().lower() for c in df.columns]

    required = {DATE_COLUMN, STATION_COLUMN} | set(DATA_COLUMNS)
    missing = required - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}\n"
            f"Found columns: {sorted(df.columns)}"
        )
    return df


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """Convert sentinel strings to NaN, parse dates, and drop invalid rows."""
    # Replace 'M' sentinel with NaN across all measurement columns
    for col in DATA_COLUMNS:
        df[col] = df[col].replace(_MISSING_SENTINEL, float("nan"))
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Parse dates
    df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN], errors="coerce")
    invalid = df[DATE_COLUMN].isna().sum()
    if invalid:
        logger.warning("%d row(s) with unparseable dates dropped.", invalid)
    df = df.dropna(subset=[DATE_COLUMN, STATION_COLUMN])

    # Sort for deterministic output
    df = df.sort_values([STATION_COLUMN, DATE_COLUMN])
    logger.info(
        "Data prepared: %d rows, date range %s → %s",
        len(df),
        df[DATE_COLUMN].min().date(),
        df[DATE_COLUMN].max().date(),
    )
    return df


def build_json(df: pd.DataFrame) -> Dict[str, Dict[str, Dict[str, Optional[float]]]]:
    """Build the nested {station -> {date -> measurements}} dictionary."""
    data: Dict[str, Any] = {}

    for _, row in df.iterrows():
        station = str(row[STATION_COLUMN])
        date_str = row[DATE_COLUMN].strftime("%Y-%m-%d")

        if station not in data:
            data[station] = {}

        data[station][date_str] = {
            col: (None if pd.isna(row[col]) else float(row[col]))
            for col in DATA_COLUMNS
        }

    station_count = len(data)
    record_count = sum(len(v) for v in data.values())
    logger.info(
        "Built JSON structure: %d station(s), %d date record(s).",
        station_count,
        record_count,
    )
    return data


def save_json(data: dict, path: Path) -> None:
    """Serialise *data* to a JSON file at *path*."""
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
        logger.info("JSON written → %s", path)
    except Exception as exc:
        raise RuntimeError(f"Failed to write JSON to '{path}': {exc}") from exc


# ---------------------------------------------------------------------------
# Public entry-point
# ---------------------------------------------------------------------------


def generate(
    excel_path: Optional[Path] = None,
    output_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Read *excel_path* and write meteorological data to *output_path* as JSON.

    Parameters
    ----------
    excel_path:
        Path to the source Excel file (defaults to ``daily.xlsx`` next to this
        script).
    output_path:
        Destination JSON file (defaults to ``temp_graph_data.json`` next to
        this script).

    Returns
    -------
    dict
        The generated data structure.
    """
    excel_path = excel_path or EXCEL_FILE
    output_path = output_path or OUTPUT_FILE

    df = read_excel(excel_path)
    df = validate_columns(df)
    df = prepare_data(df)
    data = build_json(df)
    save_json(data, output_path)
    return data


def main() -> None:
    """CLI entry-point."""
    logger.info("Starting temperature graph data generation.")
    try:
        data = generate()
    except FileNotFoundError as exc:
        logger.error("%s", exc)
        sys.exit(1)
    except (ValueError, RuntimeError) as exc:
        logger.error("%s", exc)
        sys.exit(1)
    except Exception as exc:  # noqa: BLE001
        logger.exception("Unexpected error: %s", exc)
        sys.exit(1)

    station_count = len(data)
    record_count = sum(len(v) for v in data.values())
    print(
        f"\n✓ temp_graph_data.json generated successfully.\n"
        f"  Stations : {station_count}\n"
        f"  Records  : {record_count}\n"
        f"  Output   : {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()
