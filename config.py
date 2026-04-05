"""
Configuration file for the Meteorological Dataset Processor.

Modify this file to customize file paths, validation ranges,
and processing options for your environment.
"""

import os

# ---------------------------------------------------------------------------
# File paths
# ---------------------------------------------------------------------------

# Absolute path to the source Excel file.
# Update this to match the location of your daily.xlsx file.
EXCEL_FILE_PATH = r"C:\Users\destr\OneDrive\Desktop\enero-mayo 2026\Trabajo\daily.xlsx"

# Directory where processed output files will be written.
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

# File names for each export format.
CSV_FILENAME = "meteorological_data.csv"
JSON_FILENAME = "meteorological_data.json"
SQLITE_DB_FILENAME = "meteorological_data.db"
SQLITE_TABLE_NAME = "daily_observations"

# ---------------------------------------------------------------------------
# Column definitions
# ---------------------------------------------------------------------------

# Expected columns in the source Excel file.
REQUIRED_COLUMNS = [
    "station",
    "day",
    "max_dewpoint_f",
    "precip_in",
    "avg_rh",
    "avg_feel",
    "srad_mj",
    "climo_high_f",
    "climo_precip_in",
]

# Date column name (used as the primary temporal key).
DATE_COLUMN = "day"

# Station identifier column name.
STATION_COLUMN = "station"

# ---------------------------------------------------------------------------
# Data validation ranges
# ---------------------------------------------------------------------------
# Records with values outside these ranges will be flagged or dropped,
# depending on the STRICT_VALIDATION setting below.
# Format: { "column_name": (min_value, max_value) }

VALIDATION_RANGES = {
    # Dew point in Fahrenheit: physically possible range
    "max_dewpoint_f": (-60.0, 90.0),
    # Precipitation in inches: must be non-negative; cap at extreme events
    "precip_in": (0.0, 30.0),
    # Average relative humidity: percentage 0–100
    "avg_rh": (0.0, 100.0),
    # Average "feels like" temperature in Fahrenheit
    "avg_feel": (-80.0, 140.0),
    # Solar radiation in MJ/m²: non-negative, capped at realistic daily max
    "srad_mj": (0.0, 50.0),
    # Climatological high temperature in Fahrenheit
    "climo_high_f": (-60.0, 140.0),
    # Climatological precipitation in inches
    "climo_precip_in": (0.0, 30.0),
}

# ---------------------------------------------------------------------------
# Processing options
# ---------------------------------------------------------------------------

# When True, rows that fail validation are removed from the output.
# When False, out-of-range values are replaced with NaN but the row is kept.
STRICT_VALIDATION = False

# Date format used when parsing the 'day' column.
# Set to None to let pandas auto-detect.
DATE_FORMAT = None  # e.g. "%Y-%m-%d" or "%m/%d/%Y"

# Logging configuration.
LOG_LEVEL = "INFO"          # DEBUG | INFO | WARNING | ERROR | CRITICAL
LOG_FILE = os.path.join(os.path.dirname(__file__), "processor.log")

# If True, a separate log file is written in addition to console output.
ENABLE_FILE_LOGGING = True
