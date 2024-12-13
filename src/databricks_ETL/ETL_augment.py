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

    # Save the augmented data as a CSV file
    df.write.option("header", True).mode("overwrite").csv(output_file_path)
    print("Data Augmentation Complete. Saved to:", output_file_path)

# Main function
if __name__ == "__main__":
    input_file_path = "/dbfs/data/healthcare_dataset.csv"  # Adjust the path as needed
    output_file_path = "/dbfs/data/augmented_patient_data.csv"
    augment_data(input_file_path, output_file_path)
