import os
from dotenv import load_dotenv
import pandas as pd

from financetoolkit import Toolkit
import yfinance as yf

load_dotenv()

def main():
    LOAD_NEW_DATA = True
    
    
    ## load stock data from yfinance
    ticker = 'AAPL'
    start_date = '2021-01-01'
    end_date = '2021-12-31'
    if LOAD_NEW_DATA:
        # Load stock data from yfinance
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        print(stock_data.head())

        # Load financial statement data from financetoolkit
        companies = Toolkit([ticker], api_key=os.getenv('FINANCIAL_MODELING_PREP_API_KEY'), start_date=start_date)
        
        # Obtain different financial statements
        income_statement = companies.get_income_statement()
        balance_sheet_statement = companies.get_balance_sheet_statement()
        cash_flow_statement = companies.get_cash_flow_statement()
        
        # Save to CSV
        stock_data.to_csv('data/stock_data.csv')
        income_statement.to_csv('data/income_statement.csv')
        balance_sheet_statement.to_csv('data/balance_sheet_statement.csv')
        cash_flow_statement.to_csv('data/cash_flow_statement.csv')
    else:
        # Load stock data from CSV
        stock_data = pd.read_csv('data/stock_data.csv', index_col=0)

        # Load financial statement data from CSV
        income_statement = pd.read_csv('data/income_statement.csv', index_col=0)
        balance_sheet_statement = pd.read_csv('data/balance_sheet_statement.csv', index_col=0)
        cash_flow_statement = pd.read_csv('data/cash_flow_statement.csv', index_col=0)
    
    print(stock_data.head())
    print(income_statement.head())
    print(balance_sheet_statement.head())
    print(cash_flow_statement.head())


    # Merge stock prices and financial statements data on a common key (e.g., date)
    # merged_data = pd.merge(stock_data, financial_data, on='date')
    
if __name__ == '__main__':
    main()