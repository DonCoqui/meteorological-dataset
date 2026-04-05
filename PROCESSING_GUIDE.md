# Processing Guide

Step-by-step instructions for using `data_processor.py` to load, validate, and export meteorological data.

---

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.9 or later |
| pandas | ≥ 2.0 |
| openpyxl | ≥ 3.1 |
| SQLAlchemy | ≥ 2.0 |

Install all dependencies in one command:

```bash
pip install -r requirements.txt
```

---

## Step 1 — Prepare your Excel file

Ensure your Excel file (`daily.xlsx`) contains the following columns (column names are case-insensitive and leading/trailing spaces are stripped automatically):

```
station  |  day  |  max_dewpoint_f  |  precip_in  |  avg_rh  |  avg_feel  |  srad_mj  |  climo_high_f  |  climo_precip_in
```

- The `day` column should contain dates in a recognised format (e.g., `2026-01-15`, `01/15/2026`).
- Numeric columns may contain blanks; these are treated as missing values (`NaN`).
- Extra columns in the file are ignored.

---

## Step 2 — Configure paths and options

Open `config.py` and update these settings for your environment:

```python
# Path to your Excel file
EXCEL_FILE_PATH = r"C:\Users\destr\OneDrive\Desktop\enero-mayo 2026\Trabajo\daily.xlsx"

# Where to write the output files (created automatically if it doesn't exist)
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

# Set to True to drop rows with any out-of-range values
STRICT_VALIDATION = False

# Logging level: DEBUG | INFO | WARNING | ERROR
LOG_LEVEL = "INFO"
```

---

## Step 3 — Run the processor

```bash
python data_processor.py
```

### Expected console output

```
2026-04-05 10:00:00 [INFO] meteo_processor: Starting meteorological data processing pipeline.
2026-04-05 10:00:00 [INFO] meteo_processor: Reading Excel file: daily.xlsx
2026-04-05 10:00:01 [INFO] meteo_processor: Loaded 150 rows from daily.xlsx
2026-04-05 10:00:01 [INFO] meteo_processor: Date range: 2026-01-01 → 2026-05-31
2026-04-05 10:00:01 [INFO] meteo_processor: CSV exported → output/meteorological_data.csv
2026-04-05 10:00:01 [INFO] meteo_processor: JSON exported → output/meteorological_data.json
2026-04-05 10:00:01 [INFO] meteo_processor: SQLite exported → output/meteorological_data.db
2026-04-05 10:00:01 [INFO] meteo_processor: === Data Quality Summary ===
  Total rows loaded   : 150
  Rows after cleaning : 148
  Rows dropped        : 2
  Flagged values      : 3
  Date range          : 2026-01-01 → 2026-05-31
  Stations            : ['STATION_A', 'STATION_B']

Processing complete. 148 rows written to 'output'.
```

---

## Step 4 — Inspect the output

After a successful run, the `output/` directory will contain:

```
output/
├── meteorological_data.csv   ← open in Excel or pandas
├── meteorological_data.json  ← use in web apps or APIs
└── meteorological_data.db    ← query with SQLite or SQLAlchemy
```

### Open in pandas

```python
import pandas as pd

df = pd.read_csv("output/meteorological_data.csv", parse_dates=["day"])
print(df.head())
print(df.dtypes)
```

### Query with SQLite

```bash
sqlite3 output/meteorological_data.db
```

```sql
.headers on
.mode column
SELECT day, station, precip_in FROM daily_observations LIMIT 10;
```

---

## Advanced Usage

### Batch processing

Process multiple Excel files at once and merge the results:

```python
from data_processor import MeteorologicalProcessor

processor = MeteorologicalProcessor()
df = processor.process_batch([
    "data/january.xlsx",
    "data/february.xlsx",
    "data/march.xlsx",
])
print(f"Total records: {len(df)}")
```

Duplicate records (same `day` + `station`) are removed automatically.

### Custom output directory

```python
processor = MeteorologicalProcessor(output_dir="/mnt/nas/meteo_archive")
df = processor.process()
```

### Programmatic access without exporting

If you only want the cleaned DataFrame and do not need the output files, call the private helper directly:

```python
from data_processor import MeteorologicalProcessor

processor = MeteorologicalProcessor()
df = processor._load_and_clean("daily.xlsx")
```

---

## Validation Rules

The processor applies these rules by default (configurable in `config.py`):

| Column | Min | Max | Out-of-range action (default) |
|--------|-----|-----|-------------------------------|
| `max_dewpoint_f` | −60 °F | 90 °F | Warning logged, value kept |
| `precip_in` | 0 in | 30 in | Warning logged, value kept |
| `avg_rh` | 0 % | 100 % | Warning logged, value kept |
| `avg_feel` | −80 °F | 140 °F | Warning logged, value kept |
| `srad_mj` | 0 MJ/m² | 50 MJ/m² | Warning logged, value kept |
| `climo_high_f` | −60 °F | 140 °F | Warning logged, value kept |
| `climo_precip_in` | 0 in | 30 in | Warning logged, value kept |

Set `STRICT_VALIDATION = True` in `config.py` to replace out-of-range values with `NaN` and drop rows that become incomplete.

---

## Troubleshooting

### `FileNotFoundError: Excel file not found`

Update `EXCEL_FILE_PATH` in `config.py` to the correct absolute path. On Windows, prefix the string with `r` to avoid backslash issues:

```python
EXCEL_FILE_PATH = r"C:\Users\...\daily.xlsx"
```

### `ValueError: Missing required columns`

The error message lists the missing column names. Check that your Excel file uses the exact column names shown in [Step 1](#step-1--prepare-your-excel-file). Column names are normalised to lowercase during processing, so capitalisation differences are handled automatically.

### `ModuleNotFoundError: No module named 'openpyxl'`

Run:

```bash
pip install -r requirements.txt
```

### Dates are not being parsed correctly

Set `DATE_FORMAT` in `config.py` to the explicit format string used in your file:

```python
DATE_FORMAT = "%m/%d/%Y"   # e.g. 01/15/2026
# or
DATE_FORMAT = "%d-%b-%Y"   # e.g. 15-Jan-2026
```

### The output SQLite file already exists

By default the table is **replaced** on each run (`if_exists="replace"`). To **append** instead, change the `if_exists` argument in the `_export_sqlite` method of `data_processor.py`:

```python
df_copy.to_sql(..., if_exists="append", ...)
```

---

## Log File

When `ENABLE_FILE_LOGGING = True` (default), a `processor.log` file is written to the project root alongside the script. Change the log path in `config.py`:

```python
LOG_FILE = "/var/log/meteo_processor.log"
```
