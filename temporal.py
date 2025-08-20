from scipy import stats as st
import numpy as np
import math as mth

alpha = 0.5

#print (alpha)

successes = np.array([78, 120])
trails = np.array([830, 909])

p1 = successes[0] / trails[0]
p2 = successes[1] / trails[1]

p_combined = (successes[0] + successes[1]) / (trails[0] + trails[1])
difference = p1 - p2 

z_value = difference / mth.sqrt(p_combined * (1 - p_combined) * (1/trails[0] + 1/trails[1]))

distr = st.norm(0,1)

p_value = (1 - distr.cdf(abs(z_value))) * 2

#if p_value < alpha:
#    print('Rechazar la hipótesis nula: hay una diferencia significativa entre las proporciones')
#else:
#    print('No se pudo rechazar la hipótesis nula: no hay razón para pensar que las proporciones son diferentes')

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
import pandas as pd

#df = pd.DataFrame([['a', 5], ['b', 4], ['c', 3], ['d', 2]])
#df.columns = ['letter', 'number']

#df['number'] = df.apply(lambda x: x['number']*3, axis=1)

#print(df)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#df = pd.DataFrame([1,2,3], [4,5,6], [7,8,12], [10,11,12])
#df.columns = ['number1', 'number2', 'number3']
#df.agg({'number1':'max', 'number2':'sum', 'number3':'pd.Series.nunique'})

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#df = pd.DataFrame([2,4,6,8,10,12,14,16,18,20])
#df.columns = ['number']
#print(np.logical_and(df['number']>2, df['number']<10))
#print(df[np.logical_and(df['number']>2, df['number']<10)])


