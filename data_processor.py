"""
data_processor.py
=================
Main data processing module for the Meteorological Dataset project.

Responsibilities
----------------
- Read one or more Excel files that contain daily meteorological observations.
- Validate and clean each record against configurable value ranges.
- Organise data with *date* (day) as the primary temporal key and *station*
  as the secondary key.
- Export the cleaned dataset to CSV, JSON, and SQLite formats.
- Emit detailed log messages and a data-quality summary.

Usage
-----
Run directly::

    python data_processor.py

Or import and call from your own scripts::

    from data_processor import MeteorologicalProcessor
    processor = MeteorologicalProcessor()
    df = processor.process()
"""

import logging
import os
import sys
from pathlib import Path
from typing import List, Optional

import pandas as pd
from sqlalchemy import create_engine, text

import config


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

def _setup_logging() -> logging.Logger:
    """Configure and return the module-level logger."""
    logger = logging.getLogger("meteo_processor")
    logger.setLevel(getattr(logging, config.LOG_LEVEL, logging.INFO))

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler (always enabled)
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Optional file handler
    if config.ENABLE_FILE_LOGGING:
        fh = logging.FileHandler(config.LOG_FILE, encoding="utf-8")
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


logger = _setup_logging()


# ---------------------------------------------------------------------------
# Core processor class
# ---------------------------------------------------------------------------

