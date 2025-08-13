import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

data = pd.read_csv('/datasets/data_for_tasks_3.csv', sep=',')
data['date'] = data['date'].map(lambda x: dt.datetime.strptime(x, '%d/%m/%Y'))

ordersByUsers = (
    data.drop(['group', 'revenue', 'date'], axis=1)
    .groupby('userId', as_index=False)
    .agg({'orderId': pd.Series.nunique}))

ordersByUsers.columns = ['userId', 'orders']

print(ordersByUsers.sort_values(by='orders', ascending=False).head(10))

# el rango de números desde 0 hasta el número de observaciones en ordersByUsers
x_values = pd.Series(range(0,len(ordersByUsers)))

plt.figure(figsize=(10,6))
plt.scatter(x_values, ordersByUsers['orders'])
plt.title('Diagrama de dispersión - Número de pedidos por usuario')
plt.xlabel('Observaciones')
plt.ylabel('Pedidos ("orders")')
plt.grid(True)
plt.show()
