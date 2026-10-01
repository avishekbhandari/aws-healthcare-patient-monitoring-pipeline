# AWS Healthcare Patient Monitoring Pipeline

## About This Project

This project is a hands-on AWS data engineering project based on a patient health monitoring use case.

The scenario is that a hospital receives patient monitoring files from ICU monitoring systems, wearable health devices, hospital management systems, and emergency care systems. The goal is to store incoming data, validate records, clean and transform patient readings, catalog metadata, and write processed healthcare data for reporting.

The project was implemented using Amazon S3, AWS IAM, AWS Glue Crawler, AWS Glue Data Catalog, AWS Glue Studio, PySpark, and Parquet output on Amazon S3.

This is a learning and portfolio project. It is not a production healthcare system.

---

## Project Documentation

| Document | Purpose |
|---|---|
| [Implementation Summary](implementation_summary.md) | Explains what was implemented, current scope, and limitations |
| [Architecture Diagram](architecture/architecture_diagram.md) | Shows the AWS pipeline flow and architecture explanation |
| [Data Dictionary](data/README.md) | Explains the source CSV files, columns, and data quality examples |
| [Screenshot Evidence](screenshots/README.md) | Explains the AWS screenshots and project evidence |
| [Glue ETL Script](glue_jobs/healthcare_etl.py) | Main AWS Glue PySpark ETL implementation |

---

## Business Scenario

A hospital receives patient health monitoring data from multiple systems, including:

- ICU monitoring systems
- wearable health devices
- hospital management systems
- emergency care systems

The hospital needs a data pipeline that can:

- store incoming healthcare files
- validate patient records
- clean and transform patient readings
- detect invalid or critical readings
- catalog metadata automatically
- store processed healthcare data
- prepare reporting output for downstream analysis

---

## AWS Services Used

| Service | Purpose |
|---|---|
| Amazon S3 | Stores raw, processed, and rejected healthcare data |
| AWS IAM | Provides service roles and permissions for Glue and Lambda-related setup |
| AWS Glue Crawler | Crawls raw data and creates catalog tables |
| AWS Glue Data Catalog | Stores database and table metadata |
| AWS Glue Studio | Creates and manages the Glue ETL job |
| AWS Glue PySpark | Cleans, transforms, joins, and writes healthcare data |
| Parquet | Stores final processed output in an analytics-friendly format |

---

## Pipeline Overview

```text
Healthcare Source Files
        |
        v
Amazon S3 Raw Folders
        |
        v
AWS Glue Crawler
        |
        v
AWS Glue Data Catalog
        |
        v
AWS Glue PySpark ETL Job
        |
        v
Processed Patient Monitoring Report
        |
        v
Amazon S3 processed/reports/ Parquet Output
```

---

## S3 Storage Design

The S3 bucket used for this project is:

```text
patient-health-monitoring-avishek-2026
```

The implemented S3 folder structure includes:

```text
raw/
raw/vitals/
raw/patients/
raw/devices/

processed/
processed/vitals/
processed/patients/
processed/reports/

rejected/
```

### Folder Purpose

| Folder | Purpose |
|---|---|
| `raw/vitals/` | Stores raw patient vital readings |
| `raw/patients/` | Stores raw patient details |
| `raw/devices/` | Stores raw device log data |
| `processed/vitals/` | Reserved for processed vitals data |
| `processed/patients/` | Reserved for processed patient data |
| `processed/reports/` | Stores final processed reporting output |
| `rejected/` | Reserved for bad or invalid records |

The `rejected/` folder was created as part of the storage design, but automated rejected-record movement is not implemented in the current version.

---

## IAM Roles

The AWS setup included IAM roles for Glue and Lambda-related workflow support.

### Glue IAM Role

```text
GlueHealthcareETLRole
```

This role was used by AWS Glue for accessing S3, Glue services, and related ETL resources.

### Lambda IAM Role

```text
LambdaHealthcareETLRole
```

This role was created for Lambda-related automation design, such as triggering crawler/job workflows or supporting file-processing automation.


---

## Source Data

The project uses three sample healthcare source files.

```text
patient_vitals.csv
patient_details.csv
device_logs.csv
```

### 1. patient_vitals.csv

Contains patient health readings such as:

- patient ID
- timestamp
- heart rate
- blood pressure
- oxygen level
- temperature

This file includes data quality issues for ETL practice, including:

- missing heart rate
- missing oxygen level
- duplicate patient reading
- critical oxygen reading
- high temperature reading
- high heart rate reading

### 2. patient_details.csv

Contains patient profile information such as:

- patient ID
- patient name
- age
- gender
- city
- disease

### 3. device_logs.csv

Contains device-related information such as:

- device ID
- patient ID
- device type
- device status
- last sync timestamp

---

## Glue Crawler and Data Catalog

The project uses an AWS Glue Crawler to scan raw healthcare data and create Glue Data Catalog tables.

### Glue Database

```text
healthcare_db
```

### Glue Crawler

```text
healthcare-raw-data-crawler
```

### Catalog Tables Created

The implemented Glue Catalog tables are:

```text
vitals
patients
devices
```

---

## Glue ETL Job

The main AWS Glue ETL job is:

```text
healthcare-patient-monitoring-etl-job
```

The main repository script is:

```text
glue_jobs/healthcare_etl.py
```

