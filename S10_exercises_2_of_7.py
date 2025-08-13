import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

data = pd.read_csv('/datasets/data_for_tasks_3.csv', sep=',')
data['date'] = data['date'].map(lambda x: dt.datetime.strptime(x, '%d/%m/%Y'))

ordersByUsers = (
    data.drop(['group', 'revenue', 'date'], axis=1)
    .groupby('userId', as_index=False)
    .agg({'orderId': pd.Series.nunique})
)
ordersByUsers.columns = ['userId', 'orders']

plt.hist(ordersByUsers['orders'])
plt.show()

print(ordersByUsers.sort_values(by='orders', ascending=False).head(10))