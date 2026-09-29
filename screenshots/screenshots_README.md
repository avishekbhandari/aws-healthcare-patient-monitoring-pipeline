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

## Screenshot Groups

| Area | What the screenshots should show |
|---|---|
| Source data | Patient vitals, patient details, and device logs used in the project |
| Amazon S3 setup | Raw, processed, and rejected folder structure |
| IAM setup | Roles or permissions used for Glue, S3, and logs |
| Glue Crawler | Crawler setup used to scan raw healthcare files |
| Glue Data Catalog | Healthcare database and catalog tables created from the crawler |
| Glue ETL Job | PySpark job used to clean, transform, and join healthcare data |
| Output data | Final processed report output written to S3 |
| Validation | Evidence that the ETL job ran successfully and created output |

## Source Files Used

The project uses three healthcare source files:

```text
patient_vitals.csv
patient_details.csv
device_logs.csv
```

These files represent patient health readings, patient demographic information, and medical device activity logs.

## Main ETL Script

The main implementation file for the project is:

```text
glue_jobs/healthcare_etl.py
```

The Glue job reads healthcare tables from the Glue Data Catalog, converts Glue DynamicFrames into Spark DataFrames, applies PySpark transformations, creates health-status indicators, joins patient/device datasets, and writes the final output to S3 in Parquet format.

## Expected Output Evidence

The screenshots and project files are included to support the main steps completed in this project:

- healthcare source files were prepared for ingestion
- AWS Glue ETL logic was created using PySpark
- Glue Catalog tables were referenced in the ETL job
- patient vitals, patient details, and device logs were joined
- health status and alert flag fields were created
- processed output was written to S3 in Parquet format

Some screenshots also support AWS console setup steps such as S3, Glue, and Catalog configuration. The current version focuses mainly on the Glue ETL implementation.


