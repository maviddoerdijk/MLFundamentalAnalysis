import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))) # add parent dir - 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))) # add parent dir - 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', ))) # add parent dir - 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ))) # add parent dir - 

import streamlit as st
import plotly.express as px
import pandas as pd
from GatherFundamental.calculate_ratios import get_fundamentals_dict

# Define ticker collections
ticker_collections = {
    "Magnificent Seven": ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA'],
    "FAANG": ['FB', 'AAPL', 'AMZN', 'NFLX', 'GOOGL'],
    "Top 10 AEX Companies": ['ASML', 'ADYEN', 'AALB', 'DSM', 'HEIA', 'IMCD', 'KPN', 'NN', 'PHIA', 'RAND']
}

# Streamlit app
st.title("Stock Analysis Dashboard")

# Create two columns
left_column, right_column = st.columns(2)

# Right column: Dropdown for ticker collections
with right_column:
    selected_collection = st.selectbox("Select Ticker Collection", list(ticker_collections.keys()))
    stocks = ticker_collections[selected_collection]

# Prepare data
data = {
    'Stock': [],
    'PE Ratio': [],
    'Cash Ratio': [],
    'Market Cap': []
}

for stock in stocks:
    metrics = get_fundamentals_dict(stock, ["PE Ratio", "Cash Ratio", "Market Cap"])
    data['Stock'].append(stock)
    data['PE Ratio'].append(metrics['PE Ratio'])
    data['Cash Ratio'].append(metrics['Cash Ratio'])
    data['Market Cap'].append(metrics['Market Cap'])

# Convert to DataFrame
df = pd.DataFrame(data)

# Create bubble chart using plotly express
fig = px.scatter(
    df,
    x="Cash Ratio",
    y="PE Ratio",
    size="Market Cap",
    color="Stock",
    hover_name="Stock",
    size_max=60,
    title="PE Ratio vs Cash Ratio (Bubble Size = Market Cap)"
)

# Left column: Display the plot
with left_column:
    st.plotly_chart(fig)