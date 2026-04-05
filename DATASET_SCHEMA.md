# Dataset Schema

Database schema design for long-term climatological storage, with recommended indexing strategy for efficient time-series queries.

---

## Conceptual Model

```
┌────────────────────────────────────────────┐
│              daily_observations            │
├────────────────────────────────────────────┤
│ PK  day              DATE   NOT NULL       │
│ PK  station          TEXT   NOT NULL       │
├────────────────────────────────────────────┤
│     max_dewpoint_f   REAL                  │
│     precip_in        REAL                  │
│     avg_rh           REAL                  │
│     avg_feel         REAL                  │
│     srad_mj          REAL                  │
│     climo_high_f     REAL                  │
│     climo_precip_in  REAL                  │
└────────────────────────────────────────────┘
```

The composite primary key `(day, station)` uniquely identifies each daily observation.

---

## SQLite DDL

```sql
CREATE TABLE IF NOT EXISTS daily_observations (
    day              TEXT    NOT NULL,   -- ISO 8601 date: YYYY-MM-DD
    station          TEXT    NOT NULL,   -- Station identifier

    -- Observed measurements
    max_dewpoint_f   REAL,               -- Max dew point (°F)
    precip_in        REAL,               -- Precipitation (in)
    avg_rh           REAL,               -- Average relative humidity (%)
    avg_feel         REAL,               -- Average "feels like" temp (°F)
    srad_mj          REAL,               -- Solar radiation (MJ/m²)

    -- Climatological normals
    climo_high_f     REAL,               -- Climo high temperature (°F)
    climo_precip_in  REAL,               -- Climo precipitation (in)

    PRIMARY KEY (day, station)
);
```

---

## Indexing Strategy

Three indexes are created automatically by `data_processor.py` to accelerate the most common query patterns:

### 1. Date index — `idx_day`

```sql
CREATE INDEX IF NOT EXISTS idx_day ON daily_observations (day);
```

**Optimises:** date-range scans, seasonal aggregations, year-over-year comparisons.

### 2. Station index — `idx_station`

```sql
CREATE INDEX IF NOT EXISTS idx_station ON daily_observations (station);
```

**Optimises:** station-specific extracts, cross-station comparisons.

### 3. Composite date + station index — `idx_day_station`

```sql
CREATE INDEX IF NOT EXISTS idx_day_station ON daily_observations (day, station);
```

**Optimises:** exact-record lookups and queries that filter on both dimensions simultaneously.

---

## Extending the Schema

### Adding a new measurement column

```sql
ALTER TABLE daily_observations ADD COLUMN min_temp_f REAL;
```

Update `REQUIRED_COLUMNS` and `VALIDATION_RANGES` in `config.py` to include the new column.

### Partitioning strategy (PostgreSQL / large datasets)

For datasets spanning decades, consider partitioning by year:

```sql
CREATE TABLE daily_observations (
    day              DATE    NOT NULL,
    station          TEXT    NOT NULL,
    ...
) PARTITION BY RANGE (day);

CREATE TABLE daily_obs_2024 PARTITION OF daily_observations
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

CREATE TABLE daily_obs_2025 PARTITION OF daily_observations
    FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
```

### Station metadata (optional table)

```sql
CREATE TABLE IF NOT EXISTS stations (
    station     TEXT PRIMARY KEY,
    name        TEXT,
    latitude    REAL,
    longitude   REAL,
    elevation_m REAL,
    network     TEXT,
    active_from DATE,
    active_to   DATE
);
```

Join with `daily_observations` on `station` to enrich queries with geographic context.

---

## Common Queries

### Annual precipitation totals per station

```sql
SELECT
    strftime('%Y', day)  AS year,
    station,
    ROUND(SUM(precip_in), 2) AS total_precip_in
FROM daily_observations
GROUP BY year, station
ORDER BY year, station;
```

### Days warmer than climatological normal

```sql
SELECT day, station, avg_feel, climo_high_f,
       ROUND(avg_feel - climo_high_f, 1) AS anomaly_f
FROM daily_observations
WHERE avg_feel > climo_high_f
ORDER BY anomaly_f DESC;
```

### Monthly average relative humidity

```sql
SELECT
    strftime('%Y-%m', day) AS month,
    station,
    ROUND(AVG(avg_rh), 1) AS mean_rh_pct
FROM daily_observations
GROUP BY month, station
ORDER BY month, station;
```

### Wettest days on record

```sql
SELECT day, station, precip_in
FROM daily_observations
ORDER BY precip_in DESC
LIMIT 10;
```

---

## Data Lifecycle

| Stage | Tool | Output |
|-------|------|--------|
| Ingest raw Excel | `data_processor.py` | Validated DataFrame |
| Export | `data_processor.py` | CSV, JSON, SQLite |
| Query | SQLite CLI / pandas / SQLAlchemy | Analysis results |
| Archive | Copy `.db` file to long-term storage | Historical snapshots |

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0 | 2026-04 | Initial schema with 9 columns and 3 indexes |
