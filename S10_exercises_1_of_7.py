import pandas as pd
import scipy.stats as stats
import datetime as dt
import numpy as np

visitors = pd.read_csv('/datasets/data_for_tasks_3_visitors.csv')
visitors['date'] = visitors['date'].map(
    lambda x: dt.datetime.strptime(x, '%d/%m/%Y')
)

orders = pd.read_csv('/datasets/data_for_tasks_3.csv')
orders['date'] = orders['date'].map(
    lambda x: dt.datetime.strptime(x, '%d/%m/%Y')
)

ordersByUsersA = orders[orders['group'] == 'A'].groupby('userId', as_index=False).agg({'orderId': pd.Series.nunique})

ordersByUsersA.columns = ['userId', 'orders']

ordersByUsersB = orders[orders['group'] == 'B'].groupby('userId', as_index = False).agg({'orderId':pd.Series.nunique})

ordersByUsersB.columns = ['userId', 'orders']

sampleA = pd.concat([ordersByUsersA['orders'], pd.Series(0, index=np.arange(visitors[visitors['group'] == 'A']['visitors'].sum() - len(ordersByUsersA['orders'])), name='orders')], axis=0)

sampleB = pd.concat([ordersByUsersB['orders'], pd.Series(0, index = np.arange(visitors[visitors['group'] == 'B']['visitors'].sum() - len(ordersByUsersB['orders'])), name = 'orders')], axis = 0)

print('{0:.5f}'.format(stats.mannwhitneyu(sampleA, sampleB)[1]))
print('{0:.3f}'.format(sampleB.mean() / sampleA.mean() - 1))




