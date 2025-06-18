import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Definir los datos para el gráfico de barras
data = {
    'Stage': ['Main page', 'Product page', 'Added to cart', 'Checkout page', 'Order'],
    'Quantity': [1525, 953, 595, 372, 232]
}

# Crear un DataFrame usando los datos
df = pd.DataFrame(data)

# Hacer que el fondo sea oscuro
plt.style.use("dark_background")

# Crear un gráfico de barras utilizando la librería seaborn
sns.barplot(x='Stage', y='Quantity', data=df)

# Agregar etiquetas y título al gráfico
plt.xlabel('Stage')
plt.ylabel('Quantity')
plt.title('Quantity by Stage')

# Mostrar el gráfico
plt.show()