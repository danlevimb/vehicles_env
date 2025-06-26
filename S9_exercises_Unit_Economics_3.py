import pandas as pd
import numpy as np

orders = pd.read_csv('/datasets/ltv_orders_2.csv')
costs = pd.read_csv('/datasets/ltv_costs_2.csv')

orders['order_date'] = pd.to_datetime(orders['order_date'])
costs['date'] = pd.to_datetime(costs['date'])

orders['order_month'] = orders['order_date'].astype('datetime64[M]')
costs['month'] = costs['date'].astype('datetime64[M]')

first_orders = orders.groupby('uid').agg({'order_month':'min'}).reset_index()
first_orders.columns = ['uid', 'first_order_month']
cohort_sizes = (first_orders.groupby('first_order_month').agg({'uid':'nunique'}).reset_index())
cohort_sizes.columns = ['first_order_month','n_buyers']
# ---------------------------------------------------------------------------
margin_rate = 0.4 # introduce el margen de la tienda

orders_ = pd.merge(orders, first_orders, on = 'uid')
cohorts = (orders_.groupby(['first_order_month', 'order_month']).agg({'revenue':'sum'}).reset_index())
report = pd.merge(cohort_sizes, cohorts, on ='first_order_month') # fusiona las cohortes y cohort_sizes

report['gp'] =  report['revenue'] * margin_rate
report['age'] = (report['order_month'] - report['first_order_month']) / np.timedelta64(1,'M') # encuentra la edad de cada cohorte en meses, no olvides que el valor debe ser un número entero
report['age'] = report['age'].round().astype('int')
report['ltv'] = report['gp'] / report['n_buyers']# calcula el LTV para las cohortes
result = report.pivot_table(index='first_order_month', columns ='age', values='ltv',aggfunc='mean').round()  # calcula los valores para la tabla dinámica
result = result.fillna('')
# ---------------------------------------------------------------------------
monthly_costs = costs.groupby('month').sum()
report_ = pd.merge(report, monthly_costs, left_on='first_order_month', right_on = 'month') # agrega los costos mensuales al informe de la cohorte
report_['cac'] = report_['costs'] / report_['n_buyers'] # calcula el CAC
report_['romi'] = report_['ltv'] / report_['cac']  #calcula el ROMI

output = report_.pivot_table(index='first_order_month', columns = 'age', values = 'romi', aggfunc='mean')# crea una nueva tabla dinámica

#print(output.cumsum(axis=1).round(2).fillna(''))
# ---------------------------------------------------------------------------
result = report_.pivot_table(index = 'first_order_month', columns = 'age', values ='ltv', aggfunc='mean')

m6_cum_ltv = result.cumsum(axis=1).mean(axis=0)[5] # encuentra el LTV acumulado durante 6 meses desde el momento en que se realizó el primer pedido

print('El LTV promedio durante 6 meses desde el primer pedido:', m6_cum_ltv)