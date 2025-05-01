from flask import Flask, render_template, request
from utils import calculate_profit, subsidy_income_adjustment, simulate_risk_scenarios, get_usda_data
import numpy as np

app = Flask(__name__)

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    results = []
    if request.method == 'POST':
        crops = request.form.getlist('crop')
        state = request.form['state']
        year = request.form['year']
        acres = int(request.form['acres'])
        cost_per_acre = float(request.form['cost'])
        subsidy_type = request.form['subsidy']
        std_yield = float(request.form.get('std_yield', 15))
        std_price = float(request.form.get('std_price', 1.0))

        for crop in crops:
            yield_per_acre = get_usda_data(crop, "YIELD", "BU / ACRE", state, year)
            price_per_unit = get_usda_data(crop, "PRICE RECEIVED", "$ / BU", state, year)

            if yield_per_acre and price_per_unit:
                base_profit = calculate_profit(yield_per_acre, acres, price_per_unit, cost_per_acre)
                adjusted_profit = subsidy_income_adjustment(base_profit, subsidy_type, acres)
                profits = simulate_risk_scenarios(yield_per_acre, price_per_unit, std_yield, std_price, acres, cost_per_acre)
                avg_profit = np.mean(profits)
                loss_chance = np.mean(profits < 0) * 100

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
                results.append({'crop': crop, 'error': 'Missing data'})

    return render_template('compare.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
