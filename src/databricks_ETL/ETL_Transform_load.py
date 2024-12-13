df = spark.read.csv("dbfs:/data/augmented_patient_data.csv", header=True, inferSchema=True)


original_columns = df.columns
new_columns = [col.lower().replace(" ", "_") for col in original_columns]

column_mapping = dict(zip(original_columns, new_columns))
reverse_column_mapping = dict(zip(new_columns, original_columns))

df = df.toDF(*new_columns)

df.write.format("delta").mode("overwrite").saveAsTable("ids706_data_engineering.sanassist_healthcare.healthcare_data_augmented")

display(df)

