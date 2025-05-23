"""Utility functions for analyzing sales data CSV files."""

import argparse
import datetime
import logging
import os
from typing import Tuple

import matplotlib.pyplot as plt
import pandas as pd

logging.basicConfig(level=logging.INFO)


def _ensure_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure a Revenue column exists, deriving it if needed."""
    if "Revenue" not in df.columns and {"Quantity", "Price"}.issubset(df.columns):
        df["Revenue"] = df["Quantity"] * df["Price"]
    return df


def process_data(file_path: str) -> pd.DataFrame:
    """Aggregate revenue per product and save a bar chart."""
    df = pd.read_csv(file_path)
    df = _ensure_revenue(df)
    revenue = df.groupby("Product")["Revenue"].sum().reset_index()
    revenue.to_csv("output.csv", index=False)

    plt.bar(revenue["Product"], revenue["Revenue"])
    plt.title("Revenue by Product")
    plt.savefig("bargraph.png")
    plt.close()
    return revenue


def calculate_discount(price: float, discount: float) -> float:
    """Return price after applying a percentage discount."""
    return price - (price * discount / 100)


def get_most_profitable_product(file_path: str) -> Tuple[str, float]:
    """Return the product with the highest total revenue."""
    df = pd.read_csv(file_path)
    df = _ensure_revenue(df)
    grouped = df.groupby("Product")["Revenue"].sum()
    return grouped.idxmax(), grouped.max()


def filter_last_30_days(file_path: str) -> pd.DataFrame:
    """Save and return sales from the last 30 days."""
    df = pd.read_csv(file_path)
    df["Date"] = pd.to_datetime(df["Date"])
    last_month = datetime.datetime.now() - datetime.timedelta(days=30)
    filtered = df[df["Date"] >= last_month]
    filtered.to_csv("last_30_days.csv", index=False)
    return filtered


def plot_sales(file_path: str) -> None:
    """Plot and save the daily revenue time series."""
    df = pd.read_csv(file_path)
    df = _ensure_revenue(df)
    df["Date"] = pd.to_datetime(df["Date"])
    df.sort_values("Date", inplace=True)
    df.groupby("Date")["Revenue"].sum().plot()
    plt.title("Daily Revenue")
    plt.savefig("daily.png")
    plt.close()


def calculate_tax(file_path: str) -> pd.DataFrame:
    """Add tax and net columns then write to ``taxed.csv``."""
    df = pd.read_csv(file_path)
    df = _ensure_revenue(df)
    df["Tax"] = df["Revenue"] * 0.18
    df["Net"] = df["Revenue"] - df["Tax"]
    df.to_csv("taxed.csv", index=False)
    logging.info("Tax file written")
    return df


def generate_summary(file_path: str) -> pd.DataFrame:
    """Print and save summary statistics per product."""
    df = pd.read_csv(file_path)
    df = _ensure_revenue(df)
    summary = df.groupby("Product")["Revenue"].agg(["sum", "count", "mean"])
    logging.info("\n%s", summary)
    summary.to_csv("summary.csv")
    return summary


def debug_info(file_path: str) -> pd.DataFrame:
    """Log detailed information about the CSV file."""
    df = pd.read_csv(file_path)
    logging.debug("Columns: %s", df.columns)
    logging.debug("Head: %s", df.head())
    logging.debug("Info: %s", df.info())
    logging.debug("Describe: %s", df.describe())
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Process sales data CSV")
    parser.add_argument("file", help="Path to CSV file")
    args = parser.parse_args()

    file_path = args.file
    if not os.path.exists(file_path):
        logging.error("File does not exist: %s", file_path)
        return

    logging.info("Processing %s", file_path)
    process_data(file_path)
    filter_last_30_days(file_path)
    plot_sales(file_path)
    get_most_profitable_product(file_path)
    calculate_tax(file_path)
    generate_summary(file_path)


if __name__ == "__main__":
    main()

