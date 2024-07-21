import re
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load equity dataframe from the saved pickle file
data = pd.read_pickle("data/nn_data.pkl")

# Create binary column of positive and negative earnings changes
data['binary change'] = [1 if row['change in EPS'] > 0 else 0 for _,row in data.iterrows()]

# Shift date index by -1 so we are predicting future changes: 1 or 0
data['Future change'] = data['binary change'].shift(-1)



# Goal is to anticipate the sign of future earnings change from the financial data of the current quarter.
# If the future earnings changes is + , we assign 1, otherwise 0, to Future change value of the current quarter
data[['EPS','change in EPS','Future change']].head(6)

# Examine data 
data.describe()

# Replace infinity with nan
data = data.replace([np.inf, -np.inf], np.nan)

#Drop rows where change in EPS is nan: they are no use to us 
data = data.dropna(subset = ['change in EPS', 'Future change'])


# We no longer need these columns
data = data.drop(columns = ['EPS','change in EPS','binary change'])


# Examine missing data
missing_column_data = 100*(data.isnull().sum() / data.shape[0]).round(3)
print('Percent of missing values per column:\n', missing_column_data)

# Percent of missing values per column:
#  Account Receivable Turnover                43.4
# Current Ratio                              15.8
# Quick Ratio                                15.8
# Inventory Turnover                         54.2
# Total Debt To Equity                        4.1
# EBITDA Margin                               8.0
# ROA                                        30.3
# ROE                                        34.3
# Gross Profit Margin                        21.3
# Accounts Receivable Turnover               43.4
# Inventory to Sales                         42.0
# LT Debt to Total Equity                     3.8
# Sales to Total Assets                       0.3
# EBIT to revenue                             4.1
# Profit margin                               0.0
# Sales to Cash                               0.4
# Sales to Inventory                         32.2
# Sales to Working capital                   15.8
# Sales to Dep Fixed assets                  44.3
# Working capital to total Asset             15.8
# Operating Income to Total Assets            0.3
# Trailing 12M EBITDA Margin                  8.0
# Div as % of CF                              0.5
# change in Depreciation and Amortization     1.6
# change in Inventories                      32.2
# change in Inventory Turnover               56.0
# change in R&D Expense                      69.0
# change Total Assets                         0.4
# change in Long Term Debt                    5.3
# change in Short Term Debt                  16.0
# change in Revenue                           0.0
# change in Current Ratio                    15.9
# change in Quick Ratio                      15.9
# change in Tot Debt to Common Equity         8.5
# change in Gross Margin                     21.3
# Changes in Working Capital                 16.3
# Change in Inventory to Sales               53.6
# Change in Dep Amort Expense                 1.6
# Change in CAPAX to Assets                   4.0
# Change in LTD to Equity                    13.4
# Change in Equity to Fixed Assets           45.2
# Change in Sales to Total Assets             0.4
# Change in EBIT to revenue                   4.1
# Change in Profit margin                     0.0
# Change in Sales to Inventory               32.3
# Change in Sales to Working capital         16.0
# Change in R&D to Revenue                   69.0
# Change in working cap to Assets            16.5
# Change in Operating Income or Losses        0.5
# Change in EBITDA Margin                     8.0
# Future change                               0.0



# Drop 10 columns that have more than 35% of data missing
columns_to_drop = missing_column_data[missing_column_data > 35]


# Number of columns dropped, 10
data = data.drop(columns = list(columns_to_drop.index))
# New Dataframe shape : (18903, 41)



# Keep in mind that this is a naive way to handle missing values. 
# This method can cause data leakage and does not factor the covariance between features.
# For more robust methods, take a look at MICE or KNN

for col in data.columns:
    data[col].fillna(data[col].mean(), inplace=True)
    
# Check for missing values
missing_column_data = 100*(data.isnull().sum()/ data.shape[0]).round(3)
print('Percent of missing values per column:\n',missing_column_data)


# First we need to split our data into train and test. 
from sklearn.model_selection import train_test_split

# Independent values/features
X = data.iloc[:,:-1].values
# Dependent values
y = data.iloc[:,-1].values

# Create test and train data sets, split data randomly into 20% test and 80% train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)


from scipy.stats import mstats
# Winsorize top 1% and bottom 1% of points

# Apply on X_train and X_test separately
X_train = mstats.winsorize(X_train, limits = [0.01, 0.01])
X_test = mstats.winsorize(X_test, limits = [0.01, 0.01])


# IMPORTANT: During testing, it is important to construct the test feature vectors using the means and standard deviations saved from
# the training data, rather than computing it from the test data. You must scale your test inputs using the saved means
# and standard deviations, prior to sending them to your Neural Networks library for classification.

from sklearn.preprocessing import StandardScaler

sc = StandardScaler()

# Fit to training data and then transform it
X_train = sc.fit_transform(X_train)
# Perform standardization on testing data using mu and sigma from training data
X_test = sc.transform(X_test)

# Import accuracy score
from sklearn.metrics import accuracy_score

# Multi-layer Perceptron classifier contains one or more hidden layers and can learn non-linear functions. 
from sklearn.neural_network import MLPClassifier

# hidden_layer_sizes allows us to set the number of layers and the number of nodes we wish to have in the Neural Network Classifier
# max_iter denotes the number of epochs.
# activation function for the hidden layers.
# solver specifies the algorithm for weight optimization across the nodes.

mlp = MLPClassifier(hidden_layer_sizes = (150,100,50), max_iter=300,activation = 'relu',solver = 'adam', random_state = 0)

# Train
mlp.fit(X_train,y_train)
# Predict 
y_pred = mlp.predict(X_test)
# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print('Accuracy: {:.2f}'.format(accuracy))