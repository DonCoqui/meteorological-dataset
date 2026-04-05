"""
example_usage.py
================
Practical examples showing how to use the MeteorologicalProcessor
for common meteorological data tasks.

Run any example directly::

    python example_usage.py

Each function demonstrates a focused use-case so you can copy-paste
only the parts you need into your own scripts.
"""

import os
import sqlite3
from pathlib import Path

import pandas as pd


# ---------------------------------------------------------------------------
# Example 1 – Basic processing (default config)
# ---------------------------------------------------------------------------

def example_basic_processing():
    """Load the configured Excel file and export to all formats."""
    print("\n=== Example 1: Basic Processing ===")
    from data_processor import MeteorologicalProcessor

    processor = MeteorologicalProcessor()
    df = processor.process()

    print(f"Processed {len(df)} records.")
    print(df.head())


# ---------------------------------------------------------------------------
# Example 2 – Custom file path
# ---------------------------------------------------------------------------

def example_custom_path():
    """Process an Excel file that is not the one set in config.py."""
    print("\n=== Example 2: Custom File Path ===")
    from data_processor import MeteorologicalProcessor

    custom_path = r"C:\Users\destr\OneDrive\Desktop\enero-mayo 2026\Trabajo\daily.xlsx"

    # The output will still go to the directory defined in config.py.
    processor = MeteorologicalProcessor(excel_path=custom_path)
    try:
        df = processor.process()
        print(f"Loaded {len(df)} rows from {custom_path}")
    except FileNotFoundError:
        print(f"File not found at: {custom_path}. Update the path and retry.")


# ---------------------------------------------------------------------------
# Example 3 – Query by date range
# ---------------------------------------------------------------------------

def example_query_by_date_range():
    """Filter processed records to a specific date range."""
    print("\n=== Example 3: Query by Date Range ===")
    from data_processor import MeteorologicalProcessor
    import config

    processor = MeteorologicalProcessor()
    try:
        df = processor.process()
    except FileNotFoundError:
        print("Source Excel file not found. Skipping this example.")
        return

    start = "2026-01-01"
    end   = "2026-03-31"

    mask = (df[config.DATE_COLUMN] >= start) & (df[config.DATE_COLUMN] <= end)
    subset = df.loc[mask]

    print(f"Records from {start} to {end}: {len(subset)}")
    if not subset.empty:
        print(subset[[config.DATE_COLUMN, config.STATION_COLUMN, "precip_in"]].head(10))


# ---------------------------------------------------------------------------
# Example 4 – Filter by station
# ---------------------------------------------------------------------------

def example_filter_by_station():
    """Work with data from a single weather station."""
    print("\n=== Example 4: Filter by Station ===")
    from data_processor import MeteorologicalProcessor
    import config

    processor = MeteorologicalProcessor()
    try:
        df = processor.process()
    except FileNotFoundError:
        print("Source Excel file not found. Skipping this example.")
        return

    # List all available stations
    stations = sorted(df[config.STATION_COLUMN].dropna().unique())
    print(f"Available stations: {stations}")

    if not stations:
        print("No stations found in the data.")
        return

    target_station = stations[0]
    station_df = df[df[config.STATION_COLUMN] == target_station]

    print(f"\nStation: {target_station} — {len(station_df)} records")
    print(station_df.describe())


# ---------------------------------------------------------------------------
# Example 5 – Query the SQLite database directly
# ---------------------------------------------------------------------------

def example_sqlite_query():
    """Read data directly from the exported SQLite database."""
    print("\n=== Example 5: SQLite Query ===")
    import config

    db_path = Path(config.OUTPUT_DIR) / config.SQLITE_DB_FILENAME

    if not db_path.exists():
        print(f"Database not found at {db_path}. Run example_basic_processing() first.")
        return

    conn = sqlite3.connect(db_path)

    # Monthly average precipitation per station
    query = f"""
        SELECT
            strftime('%Y-%m', {config.DATE_COLUMN}) AS month,
            {config.STATION_COLUMN},
            ROUND(AVG(precip_in), 3)   AS avg_precip_in,
            ROUND(AVG(avg_rh), 1)      AS avg_rh,
            ROUND(AVG(srad_mj), 2)     AS avg_srad_mj
        FROM {config.SQLITE_TABLE_NAME}
        GROUP BY month, {config.STATION_COLUMN}
        ORDER BY month, {config.STATION_COLUMN}
    """

    result = pd.read_sql_query(query, conn)
    conn.close()

    print("Monthly averages by station:")
    print(result)


# ---------------------------------------------------------------------------
# Example 6 – Batch processing of multiple Excel files
# ---------------------------------------------------------------------------

def example_batch_processing():
    """Merge two or more Excel files into a single dataset."""
    print("\n=== Example 6: Batch Processing ===")
    from data_processor import MeteorologicalProcessor

    # Provide a list of Excel file paths to process together.
    files = [
        r"C:\Users\destr\OneDrive\Desktop\enero-mayo 2026\Trabajo\daily.xlsx",
        # Add more paths here as needed, e.g.:
        # r"C:\...\june-august.xlsx",
    ]

    existing = [f for f in files if Path(f).exists()]
    if not existing:
        print("No Excel files found. Update the 'files' list with valid paths.")
        return

    processor = MeteorologicalProcessor()
    df = processor.process_batch(existing)
    print(f"Batch result: {len(df)} records across {len(existing)} file(s).")


# ---------------------------------------------------------------------------
# Example 7 – Summary statistics per station
# ---------------------------------------------------------------------------

def example_summary_statistics():
    """Compute descriptive statistics grouped by weather station."""
    print("\n=== Example 7: Summary Statistics per Station ===")
    from data_processor import MeteorologicalProcessor
    import config

    processor = MeteorologicalProcessor()
    try:
        df = processor.process()
    except FileNotFoundError:
        print("Source Excel file not found. Skipping this example.")
        return

    numeric_cols = [
        "max_dewpoint_f", "precip_in", "avg_rh",
        "avg_feel", "srad_mj", "climo_high_f", "climo_precip_in",
    ]
    available = [c for c in numeric_cols if c in df.columns]

    summary = df.groupby(config.STATION_COLUMN)[available].agg(
        ["mean", "min", "max", "std"]
    ).round(3)

    print(summary)


# ---------------------------------------------------------------------------
# Main – run all examples
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    example_basic_processing()
    example_custom_path()
    example_query_by_date_range()
    example_filter_by_station()
    example_sqlite_query()
    example_batch_processing()
    example_summary_statistics()