class MeteorologicalProcessor:
    """Read, validate, clean, and export meteorological daily observations."""

    def __init__(
        self,
        excel_path: Optional[str] = None,
        output_dir: Optional[str] = None,
    ) -> None:
        self.excel_path = Path(excel_path or config.EXCEL_FILE_PATH)
        self.output_dir = Path(output_dir or config.OUTPUT_DIR)
        self._df: Optional[pd.DataFrame] = None

        # Quality-check counters reset on each call to process()
        self._total_rows: int = 0
        self._invalid_rows: int = 0
        self._flagged_values: int = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def process(self) -> pd.DataFrame:
        """Run the full pipeline and return the cleaned DataFrame.

        Steps
        -----
        1. Read Excel file.
        2. Validate required columns.
        3. Parse dates.
        4. Validate value ranges.
        5. Sort by date and station.
        6. Export to all configured formats.
        7. Print quality summary.
        """
        logger.info("Starting meteorological data processing pipeline.")

        df = self._read_excel(self.excel_path)
        df = self._validate_columns(df)
        df = self._parse_dates(df)
        df = self._validate_ranges(df)
        df = self._sort_data(df)

        self._df = df
        self._ensure_output_dir()
        self._export_csv(df)
        self._export_json(df)
        self._export_sqlite(df)
        self._print_quality_summary(df)

        logger.info("Pipeline completed successfully.")
        return df

    def process_batch(self, excel_paths: List[str]) -> pd.DataFrame:
        """Process multiple Excel files and merge the results.

        Parameters
        ----------
        excel_paths:
            Sequence of paths to Excel files to process and merge.

        Returns
        -------
        Merged, deduplicated DataFrame sorted by date and station.
        """
        frames: List[pd.DataFrame] = []
        for path in excel_paths:
            logger.info("Batch processing: %s", path)
            processor = MeteorologicalProcessor(
                excel_path=path,
                output_dir=str(self.output_dir),
            )
            try:
                frames.append(processor._load_and_clean(path))
            except Exception as exc:  # noqa: BLE001
                logger.error("Skipping %s due to error: %s", path, exc)

        if not frames:
            raise ValueError("No files were successfully loaded.")

        combined = pd.concat(frames, ignore_index=True)
        combined = combined.drop_duplicates(
            subset=[config.DATE_COLUMN, config.STATION_COLUMN]
        )
        combined = self._sort_data(combined)
        self._df = combined
        self._ensure_output_dir()
        self._export_csv(combined)
        self._export_json(combined)
        self._export_sqlite(combined)
        self._print_quality_summary(combined)
        return combined

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load_and_clean(self, path: str) -> pd.DataFrame:
        """Read + validate + range-check a single file (no export)."""
        df = self._read_excel(Path(path))
        df = self._validate_columns(df)
        df = self._parse_dates(df)
        df = self._validate_ranges(df)
        return df

    # -- I/O ---------------------------------------------------------------

    def _read_excel(self, path: Path) -> pd.DataFrame:
        """Load an Excel workbook into a DataFrame."""
        logger.info("Reading Excel file: %s", path)
        if not path.exists():
            raise FileNotFoundError(
                f"Excel file not found: {path}\n"
                "Please update EXCEL_FILE_PATH in config.py."
            )
        try:
            df = pd.read_excel(path, engine="openpyxl")
        except Exception as exc:
            raise RuntimeError(f"Failed to read Excel file: {exc}") from exc

        self._total_rows = len(df)
        logger.info("Loaded %d rows from %s", self._total_rows, path.name)
        return df

    # -- Validation --------------------------------------------------------

    def _validate_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Ensure all required columns are present (case-insensitive)."""
        # Normalise column names to lowercase + strip whitespace
        df.columns = [c.strip().lower() for c in df.columns]

        missing = set(config.REQUIRED_COLUMNS) - set(df.columns)
        if missing:
            raise ValueError(
                f"Missing required columns: {sorted(missing)}\n"
                f"Found columns: {sorted(df.columns)}"
            )
        logger.debug("All required columns present.")
        return df

    def _parse_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Parse the date column to datetime dtype."""
        date_col = config.DATE_COLUMN
        try:
            df[date_col] = pd.to_datetime(
                df[date_col],
                format=config.DATE_FORMAT,
                infer_datetime_format=True,
                errors="coerce",
            )
        except TypeError:
            # Older pandas versions do not support infer_datetime_format
            df[date_col] = pd.to_datetime(
                df[date_col],
                format=config.DATE_FORMAT,
                errors="coerce",
            )

        invalid_dates = df[date_col].isna().sum()
        if invalid_dates:
            logger.warning(
                "%d row(s) have unparseable dates and will be dropped.",
                invalid_dates,
            )
            self._invalid_rows += invalid_dates
            df = df.dropna(subset=[date_col])

        logger.info("Date range: %s → %s", df[date_col].min(), df[date_col].max())
        return df

    def _validate_ranges(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate numeric columns against configured min/max ranges."""
        numeric_cols = [
            c for c in config.VALIDATION_RANGES if c in df.columns
        ]

        for col in numeric_cols:
            # Coerce to numeric (non-convertible values become NaN)
            df[col] = pd.to_numeric(df[col], errors="coerce")

            lo, hi = config.VALIDATION_RANGES[col]
            out_of_range = df[col].notna() & (
                (df[col] < lo) | (df[col] > hi)
            )
            count = out_of_range.sum()
            if count:
                self._flagged_values += count
                logger.warning(
                    "Column '%s': %d value(s) outside [%s, %s].",
                    col, count, lo, hi,
                )
                if config.STRICT_VALIDATION:
                    df.loc[out_of_range, col] = pd.NA
                    logger.debug(
                        "STRICT mode: replaced %d out-of-range '%s' values with NaN.",
                        count, col,
                    )
                # In non-strict mode we keep the values but log the warning.

        if config.STRICT_VALIDATION:
            before = len(df)
            df = df.dropna(subset=numeric_cols, how="any")
            dropped = before - len(df)
            if dropped:
                self._invalid_rows += dropped
                logger.info(
                    "STRICT mode: dropped %d row(s) with NaN in numeric columns.",
                    dropped,
                )

        return df

    def _sort_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Sort by date (primary) and station (secondary)."""
        sort_cols = [config.DATE_COLUMN, config.STATION_COLUMN]
        available = [c for c in sort_cols if c in df.columns]
        return df.sort_values(available).reset_index(drop=True)

    # -- Export ------------------------------------------------------------

    def _ensure_output_dir(self) -> None:
        """Create the output directory if it does not exist."""
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _export_csv(self, df: pd.DataFrame) -> None:
        """Write the DataFrame to a CSV file."""
        path = self.output_dir / config.CSV_FILENAME
        df.to_csv(path, index=False, date_format="%Y-%m-%d")
        logger.info("CSV exported → %s", path)

    def _export_json(self, df: pd.DataFrame) -> None:
        """Write the DataFrame to a JSON file (records orientation)."""
        path = self.output_dir / config.JSON_FILENAME
        df_copy = df.copy()
        # Serialise dates as ISO strings
        if pd.api.types.is_datetime64_any_dtype(df_copy[config.DATE_COLUMN]):
            df_copy[config.DATE_COLUMN] = df_copy[config.DATE_COLUMN].dt.strftime(
                "%Y-%m-%d"
            )
        df_copy.to_json(path, orient="records", indent=2)
        logger.info("JSON exported → %s", path)

    def _export_sqlite(self, df: pd.DataFrame) -> None:
        """Write the DataFrame to a SQLite database."""
        db_path = self.output_dir / config.SQLITE_DB_FILENAME
        engine = create_engine(f"sqlite:///{db_path}")

        df_copy = df.copy()
        # Store dates as ISO strings for maximum SQLite compatibility
        if pd.api.types.is_datetime64_any_dtype(df_copy[config.DATE_COLUMN]):
            df_copy[config.DATE_COLUMN] = df_copy[config.DATE_COLUMN].dt.strftime(
                "%Y-%m-%d"
            )

        with engine.begin() as conn:
            df_copy.to_sql(
                config.SQLITE_TABLE_NAME,
                conn,
                if_exists="replace",
                index=False,
            )
            # Create indexes for fast temporal and station queries
            conn.execute(
                text(
                    f"CREATE INDEX IF NOT EXISTS idx_day "
                    f"ON {config.SQLITE_TABLE_NAME} ({config.DATE_COLUMN})"
                )
            )
            conn.execute(
                text(
                    f"CREATE INDEX IF NOT EXISTS idx_station "
                    f"ON {config.SQLITE_TABLE_NAME} ({config.STATION_COLUMN})"
                )
            )
            conn.execute(
                text(
                    f"CREATE INDEX IF NOT EXISTS idx_day_station "
                    f"ON {config.SQLITE_TABLE_NAME} "
                    f"({config.DATE_COLUMN}, {config.STATION_COLUMN})"
                )
            )

        logger.info("SQLite exported → %s", db_path)

    # -- Quality summary ---------------------------------------------------

    def _print_quality_summary(self, df: pd.DataFrame) -> None:
        """Log a human-readable data-quality summary."""
        clean_rows = len(df)
        logger.info(
            "=== Data Quality Summary ===\n"
            "  Total rows loaded   : %d\n"
            "  Rows after cleaning : %d\n"
            "  Rows dropped        : %d\n"
            "  Flagged values      : %d\n"
            "  Date range          : %s → %s\n"
            "  Stations            : %s",
            self._total_rows,
            clean_rows,
            self._invalid_rows,
            self._flagged_values,
            df[config.DATE_COLUMN].min(),
            df[config.DATE_COLUMN].max(),
            sorted(df[config.STATION_COLUMN].dropna().unique()),
        )


# ---------------------------------------------------------------------------
# Entry-point
# ---------------------------------------------------------------------------

def main() -> None:
    """Process the default Excel file configured in config.py."""
    processor = MeteorologicalProcessor()
    try:
        df = processor.process()
        print(f"\nProcessing complete. {len(df)} rows written to '{config.OUTPUT_DIR}'.")
    except FileNotFoundError as exc:
        logger.error("%s", exc)
        sys.exit(1)
    except Exception as exc:  # noqa: BLE001
        logger.exception("Unexpected error: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
