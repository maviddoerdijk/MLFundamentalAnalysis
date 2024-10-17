import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

def plot_temp():
    tickers = ["^GSPC", "APTV", "ADM", "BG", "FMC", "MPC", "MRNA", "MHK", "NUE", "VLO"]
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(45, 10))
    fig.suptitle('Normalized Close Prices for S&P 500 and Selected Tickers')
    
    normalized_closes = []
    normalized_closes_excluding_mrna = []
    
    for ticker in tickers:
        data = yf.Ticker(ticker).history(period="5y")
        data = data.drop(columns=['Dividends', 'Stock Splits'])
        first_price = data['Close'].iloc[0]
        normalized_close = data['Close'] / first_price
        ax1.plot(normalized_close, label=ticker if not ticker == "^GSPC" else "S&P 500")
        
        if ticker != "^GSPC":
            normalized_closes.append(normalized_close)
            if ticker != "MRNA":
                normalized_closes_excluding_mrna.append(normalized_close)
    
    # Calculate the average of tickers[1:]
    avg_normalized_close = pd.concat(normalized_closes, axis=1).mean(axis=1)
    ax1.plot(avg_normalized_close, label='Average', linestyle='--', linewidth=2)
    
    # Plot only S&P 500 and average on the middle subplot
    sp500_data = yf.Ticker("^GSPC").history(period="5y")
    sp500_first_price = sp500_data['Close'].iloc[0]
    sp500_normalized_close = sp500_data['Close'] / sp500_first_price
    ax2.plot(sp500_normalized_close, label="S&P 500")
    ax2.plot(avg_normalized_close, label='Average', linestyle='--', linewidth=2)
    
    # Calculate the average excluding MRNA
    avg_normalized_close_excluding_mrna = pd.concat(normalized_closes_excluding_mrna, axis=1).mean(axis=1)
    
    # Plot S&P 500 and average excluding MRNA on the right subplot
    ax3.plot(sp500_normalized_close, label="S&P 500")
    ax3.plot(avg_normalized_close_excluding_mrna, label='Average (Excl. MRNA)', linestyle='--', linewidth=2)
    
    # Set titles and legends
    ax1.set_title('All Tickers')
    ax1.legend()
    ax2.set_title('S&P 500 vs Average')
    ax2.legend()
    ax3.set_title('S&P 500 vs Average (Excl. MRNA)')
    ax3.legend()
    
    plt.savefig('GeneralPlots/plots/multiple_tickers_normalized.png')

if __name__ == '__main__':
    plot_temp()