import streamlit as st
import pandas as pd
import altair as alt

st.title('Sales Data Analysis')

uploaded_file = st.file_uploader('Upload a CSV file', type=['csv'])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.subheader('Raw Data')
    st.write(data.head())

    if {'Product','Quantity','Price','Date'}.issubset(data.columns):
        data['Revenue'] = data['Quantity'] * data['Price']

        # Total revenue per product
        revenue_per_product = data.groupby('Product')['Revenue'].sum().reset_index()
        st.subheader('Total Revenue per Product')
        st.write(revenue_per_product)

        # Sales trend over time
        data['Date'] = pd.to_datetime(data['Date'])
        trend = data.groupby('Date')['Revenue'].sum().reset_index()
        line_chart = alt.Chart(trend).mark_line().encode(x='Date:T', y='Revenue:Q')
        st.subheader('Sales Trend Over Time')
        st.altair_chart(line_chart, use_container_width=True)

        # Top 5 best-selling products (by quantity)
        top_products = data.groupby('Product')['Quantity'].sum().nlargest(5).reset_index()
        bar_chart = alt.Chart(top_products).mark_bar().encode(x='Product:N', y='Quantity:Q')
        st.subheader('Top 5 Best-Selling Products')
        st.altair_chart(bar_chart, use_container_width=True)
    else:
        st.error('CSV must contain Date, Product, Quantity, and Price columns')
else:
    st.info('Please upload a CSV file to begin.')
