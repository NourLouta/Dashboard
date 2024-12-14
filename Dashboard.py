import streamlit as st
import pandas as pd
import plotly.express as px

# Load the cleaned data
df = pd.read_excel('cleaned_data.xlsx', engine='openpyxl')
# Sidebar for navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio(
    "Go to:",
    [
        "Overview",
        "Sales by Product Category",
        "Sales by Product Category in Each City", 
        "Top Products by Demand in Each Category",
        "Category Demand by Gender",
        "Sales by Customer Gender",
        "Sales Trend Over Time",
        "Top Sales Days",
        "Correlation Analysis",
        "Sales by Customer Type",
        "Sales Per Order by Customer Type",
        "Sales by Invoice Type",
        "Sales Across Stores",
        "Sales by Product Availability",
        "Sales by Customer Country",
        "Sales by Customer City",])

# Dashboard Title
st.title("E-commerce Pharmacy Dashboard")
st.markdown("This dashboard visualizes key insights and analyses from the dataset.")

# Visualizations based on selection
if options == "Overview":
    st.header("Overview")
    st.write("This section gives an overview of the dataset. Select any analysis from the sidebar to view its details.")
    st.dataframe(df.head(10))

elif options == "Sales by Product Category":
    category_sales = df.groupby('Product Category')['Total Sales'].sum().reset_index()
    fig = px.bar(category_sales, x='Product Category', y='Total Sales', title='Total Sales by Product Category')
    st.plotly_chart(fig)
    
    category_trend = df.groupby(['Invoice Date', 'Product Category'])['Total Sales'].sum().reset_index()
    fig_2 = px.line(category_trend,
    x='Invoice Date',
    y='Total Sales',
    color='Product Category',
    title='Sales Trend Over Time by Product Category')
    st.plotly_chart(fig_2)

elif options == "Sales by Product Category in Each City":
    category_city_sales = df.groupby(['Customer City', 'Product Category'])['Total Sales'].sum().reset_index()
     
    fig = px.bar(
    category_city_sales,
    x='Customer City',
    y='Total Sales',
    color='Product Category',
    title='Total Sales by Product Category in Each City',
    barmode='group')
    st.plotly_chart(fig)
    
elif options == "Top Products by Demand in Each Category":
    top_products = (
        df.groupby(['Product Category', 'Product Name'])['Item QTY per Invoice']
        .sum()
        .reset_index()
        .sort_values(['Product Category', 'Item QTY per Invoice'], ascending=[True, False])
    )
    top_5_products = top_products.groupby('Product Category').head(5)
    fig = px.bar(top_5_products, x='Product Name', y='Item QTY per Invoice', color='Product Category',
                 title='Top 5 Products by Demand in Each Category')
    st.plotly_chart(fig)

elif options == "Category Demand by Gender":
    category_gender_demand = df.groupby(['Product Category', 'Customer Gender'])['Item QTY per Invoice'].sum().reset_index()
    fig = px.bar(category_gender_demand, x='Product Category', y='Item QTY per Invoice', color='Customer Gender',
                 title='Category Demand by Gender', barmode='group')
    st.plotly_chart(fig)

elif options == "Sales by Customer Gender":
    gender_sales = df.groupby('Customer Gender')['Total Sales'].sum().reset_index()
    fig = px.bar(gender_sales, x='Customer Gender', y='Total Sales', title='Sales by Customer Gender')
    st.plotly_chart(fig)

elif options == "Sales Trend Over Time":
    sales_trend = df.groupby('Invoice Date')['Total Sales'].sum().reset_index()
    fig = px.line(sales_trend, x='Invoice Date', y='Total Sales', title='Sales Trend Over Time')
    st.plotly_chart(fig)

elif options == "Top Sales Days":
    top_days = df.groupby('Invoice Date')['Total Sales'].sum().nlargest(5).reset_index()
    fig = px.bar(top_days, x='Invoice Date', y='Total Sales', title='Top 5 Days with the Highest Sales')
    st.plotly_chart(fig)

elif options == "Correlation Analysis":
    numeric_columns = df.select_dtypes(include=['float64', 'int64'])
    correlation_matrix = numeric_columns.corr()
    fig = px.imshow(correlation_matrix, text_auto=True, title='Correlation Heatmap')
    st.plotly_chart(fig)

