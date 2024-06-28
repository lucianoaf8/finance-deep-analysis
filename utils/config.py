# utils\config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATABASES = {
    'plaid_db': os.getenv("PLAID_DB"),
    'finance': os.getenv("MBNA_DB")
}
