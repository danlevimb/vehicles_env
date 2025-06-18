import seaborn as sns
import matplotlib.pyplot as plt

# Definir los datos
days = [1,2,3,4,5,6,7,8,9,10]
store_sun = [40,45,17,36,14,30,33,19,48,25]
store_moon = [19,14,37,31,26,11,43,45,50,48]

# Crear el gráfico de líneas
ax = sns.lineplot(x=days, y=store_sun, label='Store Sun')
sns.lineplot(x=days, y=store_moon, label='Store Moon')

# Establecer las etiquetas y el título del gráfico
plt.xlabel('Días')
plt.ylabel('Conversión (%)')
plt.title('Conversión en el tiempo')

ax.set_xlim(0,10)
ax.set_ylim(0,50)

# Mostrar el gráfico
plt.legend()
plt.show()