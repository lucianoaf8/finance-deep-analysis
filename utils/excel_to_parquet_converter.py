# utils/excel_to_parquet_converter.py

import pandas as pd

# Load the Excel file
excel_path = 'c:\\Projects\\finance-deep-analysis\\data_integration\\normalized_encoded_data.xlsx'
data = pd.read_excel(excel_path)

# Save as Parquet
parquet_path = 'c:\\Projects\\finance-deep-analysis\\data_integration\\normalized_encoded_data.parquet'
data.to_parquet(parquet_path, index=False)

print("Converted Excel file to Parquet format successfully.")
