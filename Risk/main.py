"""
In order to optimally allocate money to each asset, one must maximize return (in some metric) and minimize risk (in some other metric).

This project maximizes the Sharpe ratio using the riskfolio module.
"""
import yfinance as yf
import riskfolio as rf
import pandas as pd
import warnings
import seaborn as sns
import matplotlib.pyplot as plt


pd.options.display.float_format = "{:.4%}".format
warnings.filterwarnings("ignore")

mag_7 = [
    "AMZN",
    "AAPL",
    "NVDA",
    "META",
    "TSLA",
    "MSFT",
    "GOOG",
]
berkshire_tickers = [
    "AAPL",    # Apple Inc.
    "BAC",     # Bank of America Corp.
    "KO",      # The Coca-Cola Company
    "AXP",     # American Express Co.
    "KHC",     # The Kraft Heinz Company
    "MCO",     # Moody's Corporation
    "VZ",      # Verizon Communications Inc.
    "CVX",     # Chevron Corporation
    "DVA",     # DaVita Inc.
    "BK",      # The Bank of New York Mellon Corporation
    "USB",     # U.S. Bancorp
    "C",       # Citigroup Inc.
    "V",       # Visa Inc.
    "MA",      # Mastercard Inc.
    "JNJ",     # Johnson & Johnson
    "PG",      # Procter & Gamble Co.
    "UPS",     # United Parcel Service Inc.
    "GS",      # The Goldman Sachs Group, Inc.
    "WFC",     # Wells Fargo & Company
    "GM"      # General Motors Company
]


factors = ["MTUM", "QUAL", "VLUE", "SIZE", "USMV"]


start = "2020-01-01"
end = "2024-07-31"

port_returns = (
    yf
    .download(
        berkshire_tickers, 
        start=start, 
        end=end
    )["Adj Close"]
    .pct_change()
    .dropna()
)

factor_returns = (
    yf
    .download(
        factors, 
        start=start, 
        end=end
    )["Adj Close"]
    .pct_change()
    .dropna()
)

port = rf.Portfolio(returns=port_returns)

port.assets_stats(method_mu="hist", method_cov="ledoit")

port.lowerret = 0.00056488 * 1.5

loadings = rf.loadings_matrix(
    X=factor_returns,
    Y=port_returns, 
    feature_selection="PCR",
    n_components=0.95
)

loadings.style.format("{:.4f}").background_gradient(cmap='RdYlGn')

# Display the heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(loadings, annot=True, fmt=".4f", cmap='RdYlGn')
plt.title("Factor Loadings Heatmap")
plt.savefig('factor_loadings_heatmap.png')
plt.clf()

port.factors = factor_returns
port.factors_stats(
    method_mu="hist",
    method_cov="ledoit",
    feature_selection="PCR",
    n_components=0.95
)

w = port.optimization(
    model="FM",
    rm="MV",
    obj="Sharpe",
    hist=False,
)

ax = rf.plot_pie(
    w=w,
    title='Sharpe FM Mean Variance',
    others=0.05,
    nrow=25,
    cmap="tab20"
)

ax.figure.savefig('sharpe_fm_mean_variance.png')
