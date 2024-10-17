import yfinance as yf
import numpy as np
import pandas as pd


def get_fundamentals_dict(tickers:list, wanted_metrics=[]) -> dict:
    """
    Calculate various metrics from a given ticker using yfinance to get the fundamental data.

    This function takes a ticker as input and computes several metrics,
    including ratios and other relevant calculations. Most metrics are not directly readable
    from financial statements and require some form of calculation.

    Parameters:
    ticker (str): The stock ticker to calculate metrics for.
    wanted_metrics (list): A list of metrics to calculate. If empty, all metrics are calculated.

    Returns:
    dict: A dictionary containing the calculated metrics.

    Example:
    >>> metrics = get_fundamentals_dict('AAPL', ['PE Ratio', 'Debt to Equity'])
    >>> print(metrics)
    {'PE Ratio': 28.5, 'Debt to Equity': 1.5}
    """

    # Fetch data from yfinance
    stocks = yf.Tickers(" ".join(tickers))
    metrics_per_ticker = {}
    for ticker in tickers:
        stock = stocks.tickers[ticker]
        financials = stock.financials
        balance_sheet = stock.balance_sheet
        cash_flow = stock.cashflow
        info = stock.info
        # dict_keys(['address1', 'city', 'state', 'zip', 'country', 'phone', 'website', 'industry', 'industryKey', 'industryDisp', 'sector', 'sectorKey', 'sectorDisp', 'longBusinessSummary', 'fullTimeEmployees', 'companyOfficers', 'auditRisk', 'boardRisk', 'compensationRisk', 'shareHolderRightsRisk', 'overallRisk', 'governanceEpochDate', 'compensationAsOfEpochDate', 'irWebsite', 'maxAge', 'priceHint', 'previousClose', 'open', 'dayLow', 'dayHigh', 'regularMarketPreviousClose', 'regularMarketOpen', 'regularMarketDayLow', 'regularMarketDayHigh', 'dividendRate', 'dividendYield', 'exDividendDate', 'payoutRatio', 'fiveYearAvgDividendYield', 'beta', 'trailingPE', 'forwardPE', 'volume', 'regularMarketVolume', 'averageVolume', 'averageVolume10days', 'averageDailyVolume10Day', 'marketCap', 'fiftyTwoWeekLow', 'fiftyTwoWeekHigh', 'priceToSalesTrailing12Months', 'fiftyDayAverage', 'twoHundredDayAverage', 'trailingAnnualDividendRate', 'trailingAnnualDividendYield', 'currency', 'enterpriseValue', 'profitMargins', 'floatShares', 'sharesOutstanding', 'sharesShort', 'sharesShortPriorMonth', 'sharesShortPreviousMonthDate', 'dateShortInterest', 'sharesPercentSharesOut', 'heldPercentInsiders', 'heldPercentInstitutions', 'shortRatio', 'shortPercentOfFloat', 'impliedSharesOutstanding', 'bookValue', 'priceToBook', 'lastFiscalYearEnd', 'nextFiscalYearEnd', 'mostRecentQuarter', 'earningsQuarterlyGrowth', 'netIncomeToCommon', 'trailingEps', 'forwardEps', 'pegRatio', 'lastSplitFactor', 'lastSplitDate', 'enterpriseToRevenue', 'enterpriseToEbitda', '52WeekChange', 'SandP52WeekChange', 'lastDividendValue', 'lastDividendDate', 'exchange', 'quoteType', 'symbol', 'underlyingSymbol', 'shortName', 'longName', 'firstTradeDateEpochUtc', 'timeZoneFullName', 'timeZoneShortName', 'uuid', 'messageBoardId', 'gmtOffSetMilliseconds', 'currentPrice', 'targetHighPrice', 'targetLowPrice', 'targetMeanPrice', 'targetMedianPrice', 'recommendationMean', 'recommendationKey', 'numberOfAnalystOpinions', 'totalCash', 'totalCashPerShare', 'ebitda', 'totalDebt', 'quickRatio', 'currentRatio', 'totalRevenue', 'debtToEquity', 'revenuePerShare', 'returnOnAssets', 'returnOnEquity', 'freeCashflow', 'operatingCashflow', 'earningsGrowth', 'revenueGrowth', 'grossMargins', 'ebitdaMargins', 'operatingMargins', 'financialCurrency', 'trailingPegRatio'])

        metrics = {}

        def fetch_financial_data(item, statement):
            try:
                return statement.loc[item].iloc[0]
            except KeyError:
                return np.nan

        for metric in wanted_metrics:
            if metric == "CA":
                metrics["CA"] = fetch_financial_data("Total Current Assets", balance_sheet) - fetch_financial_data("Cash And Cash Equivalents", balance_sheet)
            elif metric == "CL":
                metrics["CL"] = fetch_financial_data("Total Current Liabilities", balance_sheet) - fetch_financial_data("Long Term Debt", balance_sheet) - fetch_financial_data("Income Taxes Payable", balance_sheet)
            elif metric == "DEP":
                metrics["DEP"] = fetch_financial_data("Depreciation", cash_flow)
            elif metric == "STA":
                CA = fetch_financial_data("Total Current Assets", balance_sheet) - fetch_financial_data("Cash And Cash Equivalents", balance_sheet)
                CL = fetch_financial_data("Total Current Liabilities", balance_sheet) - fetch_financial_data("Long Term Debt", balance_sheet) - fetch_financial_data("Income Taxes Payable", balance_sheet)
                DEP = fetch_financial_data("Depreciation", cash_flow)
                total_assets = fetch_financial_data("Total Assets", balance_sheet)
                metrics["STA"] = (CA - CL - DEP) / total_assets if total_assets != 0 else np.nan
            elif metric == "SNOA":
                # Not implemented
                metrics["SNOA"] = np.nan
            elif metric == "COMBOACCRUAL":
                # Not implemented
                metrics["COMBOACCRUAL"] = np.nan
            elif metric == "DSRI":
                # Not implemented
                metrics["DSRI"] = np.nan
            elif metric == "GMI":
                # Not implemented
                metrics["GMI"] = np.nan
            elif metric == "AQI":
                # Not implemented
                metrics["AQI"] = np.nan
            elif metric == "SGI":
                # Not implemented
                metrics["SGI"] = np.nan
            elif metric == "DEPI":
                # Not implemented
                metrics["DEPI"] = np.nan
            elif metric == "SGAI":
                # Not implemented
                metrics["SGAI"] = np.nan
            elif metric == "LVGI":
                # Not implemented
                metrics["LVGI"] = np.nan
            elif metric == "TATA":
                # Not implemented
                metrics["TATA"] = np.nan
            elif metric == "PROBM":
                # Not implemented
                metrics["PROBM"] = np.nan
            elif metric == "PMAN":
                # Not implemented
                metrics["PMAN"] = np.nan
            elif metric == "NIMTAAVG":
                # Not implemented
                metrics["NIMTAAVG"] = np.nan
            elif metric == "MTA":
                liabilities = fetch_financial_data("Total Liab", balance_sheet)
                market_cap = info.get("marketCap", np.nan)
                metrics["MTA"] = liabilities + market_cap
            elif metric == "TLMTA":
                total_liabilities = fetch_financial_data("Total Liab", balance_sheet)
                mta = liabilities + market_cap
                metrics["TLMTA"] = total_liabilities / mta if mta != 0 else np.nan
            elif metric == "CASHMTA":
                cash_and_equivalents = fetch_financial_data("Cash And Cash Equivalents", balance_sheet)
                metrics["CASHMTA"] = cash_and_equivalents / mta if mta != 0 else np.nan
            elif metric == "EXRETAVG":
                # Not implemented
                metrics["EXRETAVG"] = np.nan
            elif metric == "SIGMA":
                # Not implemented
                metrics["SIGMA"] = np.nan
            elif metric == "RSIZE":
                # Not implemented
                metrics["RSIZE"] = np.nan
            elif metric == "MB":
                book_value = fetch_financial_data("Total Stockholder Equity", balance_sheet)
                adjusted_book_value = book_value + 0.1 * (market_cap - book_value)
                metrics["MB"] = mta / adjusted_book_value if adjusted_book_value != 0 else np.nan
            elif metric == "PRICE":
                recent_price = info.get("previousClose", np.nan)
                metrics["PRICE"] = np.log(recent_price) if recent_price > 0 else np.nan
            elif metric == "LPFD":
                # Not implemented
                metrics["LPFD"] = np.nan
            elif metric == "PFD":
                # Not implemented
                metrics["PFD"] = np.nan
            elif metric == "EBIT":
                metrics["EBIT"] = fetch_financial_data("EBIT", financials)
            elif metric == "TEV":
                total_debt = fetch_financial_data("Total Debt", balance_sheet)
                metrics["TEV"] = market_cap + total_debt - cash_and_equivalents
            elif metric == "8yr_ROA":
                # Not implemented
                metrics["8yr_ROA"] = np.nan
            elif metric == "P_8yr_ROA":
                # Not implemented
                metrics["P_8yr_ROA"] = np.nan
            elif metric == "8yr_ROC":
                # Not implemented
                metrics["8yr_ROC"] = np.nan
            elif metric == "P_8yr_ROC":
                # Not implemented
                metrics["P_8yr_ROC"] = np.nan
            elif metric == "FCFA":
                # Not implemented
                metrics["FCFA"] = np.nan
            elif metric == "P_CFOA":
                # Not implemented
                metrics["P_CFOA"] = np.nan
            elif metric == "MG":
                # Not implemented
                metrics["MG"] = np.nan
            elif metric == "P_MG":
                # Not implemented
                metrics["P_MG"] = np.nan
            elif metric == "MS":
                # Not implemented
                metrics["MS"] = np.nan
            elif metric == "P_MS":
                # Not implemented
                metrics["P_MS"] = np.nan
            elif metric == "MM":
                # Not implemented
                metrics["MM"] = np.nan
            elif metric == "P_FP":
                # Not implemented
                metrics["P_FP"] = np.nan
            elif metric == "ROA":
                net_income = fetch_financial_data("Net Income", financials)
                total_assets = fetch_financial_data("Total Assets", balance_sheet)
                metrics["ROA"] = net_income / total_assets if total_assets != 0 else np.nan
            elif metric == "FS_ROA":
                net_income = fetch_financial_data("Net Income", financials)
                total_assets = fetch_financial_data("Total Assets", balance_sheet)
                metrics["FS_ROA"] = 1 if net_income / total_assets > 0 else 0
            elif metric == "FCFTA":
                free_cash_flow = fetch_financial_data("Free Cash Flow", cash_flow)
                total_assets = fetch_financial_data("Total Assets", balance_sheet)
                metrics["FCFTA"] = free_cash_flow / total_assets if total_assets != 0 else np.nan
            elif metric == "FS_FCFTA":
                free_cash_flow = fetch_financial_data("Free Cash Flow", cash_flow)
                total_assets = fetch_financial_data("Total Assets", balance_sheet)
                metrics["FS_FCFTA"] = 1 if free_cash_flow / total_assets > 0 else 0
            elif metric == "ACCRUAL":
                free_cash_flow = fetch_financial_data("Free Cash Flow", cash_flow)
                net_income = fetch_financial_data("Net Income", financials)
                total_assets = fetch_financial_data("Total Assets", balance_sheet)
                fcfta = free_cash_flow / total_assets if total_assets != 0 else np.nan
                roa = net_income / total_assets if total_assets != 0 else np.nan
                metrics["ACCRUAL"] = fcfta - roa
            elif metric == "FS_ACCRUAL":
                free_cash_flow = fetch_financial_data("Free Cash Flow", cash_flow)
                net_income = fetch_financial_data("Net Income", financials)
                total_assets = fetch_financial_data("Total Assets", balance_sheet)
                fcfta = free_cash_flow / total_assets if total_assets != 0 else np.nan
                roa = net_income / total_assets if total_assets != 0 else np.nan
                accrual = fcfta - roa
                metrics["FS_ACCRUAL"] = 1 if accrual > 0 else 0
            elif metric == "LEVER":
                long_term_debt_t_1 = fetch_financial_data("Long Term Debt", balance_sheet.shift(1))
                total_assets_t_1 = fetch_financial_data("Total Assets", balance_sheet.shift(1))
                long_term_debt_t = fetch_financial_data("Long Term Debt", balance_sheet)
                total_assets_t = fetch_financial_data("Total Assets", balance_sheet)
                metrics["LEVER"] = (long_term_debt_t_1 / total_assets_t_1) - (long_term_debt_t / total_assets_t) if total_assets_t_1 != 0 and total_assets_t != 0 else np.nan
            elif metric == "FS_LEVER":
                long_term_debt_t_1 = fetch_financial_data("Long Term Debt", balance_sheet.shift(1))
                total_assets_t_1 = fetch_financial_data("Total Assets", balance_sheet.shift(1))
                long_term_debt_t = fetch_financial_data("Long Term Debt", balance_sheet)
                total_assets_t = fetch_financial_data("Total Assets", balance_sheet)
                lever = (long_term_debt_t_1 / total_assets_t_1) - (long_term_debt_t / total_assets_t) if total_assets_t_1 != 0 and total_assets_t != 0 else np.nan
                metrics["FS_LEVER"] = 1 if lever > 0 else 0
            elif metric == "LIQUID":
                current_ratio_t = fetch_financial_data("Total Current Assets", balance_sheet) / fetch_financial_data("Total Current Liabilities", balance_sheet)
                current_ratio_t_1 = fetch_financial_data("Total Current Assets", balance_sheet.shift(1)) / fetch_financial_data("Total Current Liabilities", balance_sheet.shift(1))
                metrics["LIQUID"] = current_ratio_t - current_ratio_t_1
            elif metric == "FS_LIQUID":
                current_ratio_t = fetch_financial_data("Total Current Assets", balance_sheet) / fetch_financial_data("Total Current Liabilities", balance_sheet)
                current_ratio_t_1 = fetch_financial_data("Total Current Assets", balance_sheet.shift(1)) / fetch_financial_data("Total Current Liabilities", balance_sheet.shift(1))
                liquid = current_ratio_t - current_ratio_t_1
                metrics["FS_LIQUID"] = 1 if liquid > 0 else 0
            elif metric == "NEQISS":
                # Not implemented
                metrics["NEQISS"] = np.nan
            elif metric == "FS_NEQISS":
                # Not implemented
                metrics["FS_NEQISS"] = np.nan
            elif metric == "FS_MARGIN":
                # Not implemented
                metrics["FS_MARGIN"] = np.nan
            elif metric == "FS_TURN":
                # Not implemented
                metrics["FS_TURN"] = np.nan
            elif metric == "P_FS":
                # Not implemented
                metrics["P_FS"] = np.nan
            elif metric == "QUALITY":
                # Not implemented
                metrics["QUALITY"] = np.nan
            elif metric == "PE Ratio":
                market_cap = info.get("marketCap", np.nan)
                net_income = fetch_financial_data("Net Income", financials)
                metrics["PE Ratio"] = market_cap / net_income if net_income != 0 else np.nan
            elif metric == "Cash Ratio":
                cash_and_equivalents = fetch_financial_data("Cash And Cash Equivalents", balance_sheet)
                total_current_liabilities = fetch_financial_data("Current Liabilities", balance_sheet)
                metrics["Cash Ratio"] = cash_and_equivalents / total_current_liabilities if total_current_liabilities != 0 else np.nan
            elif metric == "Quick Ratio":
                cash_and_equivalents = fetch_financial_data("Current Assets", balance_sheet)
                inventory = fetch_financial_data("Inventory", balance_sheet)
                current_liabilities = fetch_financial_data("Current Liabilities", balance_sheet)
                metrics["Quick Ratio"] = (cash_and_equivalents - inventory) / current_liabilities if current_liabilities != 0 else np.nan
            elif metric == "Current Ratio":
                total_current_assets = fetch_financial_data("Current Assets", balance_sheet)
                total_current_liabilities = fetch_financial_data("Current Liabilities", balance_sheet)
                metrics["Current Ratio"] = total_current_assets / total_current_liabilities if total_current_liabilities != 0 else np.nan
            elif metric == "Financial Leverage":
                total_debt = fetch_financial_data("Total Debt", balance_sheet)
                total_current_assets = fetch_financial_data("Current Assets", balance_sheet)
                metrics["Financial Leverage"] = total_debt / total_current_assets if total_current_assets != 0 else np.nan
            elif metric == "PB Ratio":
                total_assets = fetch_financial_data("Total Assets", balance_sheet)
                market_cap = info.get("marketCap", np.nan)
                metrics["PB Ratio"] = market_cap / total_assets if total_assets != 0 else np.nan
            elif metric == "Dividend Yield":
                metrics["Dividend Yield"] = info.get("dividendYield", np.nan)
            elif metric == "Market Cap":
                metrics["Market Cap"] = info.get("marketCap", np.nan)
            #TODO: add info.get("earningsGrowth"- not sure what timeframe this is
            else:
                raise ValueError(f"Invalid metric: {metric}")
        metrics_per_ticker[ticker] = metrics
    return metrics_per_ticker

