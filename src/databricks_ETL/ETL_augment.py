from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, when, lower
import random


def augment_data(input_file_path, output_file_path):
    # Create Spark session
    spark = SparkSession.builder.appName("Data Augmentation").getOrCreate()

    # Load CSV file into a Spark DataFrame
    df = spark.read.option("header", True).csv(input_file_path)

    # Convert the "Name" column to lowercase
    df = df.withColumn("Name", lower(col("Name").cast("string")))

    # Ensure all required columns exist
    required_columns = [
        "Systolic BP",
        "Diastolic BP",
        "Heart Rate",
        "BMI",
        "SpO2",
        "Creatinine",
        "CRP",
        "WBC Count",
        "Hemoglobin",
        "Medical Condition",
    ]
    for col_name in required_columns:
        if col_name not in df.columns:
            df = df.withColumn(col_name, lit(None).cast("string"))

    # Updated ranges for each condition
    ranges = {
        "Cancer": {
            "Systolic BP": (100, 180),
            "Diastolic BP": (60, 100),
            "Heart Rate": (50, 140),
            "BMI": (15.0, 40.0),
            "SpO2": (85, 95),
            "Creatinine": (0.3, 3.0),
            "CRP": (5.0, 50.0),
            "WBC Count": (3000, 50000),
            "Hemoglobin": (5.0, 14.0),
        },
        "Obesity": {
            "Systolic BP": (130, 200),
            "Diastolic BP": (90, 130),
            "Heart Rate": (80, 150),
            "BMI": (35.0, 60.0),
            "SpO2": (85, 95),
            "Creatinine": (0.8, 2.0),
            "CRP": (10.0, 50.0),
            "WBC Count": (5000, 20000),
            "Hemoglobin": (10.0, 16.0),
        },
        "Diabetes": {
            "Systolic BP": (140, 200),
            "Diastolic BP": (90, 120),
            "Heart Rate": (60, 120),
            "BMI": (25.0, 50.0),
            "SpO2": (80, 95),
            "Creatinine": (1.0, 3.0),
            "CRP": (5.0, 40.0),
            "WBC Count": (5000, 25000),
            "Hemoglobin": (6.0, 12.0),
        },
        "Asthma": {
            "Systolic BP": (90, 140),
            "Diastolic BP": (60, 90),
            "Heart Rate": (80, 180),
            "BMI": (18.0, 40.0),
            "SpO2": (70, 92),
            "Creatinine": (0.5, 1.5),
            "CRP": (3.0, 20.0),
            "WBC Count": (4000, 15000),
            "Hemoglobin": (8.0, 14.0),
        },
        "Hypertension": {
            "Systolic BP": (160, 220),
            "Diastolic BP": (100, 140),
            "Heart Rate": (70, 110),
            "BMI": (25.0, 45.0),
            "SpO2": (90, 97),
            "Creatinine": (1.0, 2.5),
            "CRP": (3.0, 20.0),
            "WBC Count": (5000, 15000),
            "Hemoglobin": (10.0, 16.0),
        },
        "Arthritis": {
            "Systolic BP": (110, 160),
            "Diastolic BP": (70, 100),
            "Heart Rate": (60, 100),
            "BMI": (18.0, 35.0),
            "SpO2": (85, 95),
            "Creatinine": (0.5, 1.5),
            "CRP": (10.0, 40.0),
            "WBC Count": (4000, 12000),
            "Hemoglobin": (8.0, 14.0),
        },
    }

    # Function to generate random values within a range
    def generate_random_values(low, high, dtype="float"):
        if dtype == "float":
            return round(random.uniform(low, high), 1)
        elif dtype == "int":
            return random.randint(low, high)

    # Augment the data for each condition
    for condition, cols in ranges.items():
        for col_name, (low, high) in cols.items():
            dtype = "float" if isinstance(low, float) else "int"
            df = df.withColumn(
                col_name,
                when(
                    col("Medical Condition") == condition,
                    lit(generate_random_values(low, high, dtype)),
                ).otherwise(col(col_name)),
            )

    # Cast integer columns to int
    integer_columns = ["Systolic BP", "Diastolic BP", "Heart Rate", "SpO2", "WBC Count"]
    for col_name in integer_columns:
        df = df.withColumn(col_name, col(col_name).cast("int"))

    # Coalesce to a single partition to create a single CSV file
    df = df.coalesce(1)

    # Save the augmented data as a single CSV file
    df.write.option("header", True).mode("overwrite").csv(output_file_path)
    print("Data Augmentation Complete. Saved to:", output_file_path)


# Main function
if __name__ == "__main__":
    # Copy the file to DBFS
    dbutils.fs.cp(
        "file:/Workspace/Users/mh720@duke.edu/SanAssist/src/databricks_ETL/data/healthcare_dataset.csv",
        "dbfs:/data/healthcare_dataset.csv",
    )

    # Verify input file exists
    display(dbutils.fs.ls("dbfs:/data/"))

    # Define input and output paths
    input_file_path = "dbfs:/data/healthcare_dataset.csv"
    output_file_path = "dbfs:/data/augmented_patient_data"

    # Run the augmentation process
    augment_data(input_file_path, output_file_path)

    # Identify the output part file and copy it back to the workspace
    files = dbutils.fs.ls(output_file_path)
    for file in files:
        if file.name.startswith("part-"):
            dbutils.fs.cp(
                file.path,
                "file:/Workspace/Users/mh720@duke.edu/SanAssist/src/databricks_ETL/data/augmented_patient_data.csv",
            )
            break

    # Verify the file exists in the workspace path
    print("File copied to the workspace path:")
    display(
        dbutils.fs.ls(
            "file:/Workspace/Users/mh720@duke.edu/SanAssist/src/databricks_ETL/data/"
        )
    )
