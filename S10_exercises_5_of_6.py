import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

orders = pd.read_csv('/datasets/data_for_tasks_3.csv', sep=',')
orders['date'] = orders['date'].map(
    lambda x: dt.datetime.strptime(x, '%d/%m/%Y'))

visitors = pd.read_csv('/datasets/data_for_tasks_3_visitors.csv', sep=',')
visitors['date'] = visitors['date'].map(
    lambda x: dt.datetime.strptime(x, '%d/%m/%Y'))

datesGroups = orders[['date', 'group']].drop_duplicates()

ordersAggregated = datesGroups.apply(
    lambda x: orders[
        np.logical_and(
            orders['date'] <= x['date'], orders['group'] == x['group'])].agg({'date': 'max',
            'group': 'max',
            'orderId': pd.Series.nunique,
            'userId': pd.Series.nunique,
            'revenue': 'sum',}),axis=1,).sort_values(by=['date', 'group'])

visitorsAggregated = datesGroups.apply(
    lambda x: visitors[
        np.logical_and(
            visitors['date'] <= x['date'], visitors['group'] == x['group']
        )
    ].agg({'date': 'max', 'group': 'max', 'visitors': 'sum'}), axis=1,).sort_values(by=['date', 'group'])

cumulativeData = ordersAggregated.merge(
    visitorsAggregated, left_on=['date', 'group'], right_on=['date', 'group']
)
cumulativeData.columns = ['date', 'group', 'orders', 'buyers', 'revenue', 'visitors']

cumulativeData['conversion'] = cumulativeData['orders'] / cumulativeData['visitors']

cumulativeDataA = cumulativeData[cumulativeData['group'] == 'A']

cumulativeDataB = cumulativeData[cumulativeData['group'] == 'B']

plt.plot(cumulativeDataA['date'], cumulativeDataA['conversion'], label = 'A')

plt.plot(cumulativeDataB['date'], cumulativeDataB['conversion'], label = 'B')

plt.legend()
plt.axis([pd.to_datetime('2019-03-10'), pd.to_datetime('2019-04-23'), 0, 0.05])