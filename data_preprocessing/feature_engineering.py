# data_preprocessing\feature_engineering.py

import os
import sys
import pandas as pd

# Add the project directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utils.logging_setup import setup_logging

logger = setup_logging('feature_engineering')

def create_features(data):
    """Create new features such as monthly aggregates, trends, and ratios."""
    logger.info("Starting feature engineering process")
    
    try:
        # Example feature: Monthly aggregates
        data['month'] = pd.to_datetime(data['date']).dt.to_period('M')
        monthly_aggregates = data.groupby('month').agg({
            'amount': ['sum', 'mean', 'std'],
            'current_balance': 'mean'
        }).reset_index()
        monthly_aggregates.columns = ['_'.join(col).strip() for col in monthly_aggregates.columns.values]
        data = pd.merge(data, monthly_aggregates, on='month', how='left')
        logger.info("Created monthly aggregates")
        
        # Example feature: Income-to-expense ratio
        data['income_to_expense_ratio'] = data['income_sum'] / data['expenses_sum']
        logger.info("Created income-to-expense ratio")
        
        logger.info("Feature engineering process completed successfully")
        print("Feature engineering process completed successfully")
        return data
    
    except Exception as e:
        logger.error(f"Error during feature engineering: {e}")
        print(f"Error during feature engineering: {e}")
        raise

if __name__ == '__main__':
    # Test feature engineering
    try:
        combined_data_path = os.path.join(project_root, 'data_integration', 'combined_data.xlsx')
        if os.path.exists(combined_data_path):
            data = pd.read_excel(combined_data_path)
            data = create_features(data)
            logger.info("Successfully created features")
            print("Successfully created features")
        else:
            logger.error(f"Combined data file not found at {combined_data_path}")
            print(f"Combined data file not found at {combined_data_path}")
    except Exception as e:
        print(f"Error: {e}")
