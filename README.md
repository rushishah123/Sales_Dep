# Sales_Dep

This repository contains a simple Streamlit app for analyzing sales data from a CSV file.

## Demo Data

A sample file `demo_sales.csv` is included with 50 entries. Each row contains:

- `Date`: order date (YYYY-MM-DD)
- `Product`: product name
- `Quantity`: units sold
- `Price`: unit price

## Running the App

Install the required packages (Streamlit, pandas, altair) if you don't have them:

```bash
pip install streamlit pandas altair
```

Start the Streamlit app:

```bash
streamlit run app.py
```

Upload your own CSV file or use the provided `demo_sales.csv` to see the analysis, which includes:

- Total revenue per product
- Sales trend over time
- Top 5 best-selling products