def filter_tickers(input_tickers: list, ratio_filters: dict):
    valid_booleans = {
        ticker: np.nan for ticker in input_tickers
    } # set these to False if any condition is not met
    filter_outputs = {}
    
    metrics_per_ticker = get_fundamentals_dict(input_tickers, list(ratio_filters.keys()))
    for ticker in input_tickers:
        metrics = metrics_per_ticker[ticker]
        filter_output_current = {}
        for metric, condition in ratio_filters.items():
            if metrics[metric] is np.nan:
                check = np.nan
            else:
                if "<" in condition and not "=" in condition:
                    check = metrics[metric] < float(condition[1:])
                elif "<=" in condition:
                    check = metrics[metric] <= float(condition[2:])
                elif ">" in condition and not "=" in condition:
                    check = metrics[metric] > float(condition[1:])
                elif ">=" in condition:
                    check = metrics[metric] >= float(condition[2:])
                elif "==" in condition:
                    check = metrics[metric] == float(condition[2:])
                else:
                    raise ValueError(f"Invalid condition: {condition}")
            filter_output_current[metric + condition] = check
        filter_outputs[ticker] = filter_output_current
        # 'PE Ratio<=9' =
        # False
        # 'Financial Leverage<1.10' =
        # True
        # 'PB Ratio<1.20' =
        # False
        # 'Current Ratio>1.50' =
        # False
        # 'Dividend Yield>0' =
        # True
        valid_booleans[ticker] = all(filter_outputs[ticker].values())
    return [ticker for ticker in input_tickers if valid_booleans[ticker] == True], [ticker for ticker in input_tickers if valid_booleans[ticker] == False or np.isnan(valid_booleans[ticker])], filter_outputs

if __name__ == "__main__":
    wanted_filters = {"PE Ratio":"<=9", "Financial Leverage":"<1.10", "PB Ratio": "<1.20", "Current Ratio": ">1.50", "Dividend Yield": ">0"}
    # try for magnificent seven
    mag_seven_tickers = ["AAPL", "MSFT", "AMZN", "TSLA", "GOOG", "FB", "NVDA"]
    # Read and print the stock tickers that make up S&P500
    html_ = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    sp500_tickers = html_.Symbol.to_list()
    valid_tickers, filtered_tickers, filter_outputs = filter_tickers(sp500_tickers, wanted_filters)
    print(filter_outputs)
    for ticker in valid_tickers:
        print(f"Valid: {ticker}")
    