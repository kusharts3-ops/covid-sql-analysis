import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


orders = pd.read_csv(r'C:\Users\DELL\Downloads\ECommerceData\olist_orders_dataset.csv')
customers = pd.read_csv(r'C:\Users\DELL\Downloads\ECommerceData\olist_customers_dataset.csv')
payments = pd.read_csv(r'C:\Users\DELL\Downloads\ECommerceData\olist_order_payments_dataset.csv')
items = pd.read_csv(r'C:\Users\DELL\Downloads\ECommerceData\olist_order_items_dataset.csv')
products = pd.read_csv(r'C:\Users\DELL\Downloads\ECommerceData\olist_products_dataset.csv')
sellers = pd.read_csv(r'C:\Users\DELL\Downloads\ECommerceData\olist_sellers_dataset.csv')


print("===ORDERS DATASET===")
print(orders.shape)
print(orders.head())
print(orders.info())
print(orders.isnull().sum())


#Analysis 1 - Order Status
print("===Order Status===")
print(orders['order_status'].value_counts())


#Analysis 2 - Total Revenue
total_revenue = payments['payment_value'].sum()
print(f"Total Revenue:R${total_revenue}")


#Analysis 3 - Monthly Revenue
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['month'] = orders['order_purchase_timestamp'].dt.to_period('M')
monthly = orders.merge(payments,on ='order_id')
Monthly_Revenue = monthly.groupby('month')['payment_value'].sum()
print("===Monthly Revenue===")
print(Monthly_Revenue)


#Analysis 4 - Payment Types
print("\n=== PAYMENT TYPES ===")
print(payments['payment_type'].value_counts())


# Analysis 5 - Revenue by State
print("=== REVENUE BY STATE ===")
merged = orders.merge(
    payments, on='order_id'
).merge(
    customers, on='customer_id'
)
state_revenue = merged.groupby(
    'customer_state'
)['payment_value'].sum()\
.sort_values(ascending=False)
print(state_revenue)


#Analysis 6 - Delivery Time
print("\n=== DELIVERY TIME ===")
orders['order_purchase_timestamp'] = \
pd.to_datetime(
    orders['order_purchase_timestamp']
)
orders['order_delivered_customer_date'] = \
pd.to_datetime(
    orders['order_delivered_customer_date']
)
orders['delivery_days'] = (
    orders['order_delivered_customer_date'] -
    orders['order_purchase_timestamp']
).dt.days
print(orders['delivery_days'].describe())
print(f"Average Delivery = {orders['delivery_days'].mean():.1f} days")
print(f"Fastest Delivery = {orders['delivery_days'].min():.0f} days")
print(f"Slowest Delivery = {orders['delivery_days'].max():.0f} days")



#Visualization 1 - Monthly Revenue
plt.figure(figsize=(12,6))
Monthly_Revenue.plot(kind='line',color='blue')
plt.title('Monthly Revenue Trend')
plt.xlabel('Month')
plt.ylabel('Revenue(R$)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


#Visualization 2 - Order Status
plt.figure(figsize=(8,6))
orders['order_status'].value_counts().plot(kind='bar',color='green')
plt.title('Orders by Status')
plt.xlabel('Status')
plt.ylabel('Count')
plt.tight_layout()
plt.show()


#Visualization 3 - Top 10 Cities
top_cities = customers['customer_city'].value_counts().head(10)
plt.figure(figsize=(10,6))
top_cities.plot(kind='bar',color='orange')
plt.title('top 10 cities by customers')
plt.xlabel('City')
plt.ylabel('Number of Customers')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


#Visualization 4 - Payment Types
plt.figure(figsize=(8,6))
payments['payment_type'].value_counts().plot(
    kind='pie',
    autopct='%1.1f%%',
    colors=['blue','green','red','orange']
)
plt.title('Payment Methods Distribution')
plt.ylabel('')
plt.tight_layout()
plt.show()


#Visualization 5 - Revenue by State
plt.figure(figsize=(12,6))
state_revenue.plot(
    kind='bar',
    color='purple'
)
plt.title('Total Revenue by State')
plt.xlabel('State')
plt.ylabel('Revenue (R$)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


#Visualization 6 - Delivery Time
plt.figure(figsize=(10,6))
orders['delivery_days'].dropna().plot(
    kind='hist',
    bins=30,
    color='red',
    edgecolor='black'
)
plt.title('Delivery Time Distribution')
plt.xlabel('Days to Deliver')
plt.ylabel('Number of Orders')
plt.tight_layout()
plt.show()