The Glue job uses PySpark to read data from AWS Glue Data Catalog, clean and transform the data, join related datasets, and write final output to S3 in Parquet format.

---

## ETL Processing Steps

The Glue ETL job performs the following steps:

1. Starts the AWS Glue job context.
2. Reads source tables from AWS Glue Data Catalog.
3. Converts Glue DynamicFrames into Spark DataFrames.
4. Removes duplicate records.
5. Filters records with missing patient IDs.
6. Handles missing heart rate values.
7. Handles missing oxygen level values.
8. Converts timestamp fields.
9. Creates `monitoring_date`.
10. Creates `monitoring_hour`.
11. Creates `health_status`.
12. Creates `alert_flag`.
13. Joins vitals data with patient details.
14. Joins the result with device logs.
15. Selects final reporting columns.
16. Writes final output to Amazon S3 as Parquet.

---

## Data Cleaning Logic

The ETL job applies basic cleaning rules:

- removes duplicate records
- filters records with missing `patient_id`
- replaces missing `heart_rate` values with `0`
- replaces missing `oxygen_level` values with `0`
- converts timestamp strings into timestamp format
- extracts monitoring date
- extracts monitoring hour
- removes duplicate records from patient and device datasets

---

## Health Status Logic

The ETL job creates a `health_status` column using the following rules:

| Condition | Health Status |
|---|---|
| `oxygen_level < 90` | Critical |
| `temperature > 100` | Fever |
| `heart_rate > 100` | High Risk |
| Otherwise | Normal |

The ETL job also creates an `alert_flag` column.

The alert flag is set to `true` when any of the following conditions are met:

- oxygen level is below 90
- temperature is above 100
- heart rate is above 100

Otherwise, the alert flag is set to `false`.

---

## Dataset Join Logic

The ETL job joins the three datasets using `patient_id`.

```text
vitals + patients + devices
```

The final joined report combines:

- patient health readings
- patient profile information
- device information
- derived health status
- alert indicator
- monitoring date and hour

---

## Final Output

The final output is written to:

```text
s3://patient-health-monitoring-avishek-2026/processed/reports/
```

The output format is:

```text
Parquet
```

### Final Output Columns

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

## Screenshot Evidence

The screenshots in the `screenshots/` folder provide evidence of the AWS setup and pipeline execution.

| Screenshot | Evidence Shown |
|---|---|
| `1.png` | S3 bucket list showing `patient-health-monitoring-avishek-2026` |
| `2.png` | S3 bucket root showing `processed/`, `raw/`, and `rejected/` folders |
| `3.png` | `raw/` folder showing `devices/`, `patients/`, and `vitals/` |
| `4.png` | `processed/` folder showing `patients/`, `reports/`, and `vitals/` |
| `5.png` | IAM roles list showing Glue and Lambda-related roles |
| `6.png` | `GlueHealthcareETLRole` with S3 and Glue permissions |
| `7.png` | `LambdaHealthcareETLRole` with S3, Glue, and Lambda permissions |
| `8.png` | Glue database page showing crawler creation and `healthcare_db` |
| `9.png` | Glue crawler list showing `healthcare-raw-data-crawler` |
| `10.png` | Crawler properties showing crawler name, IAM role, database, and ready state |
| `11.png` | Completed crawler run showing table changes |
| `12.png` | Glue database `healthcare_db` with `devices`, `patients`, and `vitals` tables |
| `13.png` | Glue ETL job details for `healthcare-patient-monitoring-etl-job` |
| `14.png` | Glue Studio script editor showing PySpark ETL code |
| `15.png` | S3 `processed/reports/` folder showing Parquet output |

---

## Repository Structure

```text
aws-healthcare-patient-monitoring-pipeline/
|
|-- architecture/
|   |-- architecture_diagram.md
|
|-- data/
|   |-- data_README.md
|   |-- patient_details.csv
|   |-- patient_vitals.csv
|   `-- device_logs.csv
|
|-- glue_jobs/
|   |-- healthcare_etl.py
|
|-- screenshots/
|   |-- screenshots_README.md
|   |-- 1.png
|   |-- 2.png
|   |-- ...
|   `-- 15.png
|
|-- .gitignore
|-- README.md
`-- implementation_summary.md
```

---

## Known Limitations

This project was built as a learning and portfolio project.

Current limitations:

- Lambda IAM role was created, but Lambda function code is not included in this repository.
- The `rejected/` folder was created, but automated rejected-record movement is not implemented.
- The Glue Catalog table names are `vitals`, `patients`, and `devices`, while the project PDF expected `patient_vitals`, `patient_details`, and `device_logs`.
- The dataset is small and sample-based.
- The Glue job uses a hardcoded S3 output path.
- The Glue job writes output using overwrite mode.
- Automated unit tests are not included.
- Infrastructure as Code is not included.

---

## What I Learned

Through this project, I practiced:

- designing a healthcare data pipeline on AWS
- creating S3 bucket folder structures for raw, processed, and rejected data
- configuring IAM roles for Glue and Lambda-related setup
- creating and running an AWS Glue Crawler
- working with AWS Glue Data Catalog
- creating AWS Glue Studio ETL jobs
- writing PySpark transformations
- cleaning healthcare data
- joining multiple datasets
- creating derived health indicators
- writing output to S3 in Parquet format
- documenting a data engineering project for GitHub

---

