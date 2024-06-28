import os
import sys
import pandas as pd
from tqdm import tqdm
from pandas.io.parsers import TextFileReader

# Add the project directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utils.logging_setup import setup_logging

logger = setup_logging('feature_engineering')

def create_features(data):
    """Create new features such as monthly aggregates, trends, and ratios."""
    logger.info("Starting feature engineering process")
    print("Starting feature engineering process")

    try:
        # Example feature: Monthly aggregates
        print("Creating monthly aggregates...")
        data['month'] = pd.to_datetime(data['date']).dt.to_period('M').astype(str)
        monthly_aggregates = data.groupby('month').agg({
            'amount': ['sum', 'mean', 'std'],
            'current_balance': 'mean'
        }).reset_index()
        monthly_aggregates.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in monthly_aggregates.columns.values]
        data = pd.merge(data, monthly_aggregates, left_on='month', right_on='month_', how='left')
        logger.info("Created monthly aggregates")
        print("Created monthly aggregates")
        
        # Ensure income and expense columns exist or create them based on some logic
        if 'income' not in data.columns or 'expense' not in data.columns:
            logger.error("Income and expense columns are missing from the data")
            raise KeyError("Income and expense columns are missing from the data")
        
        # Example feature: Income-to-expense ratio
        print("Creating income-to-expense ratio...")
        income_sum = data.groupby('month')['income'].sum().rename('income_sum')
        expense_sum = data.groupby('month')['expense'].sum().rename('expense_sum')
        
        data = data.join(income_sum, on='month')
        data = data.join(expense_sum, on='month')
        
        data['income_to_expense_ratio'] = data['income_sum'] / data['expense_sum']
        logger.info("Created income-to-expense ratio")
        print("Created income-to-expense ratio")
        
        logger.info("Feature engineering process completed successfully")
        print("Feature engineering process completed successfully")
        return data
    
    except Exception as e:
        logger.error(f"Error during feature engineering: {e}")
        print(f"Error during feature engineering: {e}")
        raise

def read_excel_with_progress_bar(file_path):
    """Read an Excel file with a progress bar."""
    # Use ExcelFile to get the number of rows in advance
    excel_file = pd.ExcelFile(file_path)
    total_rows = 0
    for sheet_name in excel_file.sheet_names:
        total_rows += len(pd.read_excel(file_path, sheet_name=sheet_name, nrows=0))
    
    # Initialize the progress bar
    pbar = tqdm(total=total_rows, desc="Loading Excel file", unit="rows")

    # Read the Excel file
    dfs = []
    for sheet_name in excel_file.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        pbar.update(len(df))
        dfs.append(df)
    
    pbar.close()
    return pd.concat(dfs, ignore_index=True)

if __name__ == '__main__':
    # Test feature engineering
    try:
        encoded_data_path = os.path.join(project_root, 'data_integration', 'normalized_encoded_data.xlsx')
        if os.path.exists(encoded_data_path):
            print(f"Loading encoded data from {encoded_data_path}...")
            data = read_excel_with_progress_bar(encoded_data_path)
            print("Encoded data loaded successfully")
            data = create_features(data)
            logger.info("Successfully created features")
            print("Successfully created features")
        else:
            logger.error(f"Encoded data file not found at {encoded_data_path}")
            print(f"Encoded data file not found at {encoded_data_path}")
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"Error: {e}")
