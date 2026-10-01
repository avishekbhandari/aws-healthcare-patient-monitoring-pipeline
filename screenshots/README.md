# Screenshot Evidence

This folder contains screenshots captured while building and testing the AWS Healthcare Patient Monitoring Pipeline.

The screenshots are included as supporting evidence for the project. They show the project setup, AWS-related steps, source data, Glue components, ETL job work, and output validation.

## Project Flow Covered

```text
Patient Healthcare Source Files
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
Amazon S3 Processed Reports Output
```

## Screenshot Index

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


