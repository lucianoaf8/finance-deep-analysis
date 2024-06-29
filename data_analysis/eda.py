import os
import sys
import dask.dataframe as dd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

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
        data = dd.read_parquet(data_path)
        logger.info("Data loaded successfully")
        return data
    else:
        logger.error(f"Data file not found at {data_path}")
        raise FileNotFoundError(f"Data file not found at {data_path}")

def descriptive_analysis(data):
    """Perform descriptive analysis on the data with a progress bar."""
    logger.info("Performing descriptive analysis")
    print("Performing descriptive analysis...")

    summary = data.describe().compute()
    print(summary)

def visualize_data(data):
    """Visualize data to identify trends, outliers, and correlations."""
    logger.info("Visualizing data")
    print("Visualizing data...")

    # Use a smaller sample for visualization to avoid memory issues
    sample_fraction = 0.01  # Use 1% of the data
    sample = data.sample(frac=sample_fraction).compute()

    # Visualize pairplot (example, adjust as needed)
    sns.pairplot(sample)
    plt.show()

    # Visualize correlation heatmap
    corr = sample.corr()
    sns.heatmap(corr, annot=True, fmt=".2f")
    plt.show()

def summarize_statistics(data):
    """Summarize key statistics and insights from the data."""
    logger.info("Summarizing key statistics")
    print("Summarizing key statistics...")
    summary = data.describe().compute().to_string()
    summary_path = os.path.join(project_root, 'data_analysis', 'eda_summary.txt')
    with open(summary_path, 'w') as file:
        file.write(summary)
    logger.info(f"Summary saved to '{summary_path}'")
    print(f"Summary saved to '{summary_path}'")

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
