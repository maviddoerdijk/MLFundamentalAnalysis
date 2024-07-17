"""
Source: https://medium.com/@Batmaxx/using-machine-learning-and-company-fundamentals-for-beating-the-stock-market-fa2d4ac438a7

"""
# best so far!


import pandas as pd

# read dataset
df = pd.read_csv("data\dataset.csv", parse_dates=["date"])

# format index
df = df.set_index(["ticker", "date"])


# if the price increases by more than x%, we label it as "True" or "Buy"
threshold = 0.05  # 5%

# calculate the return within the month
df["return_month"] = (df["adjClose"] / df["adjOpen"]) - 1

# create the target
df["target"] = df["return_month"] >= threshold


# list of features
features = [
    "price_rate_of_change_1M",
    "price_rate_of_change_3M",
    "epsDil",
    "return_on_assets",
    "return_on_equity",
    "price_to_earnings_ratio",
    "debt_to_equity_ratio",
]

# shift the value of the features by one period (make sure to use groupby!)
df[features] = df.groupby("ticker")[features].shift(1)



from pandas_profiling import ProfileReport

profile = ProfileReport(df, title="Pandas Profiling Report", minimal=True)

profile.to_notebook_iframe()


split_date = 2020

df_train = df.loc[df.index.get_level_values("date").year < split_date]
df_test = df.loc[df.index.get_level_values("date").year == split_date]



from lightgbm import LGBMClassifier
# Note: Any model can be used here

# define classifier
estimator = LGBMClassifier(
    is_unbalance=True,
    max_depth=4,
    num_leaves=8,
    min_child_samples=400,
    n_estimators=50,
)

# fit classifier on training data
estimator.fit(df_train[features], df_train["target"])


# make prediction using test data
df_test["buy"] = estimator.predict(df_test[features])


from sklearn.metrics import classification_report

print(classification_report(df_test["target"], df_test["buy"]))


# select only the stocks that were picked by the model
df_buy = df_test.loc[df_test["buy"] == True][["return_month", "target", "buy"]]


df_results = (
    df_buy.reset_index()
    .groupby("date")
    .agg({"ticker": "count", "return_month": "mean"})
)

df_results.describe()


import numpy as np

def sharpe(s_return: pd.Series, annualize: int, rf: float = 0) -> float:
    """
    Calculate sharpe ratio

    :param s_return: pd.Series with return
    :param annualize: int periods to use for annualization (252 daily, 12 monthly, 4 quarterly)
    :param rf: float risk-free rate
    :return: float sharpe ratio
    """
    # (mean - rf) / std
    sharpe_ratio = (s_return.mean() - rf) / s_return.std()

    # annualize
    sharpe_ratio = sharpe_ratio * np.sqrt(annualize)

    return sharpe_ratio


sharpe_ratio = sharpe(df_results["return_month"], annualize=12)
print(f"Sharpe ratio: {round(sharpe_ratio, 2)}")
# Sharpe ratio: 1.16


# by using the monthly return, we can calculate the cumulative return over the entire year
df_results["return_month_cumulative"] = (df_results["return_month"] + 1).cumprod() - 1


import plotly.express as px

# plot monthly return
fig = px.bar(df_results, y="return_month", title="Monthly return (%)")
fig.show()

# plot cumulative return
fig = px.line(df_results, y="return_month_cumulative", title="Cumulative return")
fig.show()


# load the historical price DIA (benchmark strategy)
df_benchmark = pd.read_csv("data/prices_DIA.csv")


sharpe_ratio_benchmark = sharpe(df_benchmark["return_month"], annualize=12)
print(f"Sharpe ratio benchmark: {round(sharpe_ratio_benchmark, 2)}")


import plotly.graph_objects as go

fig = go.Figure()
fig = fig.add_trace(
    go.Scatter(y=df_results["return_month_cumulative"], name="ML Model"),
)
fig = fig.add_trace(
    go.Scatter(y=df_benchmark["return_month_cumulative"], name="Benchmark")
)
fig.update_layout(
    title="Cumulative Return",
)
fig.show()