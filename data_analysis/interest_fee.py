# C:\Projects\finance-deep-analysis\data_analysis\interest_fees.py

import os
import sys
import pandas as pd

# Add the project directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utils.logging_setup import setup_logging
from data_extraction.extract_data import extract_data
from data_extraction.clean_data import clean_data
from data_integration.combine_data import combine_data

logger = setup_logging('interest_fees')

def analyze_interest_fees(combined_data):
    """Analyze interest and fees."""
    logger.info("Starting interest and fees analysis")
    
    try:
        # Calculate interest charges
        interest_data = combined_data[combined_data['type'] == 'interest']
        total_interest = interest_data.groupby('institution_name')['interest_charge_amount'].sum()
        logger.info(f"Total interest charges by institution: {total_interest}")
        
        # Analyze fees
        fee_data = combined_data[combined_data['type'] == 'fee']
        total_fees = fee_data.groupby('institution_name')['amount'].sum()
        logger.info(f"Total fees by institution: {total_fees}")
        
        logger.info("Interest and fees analysis completed successfully")
        print("Interest and fees analysis completed successfully")
        return total_interest, total_fees
    
    except Exception as e:
        logger.error(f"Error during interest and fees analysis: {e}")
        print(f"Error during interest and fees analysis: {e}")
        raise

if __name__ == '__main__':
    try:
        dataframes = extract_data()
        cleaned_data = clean_data(dataframes)
        combined_data = combine_data(cleaned_data)
        total_interest, total_fees = analyze_interest_fees(combined_data)
        logger.info("Successfully analyzed interest and fees")
        print("Successfully analyzed interest and fees")
    except Exception as e:
        print(f"Error: {e}")
