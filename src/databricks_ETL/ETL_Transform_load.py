from pyspark.sql import SparkSession


def csv_to_delta(input_file_path, delta_table_path):
    # Create Spark session
    spark = SparkSession.builder.appName("CSV to Delta").getOrCreate()

    # Load augmented data into a Spark DataFrame
    augmented_df = spark.read.option("header", True).csv(input_file_path)

    # Save DataFrame to a Delta table
    augmented_df.write.format("delta").mode("overwrite").save(delta_table_path)
    print("Data successfully written to Delta table at:", delta_table_path)

    # Register the Delta table in the Databricks metastore (optional)
    spark.sql(
        f"""
    CREATE TABLE IF NOT EXISTS patient_data
    USING DELTA
    LOCATION '{delta_table_path}'
    """
    )


# Main function
if __name__ == "__main__":
    input_file_path = (
        "/dbfs/data/augmented_patient_data.csv"  # Adjust the path as needed
    )
    delta_table_path = (
        "/mnt/delta/patient_data"  # Adjust the Delta table path as needed
    )
    csv_to_delta(input_file_path, delta_table_path)
