# C:\Projects\finance-deep-analysis\data_analysis\liabilities_analysis.py

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

logger = setup_logging('liabilities_analysis')

def analyze_liabilities(combined_data):
    """Analyze liabilities."""
    logger.info("Starting liabilities analysis")
    
    try:
        # Assess credit liabilities
        liabilities_data = combined_data[combined_data['type'] == 'liability']
        total_liabilities = liabilities_data.groupby('institution_name')['balance'].sum()
        logger.info(f"Total liabilities by institution: {total_liabilities}")
        
        # Calculate minimum payments and due dates
        minimum_payments = liabilities_data.groupby('institution_name')['minimum_payment_amount'].sum()
        next_due_dates = liabilities_data.groupby('institution_name')['next_payment_due_date'].min()
        logger.info(f"Minimum payments by institution: {minimum_payments}")
        logger.info(f"Next due dates by institution: {next_due_dates}")
        
        logger.info("Liabilities analysis completed successfully")
        print("Liabilities analysis completed successfully")
        return total_liabilities, minimum_payments, next_due_dates
    
    except Exception as e:
        logger.error(f"Error during liabilities analysis: {e}")
        print(f"Error during liabilities analysis: {e}")
        raise

if __name__ == '__main__':
    try:
        dataframes = extract_data()
        cleaned_data = clean_data(dataframes)
        combined_data = combine_data(cleaned_data)
        total_liabilities, minimum_payments, next_due_dates = analyze_liabilities(combined_data)
        logger.info("Successfully analyzed liabilities")
        print("Successfully analyzed liabilities")
    except Exception as e:
        print(f"Error: {e}")
