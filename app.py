# Import necessary libraries and modules
from flask import Flask, render_template, request
from utils import calculate_profit, subsidy_income_adjustment, simulate_risk_scenarios, get_usda_data
import numpy as np

# Initialize the Flask application
app = Flask(__name__)

# Define the route for the crop comparison page
@app.route('/compare', methods=['GET', 'POST'])
def compare():
    # Initialize an empty list to store results
    results = []

    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Extract form data
        crops = request.form.getlist('crop')
        state = request.form['state']
        year = request.form['year']
        acres = int(request.form['acres'])
        cost_per_acre = float(request.form['cost'])
        subsidy_type = request.form['subsidy']
        std_yield = float(request.form.get('std_yield', 15))  # Default standard deviation for yield
        std_price = float(request.form.get('std_price', 1.0))  # Default standard deviation for price

        # Loop through each crop to calculate and simulate profits
        for crop in crops:
            # Fetch yield and price data from USDA API
            yield_per_acre = get_usda_data(crop, "YIELD", "BU / ACRE", state, year)
            price_per_unit = get_usda_data(crop, "PRICE RECEIVED", "$ / BU", state, year)

            # Check if data is available
            if yield_per_acre and price_per_unit:
                # Calculate base profit and adjusted profit with subsidies
                base_profit = calculate_profit(yield_per_acre, acres, price_per_unit, cost_per_acre)
                adjusted_profit = subsidy_income_adjustment(base_profit, subsidy_type, acres)

                # Simulate profits under risk scenarios
                profits = simulate_risk_scenarios(yield_per_acre, price_per_unit, std_yield, std_price, acres, cost_per_acre)
                avg_profit = np.mean(profits)  # Average simulated profit
                loss_chance = np.mean(profits < 0) * 100  # Percentage chance of loss

                # Append results for the crop
                results.append({
                    'crop': crop,
                    'yield': yield_per_acre,
                    'price': price_per_unit,
                    'base_profit': base_profit,
                    'adjusted_profit': adjusted_profit,
                    'avg_simulated_profit': avg_profit,
                    'chance_of_loss': loss_chance
                })
            else:
                # Append error if data is missing
                results.append({'crop': crop, 'error': 'Missing data'})

    # Render the comparison results in the HTML template
    return render_template('compare.html', results=results)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
