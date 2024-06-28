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
from utils.progress_logger import ProgressLogger

logger = setup_logging('normalize_encode')

def normalize_and_encode(data, progress):
    """Normalize numerical data and encode categorical variables."""
    logger.info("Starting data normalization and encoding process")
    
    try:
        progress.update(1, "Normalizing numerical data")
        # Select numerical columns for normalization
        numerical_cols = data.select_dtypes(include=['float64', 'int64']).columns
        # Replace inf values with NaN and then fill NaN values with 0
        data[numerical_cols] = data[numerical_cols].replace([np.inf, -np.inf], np.nan).fillna(0)
        
        scaler = StandardScaler()
        data[numerical_cols] = scaler.fit_transform(data[numerical_cols])
        logger.info("Normalized numerical data")
        
        progress.update(1, "Encoding categorical data")
        # Select categorical columns for encoding and ensure they are strings
        categorical_cols = data.select_dtypes(include=['object']).columns
        data[categorical_cols] = data[categorical_cols].astype(str)
        encoder = OneHotEncoder(sparse_output=False, drop='first')
        encoded_data = pd.DataFrame(encoder.fit_transform(data[categorical_cols]))
        encoded_data.columns = encoder.get_feature_names_out(categorical_cols)
        logger.info("Encoded categorical data")
        
        progress.update(1, "Concatenating data")
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

        # Initialize progress logger
        progress = ProgressLogger(total_steps=5)
        
        if os.path.exists(combined_data_path):
            progress.update(1, "Loading data")
            data = pd.read_excel(combined_data_path)
                
            normalized_encoded_data = normalize_and_encode(data, progress)
            
            progress.update(1, "Saving data")
            # Save the normalized and encoded data
            normalized_encoded_data.to_excel(normalized_encoded_data_path, index=False)
            logger.info(f"Saved normalized and encoded data to {normalized_encoded_data_path}")
            print(f"Saved normalized and encoded data to {normalized_encoded_data_path}")

            logger.info("Successfully normalized and encoded data")
            print("Successfully normalized and encoded data")
            progress.finish()
            sys.exit(0)  # Ensure the script exits properly
        else:
            logger.error(f"Combined data file not found at {combined_data_path}")
            print(f"Combined data file not found at {combined_data_path}")
            progress.finish()
            sys.exit(1)  # Exit with an error code if the file is not found
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)  # Exit with an error code if an exception is raised