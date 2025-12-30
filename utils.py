# Import necessary libraries
import numpy as np
import requests

# Function to calculate profit based on yield, acres, market price, and cost per acre
def calculate_profit(yield_per_acre, acres, market_price, cost_per_acre):
    revenue = yield_per_acre * acres * market_price  # Total revenue
    cost = acres * cost_per_acre  # Total cost
    return revenue - cost  # Net profit

# Function to adjust profit based on subsidy type and acres
def subsidy_income_adjustment(profit, subsidy_type, acres):
    if subsidy_type == "ARC":
        return profit + 50 * acres  # Add ARC subsidy
    elif subsidy_type == "PLC":
        return profit + 40 * acres  # Add PLC subsidy
    elif subsidy_type == "Crop Insurance":
        return profit + 0.6 * max(0, -profit)  # Add crop insurance subsidy
    return profit  # No subsidy adjustment

# Function to simulate profits under risk scenarios using normal distribution
def simulate_risk_scenarios(yield_per_acre, price, std_yield, std_price, acres, cost_per_acre, num_simulations=1000):
    simulated_yields = np.random.normal(yield_per_acre, std_yield, num_simulations)  # Simulated yields
    simulated_prices = np.random.normal(price, std_price, num_simulations)  # Simulated prices
    profits = (simulated_yields * acres * simulated_prices) - (acres * cost_per_acre)  # Simulated profits
    return profits

# Function to fetch USDA data for a specific crop, statistic, unit, state, and year
def get_usda_data(crop, stat_type, unit_desc, state, year):
    api_key = "API_KEY"  # Replace with USDA QuickStats API key
    base_url = "http://quickstats.nass.usda.gov/api/api_GET/"  # USDA API endpoint
    params = {
        "key": api_key,
        "commodity_desc": crop,  # Crop name
        "statisticcat_desc": stat_type,  # Statistic type (e.g., yield, price)
        "unit_desc": unit_desc,  # Unit description (e.g., BU/ACRE, $/BU)
        "state_name": state,  # State name
        "year": year,  # Year
        "format": "JSON"  # Response format
    }
    try:
        # Make API request
        response = requests.get(base_url, params=params)
        data = response.json()
        # Check if data is available
        if "data" in data and len(data["data"]) > 0:
            return float(data["data"][0]["Value"].replace(",", ""))  # Return the first value
    except Exception:
        return None  # Return None if an error occurs
    return None  # Return None if no data is found
