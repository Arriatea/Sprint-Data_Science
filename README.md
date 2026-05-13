# Sprint-Data_Science

Reusable preprocessing pipeline for CSV datasets.

## What it does

- Reads large CSVs in chunks, so files do not need to fit fully in memory.
- Works with different CSV schemas through JSON configuration.
- Normalizes column names, trims string fields, handles missing values, coerces types, parses dates, and optimizes low-cardinality text columns.
- Writes a manifest beside the processed data with row counts, output columns, and run metadata.

## Quick start

Profile a CSV before processing:

```powershell
python csv_preprocessor.py --config configs/example_preprocess.json --profile --profile-rows 1000
```

Run preprocessing:

```powershell
python csv_preprocessor.py --config configs/example_preprocess.json
```

Use it for another CSV without changing code:

```powershell
python csv_preprocessor.py --input path/to/input.csv --output data/processed/output.csv
```

For custom parsing, types, date columns, or missing-value rules, copy
`configs/example_preprocess.json` and edit the JSON.

## Configuration options

- `read_csv`: options passed to `pandas.read_csv`, such as `sep`, `encoding`, `quotechar`, `decimal`, `thousands`, and `on_bad_lines`.
- `select_columns`, `drop_columns`, `rename_columns`: schema-specific column controls.
- `dtype_overrides`: explicit type conversions, for example `string`, `Int64`, `float`, or `boolean`.
- `datetime_columns`: map of column name to date format. Use `null` to let pandas infer the format.
- `missing_values`: per-column strategy. Supported values are `drop`, `median`, `mean`, `mode`, or a literal fill value.
- `chunksize`: number of rows processed at a time.
- `output_format`: `csv` or `parquet`.
