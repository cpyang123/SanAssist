import pandas as pd
from sqlalchemy import create_engine

# Parameters for database setup
csv_file_path = "data/augmented_patient_data.csv"
sqlite_db_path = "data/patient_data.db"
table_name = "patient_data"


def csv_to_sqlite(csv_path, db_path, table_name):
    """
    Convert a CSV file to an SQLite database.
    """
    # Load CSV into a DataFrame
    df = pd.read_csv(csv_path)

    # Create a database connection (SQLite)
    engine = create_engine(f"sqlite:///{db_path}")

    # Write the DataFrame to the SQLite database
    with engine.begin() as connection:
        df.to_sql(table_name, con=connection, if_exists="replace", index=False)

    print(f"Data successfully written to {db_path} in table '{table_name}'.")

# For databricks use databricks_connection_string = "databricks+pyhive://<username>:<password>@<host>/<database>"
# instead of db_path
# Run the function
csv_to_sqlite(csv_file_path, sqlite_db_path, table_name)
