# C:\Projects\finance-deep-analysis\data_analysis\income_expenses.py

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

logger = setup_logging('income_expenses')

def analyze_income_expenses(combined_data):
    """Analyze income and expenses."""
    logger.info("Starting income and expenses analysis")
    
    try:
        # Analyze income
        inflow_data = combined_data[combined_data['type'] == 'inflow']
        total_income = inflow_data.groupby('institution_name')['amount'].sum()
        logger.info(f"Total income by institution: {total_income}")
        
        # Analyze expenses
        outflow_data = combined_data[combined_data['type'] == 'outflow']
        total_expenses = outflow_data.groupby('institution_name')['amount'].sum()
        logger.info(f"Total expenses by institution: {total_expenses}")
        
        # Classify transactions
        transaction_data = combined_data[combined_data['type'] == 'transaction']
        categorized_transactions = transaction_data.groupby(['category', 'institution_name'])['amount'].sum().unstack()
        logger.info(f"Categorized transactions: {categorized_transactions}")
        
        logger.info("Income and expenses analysis completed successfully")
        print("Income and expenses analysis completed successfully")
        return total_income, total_expenses, categorized_transactions
    
    except Exception as e:
        logger.error(f"Error during income and expenses analysis: {e}")
        print(f"Error during income and expenses analysis: {e}")
        raise

if __name__ == '__main__':
    try:
        dataframes = extract_data()
        cleaned_data = clean_data(dataframes)
        combined_data = combine_data(cleaned_data)
        total_income, total_expenses, categorized_transactions = analyze_income_expenses(combined_data)
        logger.info("Successfully analyzed income and expenses")
        print("Successfully analyzed income and expenses")
    except Exception as e:
        print(f"Error: {e}")
