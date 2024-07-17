"https://medium.com/@gerard.agada/basic-ai-machine-learning-for-financial-statement-analysis-6ccaa1bd5cec"

from datetime import datetime
import pandas as pd
from prophet import Prophet
import simfin as sf
import seaborn as sns
import matplotlib.pyplot as plt


api_key = ''

# Set the dictionary location
sf.set_data_dir('~/simfin_data')
# Import free api key
sf.set_api_key(api_key=api_key)
# Load the income data with variant and market.
df = sf.load(dataset='income', variant='quarterly', market='us')


df_ = df[df['Ticker'] =='TSLA']


# Set the target variable
target_value = 'Revenue'
df_rev = df_[['Report Date',target_value]].copy()

#Convert the report date to a datetime format
df_rev['Report date'] = df_rev['Report Date'].map(lambda x: pd.to_datetime(x))
#Plot the chart of revenues by quarter from 2016 - 2021
plt. rcParams ["figure. figsize"] = (15,6)
sns.set_theme()
sns.lineplot(data=df_rev, x='Report date', y = target_value)

#Instantiate the Prophet model
model = Prophet()
# Fit the model - features and y target have to be renamed in order for the function to work.
model.fit(df_rev.rename(columns={'Report Date': 'ds', target_value: 'y'}))


#Predict 4 years and the next 16 periods
new_future_dates = model.make_future_dataframe(periods=16, freq = 'Q')

#Use the predict method and set that to the forecast
forecast = model.predict(new_future_dates)
forecast[['ds','yhat','yhat_lower','yhat_upper']].tail()

figure1 = model.plot(forecast, xlabel='Date', ylabel=target_value)