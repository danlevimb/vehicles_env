import numpy as np

# Crea los vectores x e y
x = [12, 9, 4, 5, 5, 7, 7, 6, 7, 11, 9, 8, 10, 4, 11] # escribe tu código aquí
y = [28.1, 18.7, 1.0, 10.2, 11.6, 19.9, 24.4, 18.1, 18.5, 25.0, 21.8, 13.4, 18.0, 11.1, 21.1]# escribe tu código aquí

# Obtiene las predicciones (Una para cada modelo)
y_1 = [(2 + 2*i) for i in x]
y_2 = [(3 + 1*i) for i in x]

# Crear funcion para determinar el error cuadrático
def error_function(y_real, y_pred):
    return sum((np.array(y_real) - np.array(y_pred))**2) / len(y_real)

# Llamar la función para determinar el error cuadrático
q_1 = error_function(y, y_1)
q_2 = error_function(y, y_2)

# Mostrar los valores de error resultante para cada modelo / función.
print('El error del primer modelo:', q_1)
print('El error del segundo modelo:', q_2)

print("¡Es correcto! Los errores son más graves con el segundo modelo, por lo que es mejor pronosticar usando el primero.")

