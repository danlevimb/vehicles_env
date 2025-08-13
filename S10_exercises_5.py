from scipy import stats as st
import numpy as np

sample_A = [3071, 3636, 3454, 3151, 2185, 3259, 1727, 2263, 2015, 
            2582, 4815, 633, 3186, 887, 2028, 3589, 2564, 1422, 1785, 
            3180, 1770, 2716, 2546, 1848, 4644, 3134, 475, 2686, 
            1838, 3352]
sample_B = [1211, 1228, 2157, 3699, 600, 1898, 1688, 1420, 5048, 3007, 
            509, 3777, 5583, 3949, 121, 1674, 4300, 1338, 3066, 
            3562, 1010, 2311, 462, 863, 2021, 528, 1849, 255, 
            1740, 2596]
sample_C = [1211, 1228, 2157, 3699, 600, 1898, 1688, 1420, 5048, 3007, 
            509, 3777, 5583, 3949, 121, 1674, 4300, 1338, 3066, 
            3562, 1010, 2311, 462, 863, 2021, 528, 1849, 255, 
            1740, 2596]

alpha = .05 # nivel de significación

results_AB = st.ttest_ind(
    sample_A, 
    sample_B)

results_BC = st.ttest_ind(
    sample_B, 
    sample_C)

results_AC = st.ttest_ind(
    sample_A, 
    sample_C)

bonferroni_alpha = alpha / 3  # tres comparaciones realizadas

print('valor p para comparar los grupos A y B: ', results_AB.pvalue)
print('valor p para comparar los grupos B y C: ', results_BC.pvalue)
print('valor p para comparar los grupos A y C: ', results_AC.pvalue)

if (results_AB.pvalue < bonferroni_alpha):
    print("Hipótesis nula rechazada para los grupos А y B")
else:
    print("Hipótesis nula no rechazada para los grupos А y B")

if (results_BC.pvalue < bonferroni_alpha):
    print("Hipótesis nula rechazada para los grupos B y C")
else:
    print("Hipótesis nula no rechazada para los grupos B y C")

if (results_AC.pvalue < bonferroni_alpha):
    print("Hipótesis nula rechazada para los grupos A y C")
else:
    print("Hipótesis nula no rechazada para los grupos А y C")