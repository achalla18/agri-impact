# AgriImpact: Crop Profit Comparison Tool

AgriImpact is a web app that helps small or rural farmers compare two crops side-by-side. It uses real government data to show expected profit, risk, and how much government support (like subsidies or insurance) can help.

## What the App Does

- Lets users choose two crops, a state, and a year
- Pulls real yield and price data from the USDA
- Calculates:
  - Profit with and without subsidies
  - Risk using 1,000 simulations (to show how prices and yields might change)
- Shows everything in a simple table for easy comparison

## Why This Matters

Many small farmers don’t have access to tools that show:
- How much money they might make from different crops
- How risky each crop is
- How government programs can help reduce financial loss

AgriImpact helps solve that by giving them a free, easy-to-use tool that uses real data and shows clear results.

## How It Works

- **Backend:** Python + Flask
- **Simulation:** NumPy (to run thousands of scenarios)
- **Data Source:** USDA QuickStats API
- **Frontend:** HTML with dropdown menus and hover-over tips
