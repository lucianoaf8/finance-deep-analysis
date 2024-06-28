# utils\setup.py

import os

# Define the project structure
project_structure = {
    'data_extraction': ['__init__.py', 'db_connection.py', 'extract_data.py', 'clean_data.py'],
    'data_integration': ['__init__.py', 'combine_data.py'],
    'data_preprocessing': ['__init__.py', 'normalize_encode.py', 'feature_engineering.py'],
    'data_analysis': [
        '__init__.py', 'account_balances.py', 'income_expenses.py',
        'liabilities_analysis.py', 'spending_analysis.py', 'interest_fees.py'
    ],
    'logs': [],
    'utils': ['__init__.py', 'config.py', 'logging_setup.py'],
    '': ['main.py', 'requirements.txt', '.env', 'README.md']
}

# Create directories and files
for folder, files in project_structure.items():
    if folder:  # Non-root directories
        os.makedirs(folder, exist_ok=True)
    for file in files:
        file_path = os.path.join(folder, file) if folder else file
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                if file.endswith('.py'):
                    f.write("# " + file_path + "\n")
                elif file == 'README.md':
                    f.write("# Finance Deep Analysis Project\n")
                else:
                    f.write("")

print("Project setup completed.")
