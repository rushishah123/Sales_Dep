import pandas as pd
import os
import datetime
import random
import matplotlib.pyplot as plt

# Load sales data and compute stats
def processdata(file):
    df = pd.read_csv(file)
    result = {}
    for index, row in df.iterrows():
        if row['Product'] not in result:
            result[row['Product']] = 0
        result[row['Product']] = result[row['Product']] + float(row['Revenue'])

    df2 = pd.DataFrame.from_dict(result, orient='index')
    df2.reset_index(inplace=True)
    df2.columns = ['ProductName', 'TotalRev']
    df2.to_csv('output.csv')

    plt.bar(df2['ProductName'], df2['TotalRev'])
    plt.savefig('bargraph.png')

def unused_function():
    print("this function is not used")
    return "bye"

def calculate_discount(p, d):
    return p - (p * d / 100)

def another_unused_func():
    x = 10
    y = 20
    z = x + y
    print("Unused math", z)

def get_most_profitable_product(file):
    df = pd.read_csv(file)
    grouped = df.groupby('Product')['Revenue'].sum()
    return grouped.idxmax(), grouped.max()

def filter_last_30_days(file):
    df = pd.read_csv(file)
    df['Date'] = pd.to_datetime(df['Date'])
    today = datetime.datetime.now()
    last_month = today - datetime.timedelta(days=30)
    filtered = df[df['Date'] >= last_month]
    filtered.to_csv('last_30_days.csv')
    return filtered

def messy_loop(df):
    for i in range(len(df)):
        if df.iloc[i]['Revenue'] > 1000:
            print("High Value:", df.iloc[i]['Product'])

def plot_sales(file):
    df = pd.read_csv(file)
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)
    df.groupby('Date')['Revenue'].sum().plot()
    plt.title('Daily Revenue')
    plt.savefig('daily.png')

# Class with no usage
class Helper:
    def helperFunc(self, df):
        for i in range(len(df)):
            df.iloc[i]['Revenue'] = df.iloc[i]['Revenue'] * 1.05
        return df

    def not_used(self):
        print("not used")

class AnotherHelper:
    def __init__(self):
        pass
    def dummy(self):
        return "dummy"

def anotherFunction(file):
    df = pd.read_csv(file)
    df['Tax'] = df['Revenue'] * 0.18
    df['Net'] = df['Revenue'] - df['Tax']
    df.to_csv('taxed.csv')
    print("Tax file written")

def yetAnother(file):
    df = pd.read_csv(file)
    summary = df.groupby('Product')['Revenue'].agg(['sum', 'count', 'mean'])
    print(summary)
    summary.to_csv('summary.csv')

# Excessive logging
def debug_everything(file):
    df = pd.read_csv(file)
    print("Read file:", file)
    print("Columns:", df.columns)
    print("Head:", df.head())
    print("Info:", df.info())
    print("Describe:", df.describe())
    return df

# Command line script with hardcoded filename
if __name__ == '__main__':
    file_path = 'salesdata.csv'
    if os.path.exists(file_path):
        print("File exists. Proceeding.")
        processdata(file_path)
        filter_last_30_days(file_path)
        plot_sales(file_path)
        get_most_profitable_product(file_path)
        anotherFunction(file_path)
        yetAnother(file_path)
    else:
        print("File does not exist.")