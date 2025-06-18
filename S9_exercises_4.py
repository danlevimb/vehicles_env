import pandas as pd

orders = pd.read_csv('/datasets/orders_data_for_cohort.csv')

first_order_date_by_customers = orders.groupby('customer_id')['order_date'].min()

first_order_date_by_customers.name = 'first_order_date'

orders = orders.join (first_order_date_by_customers, on = 'customer_id')

orders['first_order_month'] = orders['first_order_date'].astype('datetime64[M]')
orders['order_month'] = orders['order_date'].astype('datetime64[M]')

cohort_grouped = orders.groupby('first_order_month').agg({'order_id':'nunique', 'customer_id':'nunique','revenue':'sum'})

print(cohort_grouped)

#print(orders.head())


#print(orders.head())

