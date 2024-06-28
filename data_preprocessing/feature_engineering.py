import os
import sys
import pandas as pd
from tqdm import tqdm

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
        
        # Ensure income and expense columns exist
        if 'income' not in data.columns:
            logger.warning("Income column is missing from the data, creating a dummy column")
            data['income'] = 0  # Replace with appropriate logic
        
        if 'expense' not in data.columns:
            logger.warning("Expense column is missing from the data, creating a dummy column")
            data['expense'] = 0  # Replace with appropriate logic
        
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

def read_parquet_with_progress_bar(file_path, chunksize=1000):
    """Read a Parquet file with a progress bar."""
    import dask.dataframe as dd
    df = dd.read_parquet(file_path)
    total_rows = len(df)
    
    # Initialize the progress bar
    pbar = tqdm(total=total_rows, desc="Loading Parquet file", unit="rows")
    
    # Read the Parquet file in chunks
    dfs = []
    for chunk in df.to_delayed():
        chunk_df = chunk.compute()
        pbar.update(len(chunk_df))
        dfs.append(chunk_df)
    
    pbar.close()
    return pd.concat(dfs, ignore_index=True)

if __name__ == '__main__':
    # Test feature engineering
    try:
        parquet_data_path = os.path.join(project_root, 'data_integration', 'normalized_encoded_data.parquet')
        output_data_path = os.path.join(project_root, 'data_integration', 'featured_data.parquet')

        if os.path.exists(parquet_data_path):
            print(f"Loading encoded data from {parquet_data_path}...")
            data = read_parquet_with_progress_bar(parquet_data_path)
            print("Encoded data loaded successfully")
            data = create_features(data)
            logger.info("Successfully created features")
            print("Successfully created features")
            
            # Save the transformed data to a new Parquet file
            data.to_parquet(output_data_path, index=False)
            logger.info(f"Saved featured data to {output_data_path}")
            print(f"Saved featured data to {output_data_path}")
        else:
            logger.error(f"Encoded data file not found at {parquet_data_path}")
            print(f"Encoded data file not found at {parquet_data_path}")
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"Error: {e}")
