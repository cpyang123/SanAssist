import pandas as pd
import numpy as np

def test_data_augmentation():
    # Load the dataset
    file_path = "data/augmented_patient_data.csv"
    df = pd.read_csv(file_path)

    # Test 1: Check if the file was loaded successfully
    assert not df.empty, "The CSV file is empty"

    # Test 2: Check if all expected columns are present
    expected_columns = ["Name", "Medical Condition", "Systolic BP", "Diastolic BP", "Heart Rate", "BMI", "SpO2", "Creatinine", "CRP", "WBC Count", "Hemoglobin"]
    assert all(col in df.columns for col in expected_columns), "Missing expected columns"

    # Test 3: Check if 'Name' column is lowercase
    assert df["Name"].str.islower().all(), "Not all names are in lowercase"

    # Test 4: Check if 'Medical Condition' only contains expected conditions
    expected_conditions = ["Cancer", "Obesity", "Diabetes", "Asthma", "Hypertension", "Arthritis"]
    assert df["Medical Condition"].isin(expected_conditions).all(), "Unexpected medical condition found"

    # Test 5: Check if numeric columns are within expected ranges
    ranges = {
        "Systolic BP": (90, 220),
        "Diastolic BP": (60, 140),
        "Heart Rate": (50, 180),
        "BMI": (15.0, 60.0),
        "SpO2": (70, 97),
        "Creatinine": (0.3, 3.0),
        "CRP": (3.0, 50.0),
        "WBC Count": (3000, 50000),
        "Hemoglobin": (5.0, 16.0),
    }

    for col, (min_val, max_val) in ranges.items():
        assert df[col].between(min_val, max_val).all(), f"{col} contains values outside the expected range"

    # Test 6: Check if there are no null values
    assert not df.isnull().any().any(), "Dataset contains null values"

    # Test 7: Check if integer columns are indeed integers
    integer_columns = ["Systolic BP", "Diastolic BP", "Heart Rate", "SpO2", "WBC Count"]
    for col in integer_columns:
        assert df[col].dtype == np.int64, f"{col} is not of type int64"

    # Test 8: Check if float columns have at most one decimal place
    float_columns = ["BMI", "Creatinine", "CRP", "Hemoglobin"]
    for col in float_columns:
        assert df[col].apply(lambda x: len(str(x).split('.')[-1]) <= 1).all(), f"{col} has values with more than one decimal place"

    print("All tests passed successfully!")

if __name__ == "__main__":
    test_data_augmentation()
