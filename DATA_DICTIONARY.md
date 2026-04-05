# Data Dictionary

Complete reference for every column in the daily meteorological observations dataset.

---

## Column Reference

### `day` — Observation Date

| Attribute | Value |
|-----------|-------|
| **Data type** | Date (`YYYY-MM-DD`) |
| **Role** | Primary temporal key |
| **Valid range** | Any valid calendar date |
| **Null allowed** | No — rows with missing dates are dropped |
| **Notes** | All other measurements correspond to this calendar day. |

---

### `station` — Weather Station Identifier

| Attribute | Value |
|-----------|-------|
| **Data type** | String |
| **Role** | Secondary key (combined with `day` for uniqueness) |
| **Valid range** | Non-empty string |
| **Null allowed** | No |
| **Notes** | A unique identifier (name or code) assigned to each physical weather station. Multiple stations may have observations on the same date. |

---

### `max_dewpoint_f` — Maximum Dew Point Temperature

| Attribute | Value |
|-----------|-------|
| **Data type** | Float |
| **Unit** | Degrees Fahrenheit (°F) |
| **Valid range** | −60 to 90 °F |
| **Null allowed** | Yes |
| **Notes** | The highest dew point recorded during the day. The dew point is the temperature at which air becomes saturated with moisture. Higher values indicate more atmospheric moisture. |

---

### `precip_in` — Precipitation

| Attribute | Value |
|-----------|-------|
| **Data type** | Float |
| **Unit** | Inches (in) |
| **Valid range** | 0 to 30 in |
| **Null allowed** | Yes |
| **Notes** | Total liquid-equivalent precipitation (rain, melted snow, etc.) recorded during the day. Zero indicates a dry day. Trace amounts (<0.005 in) may be recorded as 0. |

---

### `avg_rh` — Average Relative Humidity

| Attribute | Value |
|-----------|-------|
| **Data type** | Float |
| **Unit** | Percent (%) |
| **Valid range** | 0 to 100 % |
| **Null allowed** | Yes |
| **Notes** | The mean relative humidity over the 24-hour observation period. Relative humidity expresses the ratio of actual water-vapour pressure to the saturation pressure at the same temperature. |

---

### `avg_feel` — Average "Feels Like" Temperature

| Attribute | Value |
|-----------|-------|
| **Data type** | Float |
| **Unit** | Degrees Fahrenheit (°F) |
| **Valid range** | −80 to 140 °F |
| **Null allowed** | Yes |
| **Notes** | The daily average of apparent (perceived) temperature, which combines actual temperature with wind speed and humidity to represent how the weather "feels" to a human. Computed from wind-chill (cold conditions) or heat-index (warm/humid conditions) algorithms. |

---

### `srad_mj` — Solar Radiation

| Attribute | Value |
|-----------|-------|
| **Data type** | Float |
| **Unit** | Megajoules per square metre (MJ/m²) |
| **Valid range** | 0 to 50 MJ/m² |
| **Null allowed** | Yes |
| **Notes** | Total incoming shortwave (solar) radiation at the surface for the day. Drives evapotranspiration calculations and crop models. Typical daily maxima: ~30 MJ/m² in summer at mid-latitudes; values near 0 are expected in winter or overcast conditions. |

---

### `climo_high_f` — Climatological High Temperature

| Attribute | Value |
|-----------|-------|
| **Data type** | Float |
| **Unit** | Degrees Fahrenheit (°F) |
| **Valid range** | −60 to 140 °F |
| **Null allowed** | Yes |
| **Notes** | The historical average (climatological normal) maximum temperature for this calendar day, typically derived from a 30-year baseline (e.g., 1991–2020 WMO normals). Use this value to compare current observations against long-term expectations. |

---

### `climo_precip_in` — Climatological Precipitation

| Attribute | Value |
|-----------|-------|
| **Data type** | Float |
| **Unit** | Inches (in) |
| **Valid range** | 0 to 30 in |
| **Null allowed** | Yes |
| **Notes** | The historical average (climatological normal) daily precipitation for this calendar day. Use this value to identify above-normal or below-normal precipitation events relative to the historical baseline. |

---

## Data Quality Flags

The processor applies the following quality checks automatically:

| Check | Action (default) | Action (STRICT mode) |
|-------|-----------------|----------------------|
| Missing required column | Raises error — processing stops | Same |
| Unparseable date | Row dropped | Same |
| Non-numeric value in numeric column | Replaced with `NaN` | Row dropped |
| Value outside valid range | Warning logged, value retained | Value set to `NaN`, then row dropped |

---

## Units Reference

| Unit | Symbol | Used for |
|------|--------|----------|
| Degrees Fahrenheit | °F | Temperature columns |
| Inches | in | Precipitation columns |
| Percent | % | Relative humidity |
| Megajoules per square metre | MJ/m² | Solar radiation |

---

## Missing Data

- Missing values are stored as `NaN` (CSV/DataFrame) or `null` (JSON/SQLite).
- The `day` and `station` columns must never be null; records lacking these values are discarded.
- For analyses requiring complete records, filter with `df.dropna()` or `WHERE column IS NOT NULL` in SQL.
