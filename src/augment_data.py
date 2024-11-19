import pandas as pd
import numpy as np

# Load the dataset
file_path = "data/healthcare_dataset.csv"
df = pd.read_csv(file_path)
df["Name"] = df["Name"].str.lower()

# Preview the original dataset
print("Original Data Shape:", df.shape)


# Function to generate synthetic biomarkers
def augment_data(df):
    np.random.seed(42)  # Ensure reproducibility
    # Blood pressure (Systolic/Diastolic)
    df["Systolic BP"] = np.random.randint(90, 160, size=len(df))  # mmHg
    df["Diastolic BP"] = np.random.randint(60, 100, size=len(df))  # mmHg

    # Heart rate
    df["Heart Rate"] = np.random.randint(60, 100, size=len(df))  # bpm

    # BMI (Body Mass Index)
    df["BMI"] = np.round(np.random.uniform(18.5, 35.0, size=len(df)), 1)  # kg/m²

    # Oxygen Saturation (SpO2)
    df["SpO2"] = np.random.randint(90, 100, size=len(df))  # Percentage

    # Random blood biomarkers
    df["Creatinine"] = np.round(np.random.uniform(0.5, 1.5, size=len(df)), 2)  # mg/dL
    df["CRP"] = np.round(np.random.uniform(0.1, 10.0, size=len(df)), 2)  # mg/L
    df["WBC Count"] = np.random.randint(4000, 11000, size=len(df))  # cells/µL
    df["Hemoglobin"] = np.round(np.random.uniform(11.0, 16.0, size=len(df)), 1)  # g/dL

    # Generate MAP from BP
    df["MAP"] = np.round((df["Systolic BP"] + 2 * df["Diastolic BP"]) / 3, 1)  # mmHg

    return df


# Augment the data
df_augmented = augment_data(df)
# Save the augmented data to a new CSV
output_path = "data/augmented_patient_data.csv"
df_augmented.to_csv(output_path, index=False)

print("\nData Augmentation Complete. Augmented data saved to:", output_path)
print("\nPreview of Augmented Data:")
print(df_augmented.head())
