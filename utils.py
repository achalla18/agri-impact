import numpy as np
import requests

def calculate_profit(yield_per_acre, acres, market_price, cost_per_acre):
    revenue = yield_per_acre * acres * market_price
    cost = acres * cost_per_acre
    return revenue - cost

def subsidy_income_adjustment(profit, subsidy_type, acres):
    if subsidy_type == "ARC":
        return profit + 50 * acres
    elif subsidy_type == "PLC":
        return profit + 40 * acres
    elif subsidy_type == "Crop Insurance":
        return profit + 0.6 * max(0, -profit)
    return profit

def simulate_risk_scenarios(yield_per_acre, price, std_yield, std_price, acres, cost_per_acre, num_simulations=1000):
    simulated_yields = np.random.normal(yield_per_acre, std_yield, num_simulations)
    simulated_prices = np.random.normal(price, std_price, num_simulations)
    profits = (simulated_yields * acres * simulated_prices) - (acres * cost_per_acre)
    return profits

def get_usda_data(crop, stat_type, unit_desc, state, year):
    api_key = "API_KEY"  # Replace with  USDA QuickStats API key
    base_url = "http://quickstats.nass.usda.gov/api/api_GET/"
    params = {
        "key": api_key,
        "commodity_desc": crop,
        "statisticcat_desc": stat_type,
        "unit_desc": unit_desc,
        "state_name": state,
        "year": year,
        "format": "JSON"
    }
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        if "data" in data and len(data["data"]) > 0:
            return float(data["data"][0]["Value"].replace(",", ""))
    except Exception:
        return None
    return None
