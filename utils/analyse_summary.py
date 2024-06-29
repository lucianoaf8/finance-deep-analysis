# utils\analyze_summary.py

import pandas as pd

def analyze_summary(file_path):
    # Read the summary file
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Parse the summary file into a DataFrame
    # Split columns and data more carefully to handle varying spaces
    columns = lines[0].strip().split()
    data = [line.strip().split() for line in lines[1:]]

    # Align columns with data by ensuring rows have the correct number of elements
    max_columns = len(columns)
    formatted_data = []

    for row in data:
        if len(row) < max_columns:
            formatted_data.append(row + [''] * (max_columns - len(row)))
        else:
            formatted_data.append(row[:max_columns])

    df = pd.DataFrame(formatted_data, columns=columns)
    
    # Convert numeric columns to float
    numeric_columns = df.columns[1:]  # Skip the first column if it's non-numeric
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

    # Analyze the DataFrame
    analysis_report = []

    for column in df.columns:
        try:
            analysis_report.append(f"Analysis for '{column}':\n")
            analysis_report.append(f"  Mean: {df[column].mean()}\n")
            analysis_report.append(f"  Standard Deviation: {df[column].std()}\n")
            analysis_report.append(f"  Minimum: {df[column].min()}\n")
            analysis_report.append(f"  25th Percentile: {df[column].quantile(0.25)}\n")
            analysis_report.append(f"  Median: {df[column].median()}\n")
            analysis_report.append(f"  75th Percentile: {df[column].quantile(0.75)}\n")
            analysis_report.append(f"  Maximum: {df[column].max()}\n")
            analysis_report.append("\n")
        except Exception as e:
            analysis_report.append(f"Error processing column '{column}': {e}\n\n")

    return analysis_report

def save_report(report, output_path):
    with open(output_path, 'w') as file:
        for line in report:
            file.write(line)

if __name__ == '__main__':
    summary_file_path = 'data_files/eda_summary.txt'
    report_output_path = 'data_files/eda_summary_analysis_report.txt'
    
    report = analyze_summary(summary_file_path)
    save_report(report, report_output_path)
    
    print(f"Analysis report saved to '{report_output_path}'")
