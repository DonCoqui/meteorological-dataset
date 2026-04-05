"""
temp_graph_data.py
==================
Generate temperature and meteorological graph data indexed by station and date.

This module reads the daily meteorological observations from daily.xlsx
and structures them as nested JSON: {station: {date: {measurements}}}
"""

import logging
import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional

import pandas as pd

import config

def _setup_logging() -> logging.Logger:
    """Configure and return the module-level logger."""
    logger = logging.getLogger("temp_graph_data")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%%(asctime)s [%%(levelname)s] %%%(name)s: %%%(message)s",
        datefmt="%%Y-%%m-%%d %%H:%%M:%%S",
    )

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


logger = _setup_logging()


class TemperatureGraphDataGenerator:
    """Generate temperature and meteorological graph data indexed by station and date."""

    # Columns to include in the output (temperature and meteorological measurements)
    MEASUREMENT_COLUMNS = [
        "max_dewpoint_f",
        "precip_in",
        "avg_rh",
        "avg_feel",
        "srad_mj",
        "climo_high_f",
        "climo_precip_in",
    ]

    def __init__(self,
        excel_path: Optional[str] = None,
        output_dir: Optional[str] = None,
    ) -> None:
        self.excel_path = Path(excel_path or config.EXCEL_FILE_PATH)
        self.output_dir = Path(output_dir or config.OUTPUT_DIR)
        self.output_file = self.output_dir / "temp_graph_data.json"

    def generate(self) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """
        Read Excel file and generate temperature graph data indexed by station and date.

        Returns
        -------
        Nested dictionary structure: {station: {date: {measurements}}}
        """
        logger.info("Starting temperature graph data generation.")

        # Read and validate data
        df = self._read_excel()
        df = self._validate_columns(df)
        df = self._parse_dates(df)
        df = self._clean_data(df)

        # Structure the data
        graph_data = self._structure_data(df)

        # Export to JSON
        self._export_json(graph_data)

        logger.info("Temperature graph data generation completed successfully.")
        return graph_data

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _read_excel(self) -> pd.DataFrame:
        """Load the Excel workbook into a DataFrame."""
        logger.info("Reading Excel file: %%s", self.excel_path)
        if not self.excel_path.exists():
            raise FileNotFoundError(f"Excel file not found: {self.excel_path}")
        
        try:
            df = pd.read_excel(self.excel_path, engine="openpyxl")
            logger.info("Loaded %%d rows from Excel file", len(df))
            return df
        except Exception as exc:
            raise RuntimeError(f"Failed to read Excel file: {exc}") from exc

    def _validate_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Ensure all required columns are present."""
        # Normalize column names
        df.columns = [c.strip().lower() for c in df.columns]

        required = [config.DATE_COLUMN, config.STATION_COLUMN]
        missing = set(required) - set(df.columns)
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
                errors="coerce",
            )
        except Exception as exc:
            raise RuntimeError(f"Failed to parse dates: {exc}") from exc

        invalid_dates = df[date_col].isna().sum()
        if invalid_dates:
            logger.warning(
                "%%d row(s) have unparseable dates and will be dropped.",
                invalid_dates,
            )
            df = df.dropna(subset=[date_col])

        logger.info("Date range: %%s → %%s", df[date_col].min(), df[date_col].max())
        return df

    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and prepare data."""
        # Drop rows where station or date is missing
        df = df.dropna(subset=[config.STATION_COLUMN, config.DATE_COLUMN])
        
        # Convert measurement columns to numeric, replacing non-numeric with NaN
        for col in self.MEASUREMENT_COLUMNS:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        
        logger.info("Data cleaned. %%d rows remaining.", len(df))
        return df

    def _structure_data(self, df: pd.DataFrame) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """Structure the data as nested dict: {station: {date: {measurements}}}."""
        graph_data: Dict[str, Dict[str, Dict[str, Any]]] = {}

        for _, row in df.iterrows():
            station = row[config.STATION_COLUMN]
            date_str = row[config.DATE_COLUMN].strftime("%%Y-%%m-%%d")

            # Initialize station dict if needed
            if station not in graph_data:
                graph_data[station] = {}

            # Initialize date dict if needed
            if date_str not in graph_data[station]:
                graph_data[station][date_str] = {}

            # Add measurements
            for col in self.MEASUREMENT_COLUMNS:
                if col in df.columns:
                    value = row[col]
                    # Convert NaN to None for JSON serialization
                    graph_data[station][date_str][col] = (
                        None if pd.isna(value) else value
                    )

        logger.info("Data structured into %%d stations.", len(graph_data))
        return graph_data

    def _ensure_output_dir(self) -> None:
        """Create the output directory if it does not exist."""
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _export_json(self, graph_data: Dict[str, Dict[str, Dict[str, Any]]]) -> None:
        """Export the structured data to JSON file."""
        self._ensure_output_dir()
        try:
            with open(self.output_file, "w", encoding="utf-8") as f:
                json.dump(graph_data, f, indent=2, ensure_ascii=False)
            logger.info("JSON exported → %%s", self.output_file)
        except Exception as exc:
            raise RuntimeError(f"Failed to export JSON: {exc}") from exc


def main() -> None:
    """Generate temperature graph data from the configured Excel file."""
    generator = TemperatureGraphDataGenerator()
    try:
        graph_data = generator.generate()
        total_records = sum(len(dates) for dates in graph_data.values())
        print(
            f"\nSuccess! Generated temperature graph data for "
            f"%%d stations with %%d total records."
            f"\nOutput: {generator.output_file}"
        )
    except FileNotFoundError as exc:
        logger.error("%%s", exc)
        sys.exit(1)
    except Exception as exc:
        logger.exception("Unexpected error: %%s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()