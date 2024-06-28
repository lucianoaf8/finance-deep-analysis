# C:\Projects\finance-deep-analysis\main.py

import os
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_extraction.db_connection import get_engine
from data_extraction.extract_data import extract_data
from data_extraction.clean_data import clean_data
from utils.logging_setup import setup_logging
from utils.config import DATABASES

logger = setup_logging('main')

def main():
    try:
        logger.info("Starting the financial data analysis project")
        
        # Test database connection
        logger.info("Testing database connection")
        try:
            get_engine(DATABASES['plaid_db'])
            get_engine(DATABASES['finance'])
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return
        
        # Step 1: Extract data
        logger.info("Step 1: Extracting data")
        dataframes = extract_data()
        
        # Step 2: Clean data
        logger.info("Step 2: Cleaning data")
        cleaned_data = clean_data(dataframes)
        
        # Print or save cleaned data for verification
        for name, df in cleaned_data.items():
            logger.info(f"\nData from {name}:")
            print(f"\nData from {name}:")
            print(df.head())
        
        logger.info("Financial data analysis project completed successfully")
    
    except Exception as e:
        logger.error(f"Error in main script: {e}")
        raise

if __name__ == '__main__':
    main()
