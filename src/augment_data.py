import pandas as pd
import numpy as np

# Load the dataset
file_path = "data/healthcare_dataset.csv"
df = pd.read_csv(file_path)
df["Name"] = df["Name"].str.lower()

# Preview the original dataset
print("Original Data Shape:", df.shape)
print(df.head())

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

# Generate all masks at once
condition_masks = {condition: df["Medical Condition"] == condition for condition in ranges.keys()}
print("for condition", condition_masks.keys())
# Apply values for each condition
for condition, mask in condition_masks.items():
    num_rows = mask.sum()
    if num_rows > 0:  # Only process if there are rows for the condition
        for col, (low, high) in ranges[condition].items():
            if isinstance(low, float):  # Continuous values
                df.loc[mask, col] = np.round(np.random.uniform(low, high, num_rows), 1)
            else:  # Integer values
                df.loc[mask, col] = np.random.randint(low, high, num_rows)

# Ensure integer columns are of type int64
integer_columns = ["Systolic BP", "Diastolic BP", "Heart Rate", "SpO2", "WBC Count"]
for col in integer_columns:
    df[col] = df[col].astype(np.int64)

# Save the augmented data to a new CSV
output_path = "data/augmented_patient_data.csv"
df.to_csv(output_path, index=False)

print("\nData Augmentation Complete. Augmented data saved to:", output_path)
print("\nPreview of Augmented Data:")
print(df.head())