# C:\Projects\finance-deep-analysis\data_extraction\clean_data.py

import os
import sys

# Add the project directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utils.logging_setup import setup_logging
from data_extraction.extract_data import extract_data

logger = setup_logging('clean_data')

def clean_data(dataframes):
    """Clean the extracted data."""
    logger.info("Starting data cleaning process")
    
    try:
        for name, df in dataframes.items():
            logger.info(f"Cleaning data for {name}")
            df.drop_duplicates(inplace=True)
            logger.info(f"Dropped duplicates for {name}")
            df.fillna(method='ffill', inplace=True)  # Forward fill as an example
            logger.info(f"Filled missing values for {name}")
            # Add more cleaning steps as needed
            logger.info(f"Cleaning completed for {name}")
        
        logger.info("Data cleaning process completed successfully")
        print("Data cleaning process completed successfully")
        return dataframes
    
    except Exception as e:
        logger.error(f"Error during data cleaning: {e}")
        print(f"Error during data cleaning: {e}")
        raise

if __name__ == '__main__':
    # Test data cleaning
    try:
        dataframes = extract_data()
        cleaned_data = clean_data(dataframes)
        for name in cleaned_data:
            logger.info(f"Successfully cleaned data for {name}")
            print(f"Successfully cleaned data for {name}")
    except Exception as e:
        print(f"Error: {e}")
