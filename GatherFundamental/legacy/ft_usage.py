# pip install financetoolkit -U
# for documentation, see https://github.com/JerBouma/FinanceToolkit

from financetoolkit import Toolkit
import os
from dotenv import load_dotenv
load_dotenv()
# To be able to get started, you need to obtain an API Key from FinancialModelingPrep. 
# This is used to gain access to 30+ years of financial statement both annually and quarterly. 
# Note that the Free plan is limited to 250 requests each day, 5 years of data and only features companies listed on US exchanges.

# set the API key manually to FINANCIAL_MODELING_PREP_API_KEY='Rp0SrVO9B19jGJRdI8GIgw2zXJkBJuwI'
API_KEY = os.getenv('FINANCIAL_MODELING_PREP_KEY')
print(API_KEY)
companies = Toolkit(["AAPL", "MSFT"], api_key=API_KEY, start_date="2017-12-31")


# a Financial Statement example
income_statement = companies.get_income_statement()
print(income_statement)
quit()

# a Historical example
historical_data = companies.get_historical_data()


# a Ratios example
profitability_ratios = companies.ratios.collect_profitability_ratios()

# a Models example
extended_dupont_analysis = companies.models.get_extended_dupont_analysis()

# an Options example
all_greeks = companies.options.collect_all_greeks(expiration_time_range=180)

# a Performance example
factor_asset_correlations = companies.performance.get_factor_asset_correlations(
    period="quarterly"
)

# a Risk example
value_at_risk = companies.risk.get_value_at_risk(period="weekly")

# a Technical example
ichimoku_cloud = companies.technicals.get_ichimoku_cloud()

# a Fixed Income example
corporate_bond_yields = companies.fixed_income.get_ice_bofa_effective_yield()

# a Fixed Income example
corporate_bond_yields = companies.fixed_income.get_ice_bofa_effective_yield()

# an Economics example
unemployment_rates = companies.economics.get_unemployment_rate()