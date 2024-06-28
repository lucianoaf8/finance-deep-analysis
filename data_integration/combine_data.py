# data_integration\combine_data.py

import os
import sys
import pandas as pd

# Add the project directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utils.logging_setup import setup_logging
from data_extraction.extract_data import extract_data
from data_extraction.clean_data import clean_data

logger = setup_logging('combine_data')

def combine_data(dataframes):
    """Combine the cleaned data from both databases into a single dataframe."""
    logger.info("Starting data combination process")
    
    try:
        combined_data = pd.DataFrame()

        # Combine all dataframes into a single dataframe
        for name, df in dataframes.items():
            combined_data = pd.concat([combined_data, df], ignore_index=True)
            logger.info(f"Combined data for {name} successfully")
        
        combined_data.to_excel('data_integration/combined_data.xlsx', index=False)
        logger.info("Saved combined data to 'data_integration/combined_data.xlsx'")
        
        logger.info("Data combination process completed successfully")
        print("Data combination process completed successfully")
        return combined_data
    
    except Exception as e:
        logger.error(f"Error during data combination: {e}")
        print(f"Error during data combination: {e}")
        raise

if __name__ == '__main__':
    # Test data combination
    try:
        dataframes = extract_data()
        cleaned_data = clean_data(dataframes)
        combined_data = combine_data(cleaned_data)
        logger.info("Successfully combined data")
        print("Successfully combined data")
    except Exception as e:
        print(f"Error: {e}")