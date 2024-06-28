# C:\Projects\finance-deep-analysis\data_analysis\account_balances.py

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

logger = setup_logging('account_balances')

def analyze_account_balances(combined_data):
    """Analyze account balances."""
    logger.info("Starting account balances analysis")
    
    try:
        # Log the columns and first few rows of the combined data
        logger.info(f"Combined data columns: {combined_data.columns.tolist()}")
        logger.info(f"Combined data preview:\n{combined_data.head()}")
        
        # Check for required columns
        if 'type' not in combined_data.columns:
            raise ValueError("Required column 'type' not found in the combined data")
        
        if 'bank_name' not in combined_data.columns:
            raise ValueError("Required column 'bank_name' not found in the combined data")
        
        # Filter account data
        account_data = combined_data[combined_data['type'] == 'account']
        
        # Calculate total balances
        total_balances = account_data.groupby('bank_name')['current_balance'].sum()
        logger.info(f"Total balances by bank: {total_balances}")
        
        # Analyze historical balance trends
        historical_balances = combined_data[combined_data['type'] == 'historical_balance']
        balance_trends = historical_balances.groupby(['bank_name', 'date'])['current_balance'].sum().unstack()
        logger.info(f"Historical balance trends: {balance_trends}")
        
        logger.info("Account balances analysis completed successfully")
        print("Account balances analysis completed successfully")
        return total_balances, balance_trends
    
    except Exception as e:
        logger.error(f"Error during account balances analysis: {e}")
        print(f"Error during account balances analysis: {e}")
        raise

if __name__ == '__main__':
    try:
        combined_data_path = os.path.join(project_root, 'data_integration', 'combined_data.xlsx')
        
        if os.path.exists(combined_data_path):
            logger.info(f"Loading combined data from {combined_data_path}")
            combined_data = pd.read_excel(combined_data_path)
        else:
            logger.info("Combined data file not found. Running data extraction, cleaning, and combining.")
            dataframes = extract_data()
            cleaned_data = clean_data(dataframes)
            combined_data = combine_data(cleaned_data)
        
        total_balances, balance_trends = analyze_account_balances(combined_data)
        logger.info("Successfully analyzed account balances")
        print("Successfully analyzed account balances")
    except Exception as e:
        print(f"Error: {e}")
