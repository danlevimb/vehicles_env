from scipy import stats as st
import numpy as np
import math as mth

alpha = .05 # nivel de significación

purchases = np.array([100, 100])
leads = np.array([400, 500])

p1 = purchases[0] / leads[0]
p2 = purchases[1] / leads[1]
p_combined = (purchases[0] + purchases[1]) / (leads[0] + leads[1])

se = mth.sqrt(p_combined * (1 - p_combined) * (1/leads[0] + 1/leads[1]))
z_value = (p1 - p2) / se

p_value = 2 * (1 - st.norm.cdf(abs(z_value)))

print('p-value: ', p_value)

if p_value < alpha:
    print("Rechazar la hipótesis nula: hay una diferencia significativa entre las proporciones")
else:
    print("No se pudo rechazar la hipótesis nula: no hay razón para pensar que las proporciones son diferentes")
    
    
# --------------------------------------------------------------
    