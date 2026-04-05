# Contributing

Thank you for your interest in contributing meteorological data or improvements to this project. This guide explains how to add new data, follow quality standards, and submit changes.

---

## Ways to Contribute

| Type | Description |
|------|-------------|
| **New data** | Add Excel files with additional stations or date ranges |
| **Bug fixes** | Fix issues in `data_processor.py` or `config.py` |
| **Documentation** | Improve guides, correct errors, add examples |
| **Features** | Add new export formats, validation rules, or analysis helpers |

---

## Adding New Meteorological Data

### File format requirements

New Excel files must contain the columns listed in the [Data Dictionary](DATA_DICTIONARY.md):

```
station | day | max_dewpoint_f | precip_in | avg_rh | avg_feel | srad_mj | climo_high_f | climo_precip_in
```

- Column names are case-insensitive; extra columns are ignored.
- The `day` column must contain recognisable dates.
- Numeric columns must use decimal notation (e.g., `0.25`, not `1/4`).
- Do not merge cells or add summary rows — one row per station per day.

### Validate your file before contributing

Run the processor against your file and confirm the quality summary shows no unexpected dropped rows:

```bash
python data_processor.py
```

Check `processor.log` for any warnings about out-of-range values.

### Station identifier conventions

- Use a consistent, short identifier (e.g., `"KTUL"`, `"STATION_42"`).
- If your station already exists in the dataset, ensure the identifier matches exactly.
- Do not use spaces in station identifiers; use underscores instead.

---

## Submitting a Pull Request

1. **Fork** the repository and create a new branch:

   ```bash
   git checkout -b add-data/station-name-year
   ```

2. **Add your Excel file** to the `data/` directory (create it if it does not exist):

   ```
   data/
   └── station_name_2026.xlsx
   ```

3. **Update `config.py`** if you are adding a new default file path or validation range.

4. **Run the processor** to confirm your data loads without errors:

   ```bash
   python data_processor.py
   ```

5. **Commit your changes** with a descriptive message:

   ```bash
   git add data/station_name_2026.xlsx
   git commit -m "Add 2026 data for Station Name"
   ```

6. **Open a pull request** describing:
   - The station(s) included
   - Date range covered
   - Data source and collection method
   - Any known quality issues

---

## Data Quality Standards

All contributed data should meet the following standards:

### Completeness

- Aim for ≤ 5 % missing values per column across the submitted period.
- Document any known gaps (e.g., sensor outages) in the PR description.

### Accuracy

- Values should fall within the valid ranges defined in `config.py` (`VALIDATION_RANGES`).
- Outliers outside these ranges are allowed if they represent real extreme events — document them in the PR.

### Timeliness

- Include the most complete data available at the time of submission.
- Partial months are acceptable; label the file accordingly (e.g., `station_jan2026_partial.xlsx`).

### Source attribution

- State the data source (e.g., NOAA, local sensor network, university station) in the PR description.
- If the data is from a public source, include a link.

---

## Code Contributions

### Development setup

```bash
pip install -r requirements.txt
```

### Code style

- Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code.
- Use descriptive variable names; avoid single-letter names outside loop counters.
- Add docstrings to all public functions and classes.
- Keep functions focused — one responsibility per function.

### Testing your changes

Before submitting a code change, verify that:

1. `data_processor.py` runs end-to-end without errors on the default file.
2. All three output files are created (`CSV`, `JSON`, `SQLite`).
3. The data-quality summary in the log looks reasonable.
4. No existing functionality has been removed or broken.

### Configuration changes

If you add a new configuration key to `config.py`:

- Give it a descriptive name in `UPPER_SNAKE_CASE`.
- Add a comment explaining what it does and its default value.
- Update the [Processing Guide](PROCESSING_GUIDE.md) if the change affects user workflow.

---

## Reporting Issues

If you encounter a bug or have a question:

1. Check the existing [issues](../../issues) first.
2. If none matches, open a new issue with:
   - A clear title
   - Steps to reproduce the problem
   - The relevant portion of `processor.log`
   - Python and library versions (`pip show pandas openpyxl sqlalchemy`)

---

## Code of Conduct

- Be respectful and constructive in all communications.
- Data accuracy matters — do not knowingly submit falsified or fabricated observations.
- Attribute data to its original source.
