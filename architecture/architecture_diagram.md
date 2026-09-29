# Architecture Diagram: AWS Healthcare Patient Monitoring Pipeline

## High-Level Architecture

```text
Healthcare Source Files
        |
        v
Amazon S3 Raw Zone
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

## Source Data Flow

The pipeline starts with three healthcare source files:

```text
patient_vitals.csv
patient_details.csv
device_logs.csv
```

These files represent patient health readings, patient demographic information, and medical device activity logs.

## S3 Folder Structure

The planned S3 folder structure is:

```text
raw/vitals/
raw/patients/
raw/devices/
processed/vitals/
processed/patients/
processed/reports/
rejected/
```

The raw folders store incoming files. The processed folders store cleaned and transformed output. The rejected folder is reserved for invalid or bad records.

## Glue Crawler and Data Catalog

AWS Glue Crawler is used to scan the raw healthcare files and create metadata tables in AWS Glue Data Catalog.

Expected catalog tables:

```text
patient_vitals
patient_details
device_logs
```

In the current Glue ETL job, the catalog tables are referenced as:

```text
vitals
patients
devices
```

These represent the same three source datasets.

## Glue ETL Job

The main ETL job is:

```text
glue_jobs/healthcare_etl.py
```

The Glue job performs these steps:

1. Reads source tables from AWS Glue Data Catalog.
2. Converts Glue DynamicFrames into Spark DataFrames.
3. Cleans patient vitals, patient details, and device logs.
4. Creates derived columns such as `health_status`, `alert_flag`, `monitoring_date`, and `monitoring_hour`.
5. Joins patient vitals with patient details.
6. Joins the result with device logs.
7. Writes the final report output to S3 in Parquet format.

## Health Status Transformation

The Glue ETL job creates patient status indicators based on health readings.

| Condition | Status |
|---|---|
| oxygen level below 90 | Critical |
| temperature above 100 | Fever |
| heart rate above 100 | High Risk |
| otherwise | Normal |

The ETL job also creates an `alert_flag` field for records that need attention.

## Output Layer

The final output is written to:

```text
processed/reports/
```

The Glue job writes the final data in Parquet format.

## Main Business Data Flow

```text
patient_vitals.csv
patient_details.csv
device_logs.csv
        |
        v
S3 Raw Folders
        |
        v
Glue Crawler and Data Catalog
        |
        v
Glue PySpark ETL
        |
        v
Joined Patient Monitoring Report
        |
        v
S3 Parquet Output
```

## Monitoring and Future Extension

The current version focuses mainly on the AWS Glue ETL implementation.

Future improvements could include:

- Lambda trigger for new file uploads
- rejected-record movement
- Glue Workflow orchestration
- CloudWatch log documentation
- Athena queries on top of the Parquet output
- data quality count reporting
- parameterized S3 paths
