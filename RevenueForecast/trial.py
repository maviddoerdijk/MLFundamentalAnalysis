import os
from dotenv import load_dotenv
import pandas as pd

from financetoolkit import Toolkit
import yfinance as yf


def main():

    load_dotenv()
    print(os.getenv('FINANCIAL_MODELING_PREP_API_KEY'))
    quit()

if __name__ == '__main__':
    main()