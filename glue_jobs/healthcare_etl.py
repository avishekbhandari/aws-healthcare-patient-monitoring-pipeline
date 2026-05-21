import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import *

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)


DATABASE_NAME = "healthcare_db"
OUTPUT_PATH = "s3://patient-health-monitoring-avishek-2026/processed/reports/"

# Read Glue Catalog tables
vitals_dynamic_frame = glueContext.create_dynamic_frame.from_catalog(
    database=DATABASE_NAME,
    table_name="vitals"
)

patients_dynamic_frame = glueContext.create_dynamic_frame.from_catalog(
    database=DATABASE_NAME,
    table_name="patients"
)

devices_dynamic_frame = glueContext.create_dynamic_frame.from_catalog(
    database=DATABASE_NAME,
    table_name="devices"
)

# Convert DynamicFrames to Spark DataFrames
vitals_df = vitals_dynamic_frame.toDF()
patients_df = patients_dynamic_frame.toDF()
devices_df = devices_dynamic_frame.toDF()


#Cleans vitals DataFrame

clean_vitals_df = (vitals_df
.dropDuplicates()
.filter(col("patient_id").isNotNull())
.withColumn("heart_rate", when(col("heart_rate").isNull(), lit(0)).otherwise(col("heart_rate")))
.withColumn("oxygen_level", when(col("oxygen_level").isNull(), lit(0)).otherwise(col("oxygen_level")))
.withColumn("timestamp_converted", to_timestamp(col("timestamp"), "M/d/yyyy H:mm"))
.withColumn("monitoring_date", to_date(col("timestamp_converted")))
.withColumn("monitoring_hour", hour(col("timestamp_converted")))
)

#cleans patients and devices DataFrame

clean_patients_df = patients_df.dropDuplicates().filter(col("patient_id").isNotNull())

clean_devices_df = (devices_df.dropDuplicates()
.filter(col("patient_id").isNotNull())
.withColumn("last_sync", to_timestamp(col("last_sync"), "yyyy-MM-dd HH:mm:ss"))
)

# adds health status and alert flag column based on condition
vitals_transformed_df = (
    clean_vitals_df
    .withColumn(
        "health_status",
        when(col("oxygen_level") < 90, "Critical")
        .when(col("temperature") > 100, "Fever")
        .when(col("heart_rate") > 100, "High Risk")
        .otherwise("Normal")
    )
    .withColumn(
        "alert_flag",
        when(
            (col("oxygen_level") < 90) |
            (col("temperature") > 100) |
            (col("heart_rate") > 100),
            lit(True)
        ).otherwise(lit(False))
    )
)

patient_vitals_df = vitals_transformed_df.join(
    clean_patients_df,
    on="patient_id",
    how="inner"
)

# Join with device logs
final_df = patient_vitals_df.join(
    clean_devices_df,
    on="patient_id",
    how="left"
)

# Replace missing device information
final_df = final_df.fillna({
    "device_type": "No Device"
})

# Select final report columns
final_output_df = final_df.select(
    col("patient_id"),
    col("name").alias("patient_name"),
    col("disease"),
    col("heart_rate"),
    col("oxygen_level"),
    col("temperature"),
    col("health_status"),
    col("alert_flag"),
    col("device_type"),
    col("monitoring_date"),
    col("monitoring_hour")
)

# Write final output as Parquet format in S3
final_output_df.write.mode("overwrite").parquet(OUTPUT_PATH)

job.commit()