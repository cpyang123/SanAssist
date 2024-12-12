from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, when
import random

def augment_data(input_file_path, output_file_path):
    # Create Spark session
    spark = SparkSession.builder.appName("Data Augmentation").getOrCreate()

    # Load CSV file into a Spark DataFrame
    df = spark.read.option("header", True).csv(input_file_path)

    # Convert columns to lowercase where necessary
    df = df.withColumn("Name", col("Name").alias("lower(Name)"))

    # Define ranges for each condition
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
        # Add other conditions with their respective ranges...
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

    # Save the augmented data as a CSV file
    df.write.option("header", True).mode("overwrite").csv(output_file_path)
    print("Data Augmentation Complete. Saved to:", output_file_path)

# Main function
if __name__ == "__main__":
    input_file_path = "/dbfs/data/healthcare_dataset.csv"  # Adjust the path as needed
    output_file_path = "/dbfs/data/augmented_patient_data.csv"
    augment_data(input_file_path, output_file_path)
