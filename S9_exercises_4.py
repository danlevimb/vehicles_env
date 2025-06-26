# 1.- Importar librerias
import pandas as pd

# 2.- Cargar archivo CSV
orders = pd.read_csv('/datasets/orders_data_for_cohort.csv')

# 3.- Convertir los campos de fecha en datetime
orders['order_date'] = pd.to_datetime(orders['order_date'])

# 4.- Obtener la primer fecha del evento
first_order_date_by_customers = orders.groupby('customer_id')['order_date'].min()

# 5.- Renombrar la columna del grupo para poder unirla posteriormente
first_order_date_by_customers.name = 'first_order_date'

# 6.- Integrar la primer fecha del evento en el dataframe original
orders = orders.join (first_order_date_by_customers, on = 'customer_id')

# 7.- Obtener el mes del primer evento
orders['first_order_month'] = orders['first_order_date'].astype('datetime64[M]')

# 8.- Obtener el mes del evento
orders['order_month'] = orders['order_date'].astype('datetime64[M]')

# 9.- Agrupar cohortes
cohort_grouped = orders.groupby('first_order_month').agg({'order_id':'nunique', 'customer_id':'nunique','revenue':'sum'})

print(cohort_grouped)