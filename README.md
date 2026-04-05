# Meteorological Dataset

A Python pipeline for processing, validating, and storing long-term meteorological and climatological data from daily weather-station observations.

---

## Features

- **Reads Excel files** (`.xlsx`) with daily meteorological observations across multiple weather stations.
- **Validates and cleans** data using configurable acceptable ranges per column.
- **Organises records** with *date* (`day`) as the primary temporal key and *station* as the secondary key.
- **Exports to CSV, JSON, and SQLite** — ready for spreadsheets, APIs, and time-series queries.
- **Supports batch processing** — merge observations from multiple Excel files into a single dataset.
- **Comprehensive logging** with a data-quality summary after every run.

---

## Project Structure

```
meteorological-dataset/
├── data_processor.py     # Core processing pipeline
├── config.py             # File paths, validation ranges, and options
├── example_usage.py      # 7 ready-to-run usage examples
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── DATA_DICTIONARY.md    # Column definitions, units, and valid ranges
├── DATASET_SCHEMA.md     # Database schema design and indexing strategy
├── PROCESSING_GUIDE.md   # Step-by-step usage guide with troubleshooting
└── CONTRIBUTING.md       # How to contribute new data and best practices
```

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/DonCoqui/meteorological-dataset.git
cd meteorological-dataset
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your Excel file path

Open `config.py` and update `EXCEL_FILE_PATH` to point to your `daily.xlsx`:

```python
EXCEL_FILE_PATH = r"C:\Users\destr\OneDrive\Desktop\enero-mayo 2026\Trabajo\daily.xlsx"
```

### 4. Run the processor

```bash
python data_processor.py
```

Processed files are written to the `output/` directory:

| File | Format |
|------|--------|
| `output/meteorological_data.csv` | Comma-separated values |
| `output/meteorological_data.json` | JSON (records) |
| `output/meteorological_data.db` | SQLite database |

---

## Input Data Format

Your Excel file must contain the following columns (column names are case-insensitive):

| Column | Description |
|--------|-------------|
| `station` | Weather station identifier |
| `day` | Observation date (primary key) |
| `max_dewpoint_f` | Maximum dew point (°F) |
| `precip_in` | Precipitation (inches) |
| `avg_rh` | Average relative humidity (%) |
| `avg_feel` | Average "feels like" temperature (°F) |
| `srad_mj` | Solar radiation (MJ/m²) |
| `climo_high_f` | Climatological high temperature (°F) |
| `climo_precip_in` | Climatological precipitation (inches) |

See [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md) for full specifications.

---

## Documentation

| Document | Purpose |
|----------|---------|
| [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md) | Column definitions, units, data types, valid ranges, quality notes |
| [`DATASET_SCHEMA.md`](DATASET_SCHEMA.md) | Database schema and indexing strategy for long-term storage |
| [`PROCESSING_GUIDE.md`](PROCESSING_GUIDE.md) | Step-by-step guide with examples and troubleshooting |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to contribute new meteorological data |

---

## Example Usage

```python
from data_processor import MeteorologicalProcessor

# Basic usage
processor = MeteorologicalProcessor()
df = processor.process()

# Batch processing
processor.process_batch([
    "january.xlsx",
    "february.xlsx",
])
```

See [`example_usage.py`](example_usage.py) for 7 complete examples.

---

## License

This project is open source. See the repository for details.
