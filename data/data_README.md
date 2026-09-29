# Data Dictionary

This folder contains the sample healthcare source files used in the AWS Healthcare Patient Monitoring Pipeline.

The data is small and sample-based. It is used to demonstrate ingestion, cleaning, transformation, joining, health-status logic, and final reporting output.

---

## Files Included

```text
patient_vitals.csv
patient_details.csv
device_logs.csv
```

---

## 1. patient_vitals.csv

This file contains patient health monitoring readings.

### Columns

| Column | Description |
|---|---|
| patient_id | Unique patient identifier |
| timestamp | Time when the patient reading was captured |
| heart_rate | Patient heart rate reading |
| blood_pressure | Patient blood pressure reading |
| oxygen_level | Patient oxygen level reading |
| temperature | Patient body temperature reading |

### Data Quality Examples

This file includes sample data quality issues used for ETL practice:

- duplicate patient reading
- missing heart rate value
- missing oxygen level value
- critical oxygen reading
- high temperature reading
- high heart rate reading

These issues are handled in the Glue PySpark ETL job.

---

## 2. patient_details.csv

This file contains basic patient profile information.

### Columns

| Column | Description |
|---|---|
| patient_id | Unique patient identifier |
| name | Patient name |
| age | Patient age |
| gender | Patient gender |
| city | Patient city |
| disease | Existing medical condition or disease |

This dataset is joined with patient vitals using `patient_id`.

---

## 3. device_logs.csv

This file contains medical device activity information.

### Columns

| Column | Description |
|---|---|
| device_id | Unique device identifier |
| patient_id | Patient identifier connected to the device |
| device_type | Type of medical or monitoring device |
| status | Device activity status |
| last_sync | Last sync timestamp from the device |

This dataset is joined with patient vitals and patient details using `patient_id`.

---

## Main Join Key

The main join key across the datasets is:

```text
patient_id
```

The ETL job joins:

```text
patient_vitals.csv + patient_details.csv + device_logs.csv
```

to create the final patient monitoring report.

---

## Data Usage in ETL

The Glue PySpark ETL job uses these files through Glue Data Catalog tables.

The ETL process:

1. Reads patient vitals, patient details, and device logs.
2. Removes duplicate records.
3. Filters records with missing patient IDs.
4. Handles missing heart rate and oxygen level values.
5. Converts timestamp fields.
6. Creates `monitoring_date` and `monitoring_hour`.
7. Creates `health_status`.
8. Creates `alert_flag`.
9. Joins all datasets.
10. Writes the final output to S3 as Parquet.

---

