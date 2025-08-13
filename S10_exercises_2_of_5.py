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

print('{0:.3f}'.format(stats.mannwhitneyu(orders[orders['group'] == 'A']['revenue'], orders[orders['group'] == 'B']['revenue'],)[1]))

print('{0:.3f}'.format(orders[orders['group'] == 'B']['revenue'].mean() / orders[orders['group'] == 'A']['revenue'].mean() - 1))
