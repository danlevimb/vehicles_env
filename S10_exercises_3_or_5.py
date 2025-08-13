import pandas as pd
import scipy.stats as stats
import datetime as dt
import numpy as np

visitors = pd.read_csv('/datasets/data_for_tasks_3_visitors.csv')
visitors['date'] = visitors['date'].map(
    lambda x: dt.datetime.strptime(x, '%d/%m/%Y'))

orders = pd.read_csv('/datasets/data_for_tasks_3.csv')
orders['date'] = orders['date'].map(
    lambda x: dt.datetime.strptime(x, '%d/%m/%Y'))

ordersByUsersA = (
    orders[orders['group'] == 'A']
    .groupby('userId', as_index=False)
    .agg({'orderId': pd.Series.nunique}))

ordersByUsersA.columns = ['userId', 'orders']

ordersByUsersA[ordersByUsersA['orders'] > 2]['userId']

ordersByUsersB = (
    orders[orders['group'] == 'B']
    .groupby('userId', as_index=False)
    .agg({'orderId': pd.Series.nunique}))

ordersByUsersB.columns = ['userId', 'orders']

usersWithManyOrders = pd.concat([ordersByUsersA[ordersByUsersA['orders'] > 2]['userId'], ordersByUsersB[ordersByUsersB['orders'] > 2]['userId']], axis = 0)

usersWithExpensiveOrders = orders[orders['revenue'] > 10000]['userId']

abnormalUsers = pd.concat([usersWithManyOrders, usersWithExpensiveOrders], axis = 0).drop_duplicates().sort_values()

print(abnormalUsers.head(5))