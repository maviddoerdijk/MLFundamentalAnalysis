import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def load_data(file_path):
    return pd.read_pickle(file_path)


def prepare_financial_data(income_statement, input_feature_names):
    # Convert income_statement to DataFrame
    data = pd.DataFrame(income_statement)
    
    # Transpose the DataFrame to have years as rows and financial metrics as columns
    data = data.T
    
    # Flatten the multi-level columns
    data.columns = ['_'.join(col).strip() for col in data.columns.values]
    
    # Reset index to have the years as a column
    data.reset_index(inplace=True)
    
    # Rename columns for easier access and ensure 'Year' is the first column
    data.rename(columns={data.columns[0]: 'Year'}, inplace=True)
    data['Year'] = data['Year'].astype(str).str[:4].astype(int)
    
    # Drop rows with missing 'Revenue' values
    revenue_columns = [col for col in data.columns if 'Revenue' in col]
    data = data.dropna(subset=revenue_columns)
    
    # Fill missing values with column means
    data = data.fillna(data.mean())
    
    # Define features (X) and target (y)
    feature_columns = [col for col in data.columns if any(feature in col for feature in input_feature_names)]
    X = data[feature_columns]
    y = data[revenue_columns[0]]  # Assuming the first 'Revenue' column is the target
    
    return X, y

def preprocess_data(data):
    data['binary change'] = [1 if row['change in EPS'] > 0 else 0 for _, row in data.iterrows()]
    data['Future change'] = data['binary change'].shift(-1)
    data = data.replace([np.inf, -np.inf], np.nan)
    data = data.dropna(subset=['change in EPS', 'Future change'])
    data = data.drop(columns=['EPS', 'change in EPS', 'binary change'])
    missing_column_data = 100 * (data.isnull().sum() / data.shape[0]).round(3)
    columns_to_drop = missing_column_data[missing_column_data > 35]
    data = data.drop(columns=list(columns_to_drop.index))
    for col in data.columns:
        data[col].fillna(data[col].mean(), inplace=True)
    return data

def split_data(data):
    X = data.iloc[:, :-1].values
    y = data.iloc[:, -1].values
    return train_test_split(X, y, test_size=0.2, random_state=0)

