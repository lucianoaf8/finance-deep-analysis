# data_preprocessing\normalize_encode.py

import os
import sys
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import numpy as np

# Add the project directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utils.logging_setup import setup_logging

logger = setup_logging('normalize_encode')

def normalize_and_encode(data):
    """Normalize numerical data and encode categorical variables."""
    logger.info("Starting data normalization and encoding process")
    
    try:
        print("Normalizing numerical data...")
        logger.info("Normalizing numerical data...")
        # Select numerical columns for normalization
        numerical_cols = data.select_dtypes(include=['float64', 'int64']).columns
        # Replace inf values with NaN and then fill NaN values with 0
        data[numerical_cols] = data[numerical_cols].replace([np.inf, -np.inf], np.nan).fillna(0)
        
        scaler = StandardScaler()
        data[numerical_cols] = scaler.fit_transform(data[numerical_cols])
        logger.info("Normalized numerical data")
        
        print("Encoding categorical data...")
        logger.info("Encoding categorical data...")
        # Select categorical columns for encoding and ensure they are strings
        categorical_cols = data.select_dtypes(include=['object']).columns
        data[categorical_cols] = data[categorical_cols].astype(str)
        encoder = OneHotEncoder(sparse_output=False, drop='first')
        encoded_data = pd.DataFrame(encoder.fit_transform(data[categorical_cols]))
        encoded_data.columns = encoder.get_feature_names_out(categorical_cols)
        logger.info("Encoded categorical data")
        
        print("Concatenating data...")
        logger.info("Concatenating data...")
        # Concatenate the normalized and encoded data
        data = pd.concat([data, encoded_data], axis=1)
        data.drop(columns=categorical_cols, inplace=True)
        logger.info("Concatenated normalized and encoded data")
        
        logger.info("Data normalization and encoding process completed successfully")
        print("Data normalization and encoding process completed successfully")
        return data
    
    except Exception as e:
        logger.error(f"Error during data normalization and encoding: {e}")
        print(f"Error during data normalization and encoding: {e}")
        raise

if __name__ == '__main__':
    # Test data normalization and encoding
    try:
        combined_data_path = os.path.join(project_root, 'data_integration', 'combined_data.xlsx')
        normalized_encoded_data_path = os.path.join(project_root, 'data_integration', 'normalized_encoded_data.xlsx')

        if os.path.exists(combined_data_path):
            print("Loading data...")
            logger.info("Loading data...")
            data = pd.read_excel(combined_data_path)

            # Ensure income and expense columns are included
            if 'income' not in data.columns:
                logger.warning("Income column is missing from the data, creating a dummy column")
                data['income'] = 0  # Replace with appropriate logic
            
            if 'expense' not in data.columns:
                logger.warning("Expense column is missing from the data, creating a dummy column")
                data['expense'] = 0  # Replace with appropriate logic
                
            normalized_encoded_data = normalize_and_encode(data)
            
            print("Saving data...")
            logger.info("Saving data...")
            try:
                chunk_size = 500
                total_chunks = (len(normalized_encoded_data) // chunk_size) + 1
                with pd.ExcelWriter(normalized_encoded_data_path, engine='xlsxwriter') as writer:
                    for i in range(0, len(normalized_encoded_data), chunk_size):
                        chunk_number = (i // chunk_size) + 1
                        logger.info(f"Saving chunk {chunk_number}/{total_chunks}")
                        print(f"Saving chunk {chunk_number}/{total_chunks}")
                        startrow = i if i == 0 else i + 1
                        normalized_encoded_data.iloc[i:i + chunk_size].to_excel(writer, index=False, startrow=startrow, header=i==0)
                logger.info(f"Saved normalized and encoded data to {normalized_encoded_data_path}")
                print(f"Saved normalized and encoded data to {normalized_encoded_data_path}")
            except Exception as e:
                logger.error(f"Error while saving data: {e}")
                print(f"Error while saving data: {e}")
                raise

            logger.info("Successfully normalized and encoded data")
            print("Successfully normalized and encoded data")
            sys.exit(0)  # Ensure the script exits properly
        else:
            logger.error(f"Combined data file not found at {combined_data_path}")
            print(f"Combined data file not found at {combined_data_path}")
            sys.exit(1)  # Exit with an error code if the file is not found
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)  # Exit with an error code if an exception is raised