elif options == "Sales by Customer Type":
    customer_type_sales = df.groupby('Customer Type')['Total Sales'].sum().reset_index()
    fig = px.bar(customer_type_sales, x='Customer Type', y='Total Sales', title='Total Sales by Customer Type')
    st.plotly_chart(fig)
    
    customer_country_sales = df.groupby(['Customer Country', 'Customer Type'])['Total Sales'].sum().reset_index()
    fig_4 = px.bar(
    customer_country_sales,
    x='Customer Country',
    y='Total Sales',
    color='Customer Type',
    title='Total Sales by Customer Type and Country',
    barmode='group')
    st.plotly_chart(fig_4)

elif options == "Sales Per Order by Customer Type":
    order_sales = df.groupby('Customer Type')['Total Sales'].mean().reset_index()
    fig = px.bar(order_sales, x='Customer Type', y='Total Sales', title='Average Sales Per Order by Customer Type')
    st.plotly_chart(fig)

elif options == "Sales by Invoice Type":

    sales_by_invoice_items = (
        df.groupby('Invoice Type')['Invoice Items Count']
        .sum()
        .reset_index()
        .sort_values(by='Invoice Items Count', ascending=False)
    )
    fig_items = px.bar(
        sales_by_invoice_items,
        x='Invoice Type',
        y='Invoice Items Count',
        title='Number of Items Sold by Invoice Type',
        labels={'Invoice Items Count': 'Number of Items', 'Invoice Type': 'Invoice Type'},
        text='Invoice Items Count',
        color='Invoice Type'
    )
    fig_items.update_traces(textposition='outside')
    st.plotly_chart(fig_items)

    # Total Sales by Invoice Type
    sales_by_invoice_sales = (
        df.groupby('Invoice Type')['Total Sales']
        .sum()
        .reset_index()
        .sort_values(by='Total Sales', ascending=False)
    )
    fig_sales = px.bar(
        sales_by_invoice_sales,
        x='Invoice Type',
        y='Total Sales',
        title='Total Sales by Invoice Type',
        labels={'Total Sales': 'Total Sales (SAR)', 'Invoice Type': 'Invoice Type'},
        text='Total Sales',
        color='Invoice Type'
    )
    fig_sales.update_traces(textposition='outside')
    st.plotly_chart(fig_sales)

    # Pie Chart of Total Sales by Invoice Type
    fig_pie = px.pie(
        sales_by_invoice_sales,
        names='Invoice Type',
        values='Total Sales',
        title='Sales Distribution by Invoice Type',
        hole=0.4  # Donut chart style
    )
    st.plotly_chart(fig_pie)

elif options == "Sales Across Stores":
    store_sales = df.groupby('Store ID')['Total Sales'].sum().reset_index()
    fig = px.bar(store_sales, x='Store ID', y='Total Sales', title='Sales Across Stores')
    st.plotly_chart(fig)

elif options == "Sales by Product Availability":
    availability_sales = df.groupby('Product Availability')['Total Sales'].sum().reset_index()
    fig = px.bar(availability_sales, x='Product Availability', y='Total Sales',
                 title='Sales by Product Availability')
    st.plotly_chart(fig)

elif options == "Sales by Customer Country":
    sales_by_country = df.groupby('Customer Country')['Invoice Items Count'].sum().reset_index()
    fig = px.bar(sales_by_country, x='Customer Country', y='Invoice Items Count', title='Sales by Customer Country')
    st.plotly_chart(fig)
    
    country_sales = df.groupby('Customer Country')['Total Sales'].sum().reset_index()
    country_sales = country_sales.sort_values(by='Total Sales', ascending=False).head(5)
    fig_3 = px.bar(country_sales, x='Customer Country', y='Total Sales', title='Top 5 Countries by Total Sales')
    st.plotly_chart(fig_3)

elif options == "Sales by Customer City":
    sales_by_city = df.groupby('Customer City')['Total Sales'].sum().reset_index()
    fig_6 = px.bar(sales_by_city, x='Customer City', y='Total Sales', title='Total Sales by City')
    st.plotly_chart(fig_6)
    
    city_distribution = df['Customer City'].value_counts().reset_index()
    city_distribution.columns = ['City', 'Count']
    fig_7 = px.pie(city_distribution, names='City', values='Count', title='Customer Distribution by City')
    st.plotly_chart(fig_7)
