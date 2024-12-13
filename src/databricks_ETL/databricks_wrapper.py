import requests
import time
import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

load_dotenv()

# Databricks details
databricks_url = os.environ.get("SERVER_HOST")
token = os.environ.get("DATABRICKS_ACCESS_TOKEN")
job_id = os.environ.get("JOB_ID")

# Start job
start_job_url = f"https://{databricks_url}/api/2.1/jobs/run-now"
headers = {"Authorization": f"Bearer {token}"}
payload = {"job_id": job_id}

response = requests.post(start_job_url, headers=headers, json=payload, timeout=20)
if response.status_code == 200:
    RUN_ID = response.json().get("run_id")
    print(f"Job started successfully. Run ID: {RUN_ID}")
else:
    print(f"Error starting job: {response.text}")
    exit(1)


# Monitor job
def monitor_job(run_id):
    get_status_url = f"https://{databricks_url}/api/2.1/jobs/runs/get"
    while True:
        time.sleep(30)  # Poll every 30 seconds
        status_response = requests.get(
            get_status_url, headers=headers, params={"run_id": run_id}, timeout=20
        )
        if status_response.status_code == 200:
            state = status_response.json().get("state").get("life_cycle_state")
            print(f"Job status: {state}")
            if state == "TERMINATED":
                result_state = status_response.json().get("state").get("result_state")
                print(f"Job finished with result state: {result_state}")
                return result_state
            elif state in ["INTERNAL_ERROR", "SKIPPED", "FAILED"]:
                print(f"Job failed with state: {state}")
                return state
        else:
            print(f"Error fetching job status: {status_response.text}")
            return "ERROR"


# Check job status
job_status = monitor_job(RUN_ID)
if job_status == "SUCCESS":
    print("Job completed successfully!")
else:
    print("Job did not complete successfully.")


# Databricks settings
DATABRICKS_INSTANCE = databricks_url  # Update with your Databricks URL
DATABRICKS_TOKEN = token
TABLE_NAME = "ids706_data_engineering.sanassist_healthcare.healthcare_data_augmented"  # Update with your table name

# Query to export the table
QUERY = f"SELECT * FROM {TABLE_NAME}"

# Headers for API authentication
headers = {
    "Authorization": f"Bearer {DATABRICKS_TOKEN}",
    "Content-Type": "application/json",
}

# Run the query
response = requests.post(
    f"{DATABRICKS_INSTANCE}/api/2.0/sql/statements",
    json={"statement": QUERY},
    headers=headers,
)

# Check the response
if response.status_code != 200:
    print("Error:", response.json())
    exit()

# Extract the results
result = response.json()
statement_id = result["statement_id"]

# Poll the API for the query result
result_url = f"{DATABRICKS_INSTANCE}/api/2.0/sql/statements/{statement_id}/result"
while True:
    result_response = requests.get(result_url, headers=headers)
    result_data = result_response.json()
    if result_data.get("status") == "SUCCEEDED":
        break
    elif result_data.get("status") == "FAILED":
        print("Query failed:", result_data)
        exit()

# Get rows from the response
rows = result_data.get("result", {}).get("rows", [])
columns = result_data.get("result", {}).get("columns", [])

# Convert rows and columns to a Pandas DataFrame
column_names = [col["name"] for col in columns]
df = pd.DataFrame(rows, columns=column_names)

# Replace underscores with spaces in column names
df.columns = df.columns.str.replace("_", " ")

# Display the DataFrame
print(df)


sqlite_db_path = "data/patient_data_test.db"
table_name = "patient_data"

# Create a database connection (SQLite)
engine = create_engine(f"sqlite:///{db_path}")

# Write the DataFrame to the SQLite database
with engine.begin() as connection:
    df.to_sql(table_name, con=connection, if_exists="replace", index=False)
