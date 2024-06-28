# data_analysis\eda.py

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Add the project directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from utils.logging_setup import setup_logging

logger = setup_logging('eda')

def load_data():
    """Load the featured data for analysis."""
    data_path = os.path.join(project_root, 'data_integration', 'featured_data.parquet')
    if os.path.exists(data_path):
        logger.info(f"Loading data from {data_path}")
        data = pd.read_parquet(data_path)
        logger.info("Data loaded successfully")
        return data
    else:
        logger.error(f"Data file not found at {data_path}")
        raise FileNotFoundError(f"Data file not found at {data_path}")

def descriptive_analysis(data):
    """Perform descriptive analysis on the data."""
    logger.info("Performing descriptive analysis")
    print(data.describe(include='all'))

def visualize_data(data):
    """Visualize data to identify trends, outliers, and correlations."""
    logger.info("Visualizing data")

    # Example visualizations
    sns.pairplot(data)
    plt.show()

    sns.heatmap(data.corr(), annot=True, fmt=".2f")
    plt.show()

def summarize_statistics(data):
    """Summarize key statistics and insights from the data."""
    logger.info("Summarizing key statistics")
    summary = data.describe(include='all').to_string()
    with open(os.path.join(project_root, 'data_analysis', 'eda_summary.txt'), 'w') as file:
        file.write(summary)
    logger.info("Summary saved to 'eda_summary.txt'")

if __name__ == '__main__':
    try:
        data = load_data()
        descriptive_analysis(data)
        visualize_data(data)
        summarize_statistics(data)
        logger.info("EDA completed successfully")
        print("EDA completed successfully")
    except Exception as e:
        logger.error(f"Error during EDA: {e}")
        print(f"Error during EDA: {e}")
