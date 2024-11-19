import pandas as pd
from sqlalchemy import create_engine


def test_database_1():
    sqlite_db_path = "data/patient_data.db"
    table_name = "patient_data"
    # Run the tests
    database_helper(sqlite_db_path, table_name)


def test_data():
    # Load the augmented dataset
    file_path = "data/augmented_patient_data.csv"
    df = pd.read_csv(file_path)
    # Test 1: Check for missing values
    assert (
        df.isnull().sum().sum() == 0
    ), f"Dataset contains missing values:\n{df.isnull().sum()}"

    # Test 2: Validate ranges for synthetic biomarkers
    assert (
        (df["Systolic BP"] >= 90) & (df["Systolic BP"] <= 160)
    ).all(), "Systolic BP out of range"
    assert (
        (df["Diastolic BP"] >= 60) & (df["Diastolic BP"] <= 100)
    ).all(), "Diastolic BP out of range"
    assert (
        (df["Heart Rate"] >= 60) & (df["Heart Rate"] <= 100)
    ).all(), "Heart Rate out of range"
    assert ((df["BMI"] >= 10) & (df["BMI"] <= 50)).all(), "BMI out of range"
    assert ((df["SpO2"] >= 90) & (df["SpO2"] <= 100)).all(), "SpO2 out of range"
    assert (
        (df["Creatinine"] >= 0.1) & (df["Creatinine"] <= 2.0)
    ).all(), "Creatinine out of range"
    assert ((df["CRP"] >= 0.1) & (df["CRP"] <= 10.0)).all(), "CRP out of range"
    assert (
        (df["WBC Count"] >= 4000) & (df["WBC Count"] <= 11000)
    ).all(), "WBC Count out of range"
    assert (
        (df["Hemoglobin"] >= 10) & (df["Hemoglobin"] <= 18)
    ).all(), "Hemoglobin out of range"
    assert ((df["MAP"] >= 50) & (df["MAP"] <= 120)).all(), "MAP out of range"

    # Test 3: Validate data types
    expected_types = {
        "Systolic BP": "int64",
        "Diastolic BP": "int64",
        "Heart Rate": "int64",
        "BMI": "float64",
        "SpO2": "int64",
        "Creatinine": "float64",
        "CRP": "float64",
        "WBC Count": "int64",
        "Hemoglobin": "float64",
        "MAP": "float64",
    }
    for column, expected_type in expected_types.items():
        assert (
            df[column].dtype == expected_type
        ), f"Column {column} has wrong type: {df[column].dtype}, expected {expected_type}"

    # Test 4: Check row count
    assert len(df) > 0, "Dataset is empty"

    # Test 5: Check for duplicate rows
    assert not df.duplicated().any(), "Dataset contains duplicate rows"

    print("All tests passed successfully!")


# Database parameters
def database_helper(db_path, table_name):
    """
    Run tests on the database to validate data integrity.
    """
    # Connect to the SQLite database
    engine = create_engine(f"sqlite:///{db_path}")

    # Load data into a pandas DataFrame for testing
    with engine.connect() as connection:
        df = pd.read_sql_table(table_name, con=connection)

    # Test 1: Check for missing values
    assert (
        df.isnull().sum().sum() == 0
    ), f"Database contains missing values:\n{df.isnull().sum()}"

    # Test 2: Validate ranges for synthetic biomarkers
    assert (
        (df["Systolic BP"] >= 90) & (df["Systolic BP"] <= 160)
    ).all(), "Systolic BP out of range"
    assert (
        (df["Diastolic BP"] >= 60) & (df["Diastolic BP"] <= 100)
    ).all(), "Diastolic BP out of range"
    assert (
        (df["Heart Rate"] >= 60) & (df["Heart Rate"] <= 100)
    ).all(), "Heart Rate out of range"
    assert ((df["BMI"] >= 10) & (df["BMI"] <= 50)).all(), "BMI out of range"
    assert ((df["SpO2"] >= 90) & (df["SpO2"] <= 100)).all(), "SpO2 out of range"
    assert (
        (df["Creatinine"] >= 0.1) & (df["Creatinine"] <= 2.0)
    ).all(), "Creatinine out of range"
    assert ((df["CRP"] >= 0.1) & (df["CRP"] <= 10.0)).all(), "CRP out of range"
    assert (
        (df["WBC Count"] >= 4000) & (df["WBC Count"] <= 11000)
    ).all(), "WBC Count out of range"
    assert (
        (df["Hemoglobin"] >= 10) & (df["Hemoglobin"] <= 18)
    ).all(), "Hemoglobin out of range"
    assert ((df["MAP"] >= 50) & (df["MAP"] <= 120)).all(), "MAP out of range"

    # Test 3: Validate data types
    expected_types = {
        "Systolic BP": "int64",
        "Diastolic BP": "int64",
        "Heart Rate": "int64",
        "BMI": "float64",
        "SpO2": "int64",
        "Creatinine": "float64",
        "CRP": "float64",
        "WBC Count": "int64",
        "Hemoglobin": "float64",
        "MAP": "float64",
    }
    for column, expected_type in expected_types.items():
        actual_type = str(df[column].dtype)
        assert (
            actual_type == expected_type
        ), f"Column {column} has wrong type: {actual_type}, expected {expected_type}"

    # Test 4: Check row count
    assert len(df) > 0, "Database table is empty"

    # Test 5: Check for duplicate rows
    assert not df.duplicated().any(), "Database table contains duplicate rows"

    print("All database tests passed successfully!")


# Run the tests
test_data()
