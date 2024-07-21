import json
from workflows import Workflows
from dotenv import load_dotenv
from pathlib import Path
import os


def load_config(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)

def main():
    # Specify the path to your .env file
    load_dotenv()
    config = load_config('config.json')
    workflows = Workflows(config)
    
    # workflows.run_classification()
    # workflows.run_regression()
    workflows.run_revenue_prediction()

if __name__ == "__main__":
    main()
