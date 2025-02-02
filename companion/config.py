import os
import yaml

# Locate config.yaml at the root directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
CONFIG_PATH = os.path.join(BASE_DIR, "..", "config.yaml")

# Load configuration once and reuse
try:
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}  # Ensure a dictionary is always returned
except FileNotFoundError:
    print("⚠️ Warning: config.yaml not found, using empty defaults.")
    config = {}  # Default to an empty dictionary if missing