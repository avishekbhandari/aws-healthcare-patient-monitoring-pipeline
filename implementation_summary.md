# Implementation Summary

## Project Name

AWS Healthcare Patient Monitoring Pipeline

## Purpose

This project demonstrates a basic AWS data engineering workflow for patient health monitoring data.

The goal of the project is to process healthcare source files, clean patient monitoring records, join related datasets, create health-status indicators, and write the processed output to Amazon S3 in Parquet format.

This is a portfolio and learning project focused mainly on AWS Glue, PySpark, AWS Glue Data Catalog, and Amazon S3.

---

## What Was Implemented

The current implementation includes:

- S3 bucket and healthcare folder structure
- raw, processed, and rejected storage zones
- Glue IAM role setup
- Lambda IAM role setup
- AWS Glue Crawler
- AWS Glue Data Catalog database: `healthcare_db`
- Glue Catalog tables: `vitals`, `patients`, and `devices`
- AWS Glue Studio ETL job
- PySpark ETL script
- data cleaning logic
- health status and alert flag logic
- joins between vitals, patients, and devices
- final reporting column selection
- Parquet output written to S3
- screenshot evidence
- architecture documentation
- data dictionary

---

## Source Data

The project uses three source files:

```text
patient_vitals.csv
patient_details.csv
device_logs.csv
```

### patient_vitals.csv

This file contains patient monitoring readings such as:

- patient ID
- timestamp
- heart rate
- blood pressure
- oxygen level
- temperature

### patient_details.csv

This file contains patient profile information such as:

- patient ID
- patient name
- age
- gender
- city
- disease

### device_logs.csv

This file contains medical device information such as:

- device ID
- patient ID
- device type
- device status
- last sync time

---

## Main ETL File

The main implementation file is:

```text
glue_jobs/healthcare_etl.py
```

This file contains the AWS Glue PySpark job used to process the healthcare datasets.

---

## Glue Catalog Usage

The Glue ETL job reads data from the AWS Glue Data Catalog.

The current job references these catalog tables:

```text
vitals
patients
devices
```

These tables represent the patient vitals, patient details, and device logs datasets.

---

## ETL Processing Steps

The Glue job performs these main steps:

1. Starts the AWS Glue job context.
2. Reads source tables from the Glue Data Catalog.
3. Converts Glue DynamicFrames into Spark DataFrames.
4. Cleans patient vitals records.
5. Cleans patient details records.
6. Cleans device log records.
7. Creates health-status indicators.
8. Creates an alert flag.
9. Joins vitals data with patient details.
10. Joins the result with device logs.
11. Selects final reporting columns.
12. Writes the final output to S3 as Parquet.

---

## Data Cleaning Logic

The ETL job applies basic data cleaning rules:

- removes duplicate records
- filters out records with missing patient IDs
- replaces missing heart rate values with `0`
- replaces missing oxygen level values with `0`
- converts timestamp values into timestamp format
- creates a monitoring date column
- creates a monitoring hour column
- cleans duplicate records from patient and device datasets

---

## Health Status Logic

The project creates a `health_status` column using patient health readings.

| Condition | Output Status |
|---|---|
| oxygen level below 90 | Critical |
| temperature above 100 | Fever |
| heart rate above 100 | High Risk |
| otherwise | Normal |

The project also creates an `alert_flag` column.

The alert flag is set to `true` when any of these conditions are found:

- oxygen level is below 90
- temperature is above 100
- heart rate is above 100

Otherwise, the alert flag is set to `false`.

---

## Final Output Columns

The final output includes these fields:

```text
patient_id
patient_name
disease
heart_rate
oxygen_level
temperature
health_status
alert_flag
device_type
monitoring_date
monitoring_hour
```

---

## Output Location

The Glue job writes the final output as Parquet to:

```text
s3://patient-health-monitoring-avishek-2026/processed/reports/
```

---

## Current Limitations

This project is intentionally limited in scope.

Known limitations:

- the dataset is small and sample-based
- Lambda automation is not implemented in code
- rejected-record movement is not implemented in code
- - Glue Crawler was created through the AWS console, but Infrastructure as Code is not included
- CloudWatch monitoring is not fully documented
- there are no automated unit tests
- S3 paths are hardcoded in the Glue job
- the job uses overwrite mode for output

---


