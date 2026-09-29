# AWS Healthcare Patient Monitoring Pipeline

## About This Project

This project is a hands-on AWS data engineering project built around a patient health monitoring use case.

The project scenario is that a hospital receives patient monitoring files from ICU monitoring systems, wearable health devices, hospital management systems, and emergency care systems. The goal is to store patient data, validate incoming records, clean and transform health readings, catalog metadata, and write processed healthcare data for reporting.

I built the main ETL part of the pipeline using AWS Glue, PySpark, AWS Glue Data Catalog, and Amazon S3.

---

## Business Scenario

A hospital receives patient health monitoring files that include:

- patient vital readings
- patient demographic details
- medical device logs

The hospital wants to:

- ingest patient data
- validate incoming files
- clean medical records
- detect invalid patient readings
- store transformed healthcare data
- separate or identify bad records
- prepare patient monitoring data for reporting

---

## Pipeline Overview

```text
Source Healthcare Files
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
Cleaned and Transformed Patient Monitoring Data
        |
        v
Amazon S3 Processed Reports Folder
```

---

## Technologies Used

- AWS Glue
- AWS Glue Data Catalog
- Amazon S3
- PySpark
- Python
- Parquet
- Git and GitHub

---

## Source Data

The project uses three healthcare datasets:

```text
patient_vitals.csv
patient_details.csv
device_logs.csv
```

### Patient Vitals

Contains patient health readings such as:

- patient ID
- timestamp
- heart rate
- blood pressure
- oxygen level
- temperature

### Patient Details

Contains patient information such as:

- patient ID
- name
- age
- gender
- city
- disease

### Device Logs

Contains device information such as:

- device ID
- patient ID
- device type
- device status
- last sync time

---

## S3 Folder Design

The expected S3 folder structure for this project is:

```text
raw/vitals/
raw/patients/
raw/devices/
processed/vitals/
processed/patients/
processed/reports/
rejected/
```

The raw folders store incoming patient data. The processed folders store cleaned and transformed data. The rejected folder is intended for bad or invalid records.

---

## AWS Glue Data Catalog

The project uses AWS Glue Data Catalog to store metadata for the healthcare datasets.

The expected catalog tables are based on:

```text
patient_vitals
patient_details
device_logs
```

In the Glue ETL job, I worked with catalog tables named:

```text
vitals
patients
devices
```

These tables represent the same three source datasets used in the patient monitoring pipeline.

---

## Main Glue ETL Job

The main ETL script is:

```text
glue_jobs/healthcare_etl.py
```

This Glue job performs the following steps:

1. Reads catalog tables using AWS Glue.
2. Converts Glue DynamicFrames into Spark DataFrames.
3. Cleans patient vitals data.
4. Cleans patient details and device logs.
5. Creates health status and alert indicators.
6. Joins vitals, patient, and device data.
7. Selects the final reporting columns.
8. Writes the final output to Amazon S3 in Parquet format.

---

## Data Cleaning Steps

The ETL job applies basic cleaning logic, including:

- removing duplicate records
- filtering records with missing patient IDs
- handling missing heart rate values
- handling missing oxygen level values
- converting timestamp fields
- creating monitoring date
- creating monitoring hour
- cleaning patient and device records

---

## Health Status Logic

The project creates a `health_status` column based on patient readings.

| Condition | Health Status |
|---|---|
| oxygen level below 90 | Critical |
| temperature above 100 | Fever |
| heart rate above 100 | High Risk |
| otherwise | Normal |

The project also creates an `alert_flag` column.

The alert flag is set to `true` when any of these conditions are met:

- oxygen level is below 90
- temperature is above 100
- heart rate is above 100

Otherwise, the alert flag is set to `false`.

---

## Dataset Join Logic

The Glue job joins three datasets:

```text
patient vitals
patient details
device logs
```

The final joined dataset provides a patient monitoring report with health readings, patient information, device information, and derived health indicators.

---

## Final Output

The final output includes:

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

The transformed data is written to S3 in Parquet format.

Output path used in the Glue job:

```text
s3://patient-health-monitoring-avishek-2026/processed/reports/
```

---

## Repository Structure

```text
aws-healthcare-patient-monitoring-pipeline/
|
|-- architecture/
|   `-- architecture notes or diagrams
|
|-- data/
|   |-- patient_details.csv
|   |-- patient_vitals.csv
|   `-- device_logs.csv
|
|-- screenshots/
|   `-- project screenshots
|
|-- glue_jobs/
|   `-- healthcare_etl.py
|
|-- lambda/
|   `-- placeholder for future Lambda work
|
|-- scripts/
|   `-- placeholder for helper scripts
|
|-- README.md
`-- .gitignore
```

---

## Project Evidence

This repository includes:

- sample healthcare source files
- AWS Glue ETL script
- PySpark transformation logic
- project screenshots in the `screenshots` folder
- folder structure for architecture, data, Glue jobs, Lambda, and scripts

The main implementation file is:

```text
glue_jobs/healthcare_etl.py
```

---

## What I Learned

While building this project, I practiced:

- organizing a healthcare data engineering project
- using AWS Glue job structure
- reading tables from AWS Glue Data Catalog
- converting Glue DynamicFrames into Spark DataFrames
- cleaning healthcare data with PySpark
- joining multiple datasets
- creating derived health indicators
- writing transformed output as Parquet
- using Amazon S3 as a storage layer

This project helped me understand how AWS Glue and PySpark can be used to process healthcare monitoring data.

---

## Known Limitations

This project was built as a learning and portfolio project, so the scope is focused.

Some limitations of the current version are:

- The datasets are small sample files.
- The project focuses mainly on the AWS Glue ETL job.
- The Lambda folder is included as a placeholder, but Lambda automation is not implemented in the current version.
- The script writes the final output using overwrite mode.
- Automated data quality reporting is not yet included.
- CloudWatch monitoring details are not documented yet.
- The project does not currently include automated tests.

These are areas I would improve in a future version.

---

## Future Improvements

If I continue improving this project, I would like to:

- add a simple architecture diagram
- add a screenshot index for the `docs` folder
- document the Glue crawler setup
- add CloudWatch monitoring notes
- add rejected-record handling documentation
- add data quality count checks
- parameterize the S3 input and output paths
- add Lambda or Glue Workflow orchestration
- add Athena queries for reporting on the processed Parquet output

---

