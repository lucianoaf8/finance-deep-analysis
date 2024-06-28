# data_extraction\extract_data.py

import os
import sys
import pandas as pd

# Add the project directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from data_extraction.db_connection import get_engine
from utils.config import DATABASES
from utils.logging_setup import setup_logging

logger = setup_logging('extract_data')

def extract_data():
    """Extract data from both databases and return as dataframes."""
    logger.info("Starting data extraction process")
    
    try:
        plaid_engine = get_engine(DATABASES['plaid_db'])
        finance_engine = get_engine(DATABASES['finance'])

        dataframes = {}

        # Extracting data from plaid_db
        logger.info("Extracting data from plaid_db")
        dataframes['plaid_accounts'] = pd.read_sql('SELECT * FROM plaid_accounts', plaid_engine)
        logger.info("Extracted plaid_accounts successfully")
        
        dataframes['plaid_liabilities_credit'] = pd.read_sql('SELECT * FROM plaid_liabilities_credit', plaid_engine)
        logger.info("Extracted plaid_liabilities_credit successfully")
        
        dataframes['plaid_liabilities_credit_apr'] = pd.read_sql('SELECT * FROM plaid_liabilities_credit_apr', plaid_engine)
        logger.info("Extracted plaid_liabilities_credit_apr successfully")
        
        dataframes['plaid_transactions'] = pd.read_sql('SELECT * FROM plaid_transactions', plaid_engine)
        logger.info("Extracted plaid_transactions successfully")
        
        dataframes['plaid_transaction_counterparties'] = pd.read_sql('SELECT * FROM plaid_transaction_counterparties', plaid_engine)
        logger.info("Extracted plaid_transaction_counterparties successfully")
        
        dataframes['asset_report'] = pd.read_sql('SELECT * FROM asset_report', plaid_engine)
        logger.info("Extracted asset_report successfully")
        
        dataframes['asset_account'] = pd.read_sql('SELECT * FROM asset_account', plaid_engine)
        logger.info("Extracted asset_account successfully")
        
        dataframes['asset_transaction'] = pd.read_sql('SELECT * FROM asset_transaction', plaid_engine)
        logger.info("Extracted asset_transaction successfully")
        
        dataframes['asset_historical_balance'] = pd.read_sql('SELECT * FROM asset_historical_balance', plaid_engine)
        logger.info("Extracted asset_historical_balance successfully")
        
        dataframes['inflow_streams'] = pd.read_sql('SELECT * FROM inflow_streams', plaid_engine)
        logger.info("Extracted inflow_streams successfully")
        
        dataframes['outflow_streams'] = pd.read_sql('SELECT * FROM outflow_streams', plaid_engine)
        logger.info("Extracted outflow_streams successfully")
        
        dataframes['inflow_transactions'] = pd.read_sql('SELECT * FROM inflow_transactions', plaid_engine)
        logger.info("Extracted inflow_transactions successfully")
        
        dataframes['outflow_transactions'] = pd.read_sql('SELECT * FROM outflow_transactions', plaid_engine)
        logger.info("Extracted outflow_transactions successfully")

        logger.info("Extracting data from finance")
        dataframes['mbna_accounts'] = pd.read_sql('SELECT * FROM mbna_accounts', finance_engine)
        logger.info("Extracted mbna_accounts successfully")
        
        dataframes['mbna_transactions'] = pd.read_sql('SELECT * FROM mbna_transactions', finance_engine)
        logger.info("Extracted mbna_transactions successfully")

        logger.info("Data extraction completed successfully")
        print("Data extraction completed successfully")
        return dataframes
    
    except Exception as e:
        logger.error(f"Error during data extraction: {e}")
        print(f"Error during data extraction: {e}")
        raise

if __name__ == '__main__':
    # Test data extraction
    try:
        dataframes = extract_data()
        for name, df in dataframes.items():
            logger.info(f"Successfully extracted data for {name}")
            print(f"Successfully extracted data for {name}")
    except Exception as e:
        print(f"Error: {e}")
