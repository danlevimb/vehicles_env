import pandas as pd
#import seaborn as sns
#import matplotlib.pyplot as plt
import numpy as np

# 2.- Cargar CSV's
orders = pd.read_csv('/datasets/ltv_orders_1.csv')
costs = pd.read_csv('/datasets/ltv_costs_1.csv')

# 3.- Convertir los campos de fecha en datetime
orders['order_date'] = pd.to_datetime(orders['order_date']).astype('datetime64')
costs['date'] = pd.to_datetime(costs['date']).astype('datetime64')

# 4.- Obtener el mes de las ordenes y las compras
orders['order_month'] = orders['order_date'].astype('datetime64[M]')
costs['month'] = costs['date'].astype('datetime64[M]')

# Encontrar la fecha de primera compra de cada cliente
first_orders = orders.groupby('uid').agg({'order_month':'min'}).reset_index()

# Renombrar las columnas del dataframe
first_orders.columns = ['uid', 'first_order_month']

# Calcular el numero de clientes por mes
cohort_sizes = first_orders.groupby('first_order_month').agg({'uid':'nunique'}).reset_index()
cohort_sizes.columns = ['first_order_month', 'n_buyers']
orders_ = pd.merge(orders, first_orders, on = 'uid')

cohorts = orders_.groupby(['first_order_month', 'order_month']).agg({'revenue':'sum'}).reset_index()

report = pd.merge(cohort_sizes, cohorts, on = 'first_order_month')

margin_rate = 0.5

report['gp'] = report['revenue'] * margin_rate
report['age'] = (report['order_month'] - report['first_order_month']) / np.timedelta64(1,'M')
report['age'] = report['age'].round().astype('int')

report['ltv'] = report['gp'] / report['n_buyers']

output = report.pivot_table(index='first_order_month', columns='age', values ='ltv', aggfunc = 'mean').round()

ltv_201803 = output.loc['2018-03-01'].sum()

#Obtener la cohorte necesaria
cohort_201803 = report[report['first_order_month'] == '2018-03-01']

# calcular los costos para el mes de la cohorte
costs_201803 = costs[costs['month'] == '2018-03-01']['costs'].sum()

n_buyers_201803 = cohort_201803['n_buyers'][0]
cac_201803 = costs_201803 / n_buyers_201803
ltv_201803 = output.loc['2018-03-01'].sum()

#print('CAC = ', cac_201803)
#print('LTV = ', ltv_201803)

# ----------------

# Calcular los costos por mes
monthly_costs = costs.groupby('month').sum()

report_ = pd.merge(report, monthly_costs, left_on = 'first_order_month', right_on ='month')
report_['cac'] = report_['costs'] / report_['n_buyers']
#print(report_.head())

report_['romi'] = report_['ltv'] / report_['cac']
output = report_.pivot_table(index='first_order_month', columns = 'age', values = 'romi',aggfunc='mean')
print(output.cumsum(axis=1).mean(axis=0))







