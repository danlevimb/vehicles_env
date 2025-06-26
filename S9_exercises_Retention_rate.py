import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

# 1.- Cargar el archivo CSV
user_activity = pd.read_csv('/datasets/user_activity.csv')

# 2.- Cambiar el tipo de dato de la fecha
user_activity['activity_date'] = pd.to_datetime(user_activity['activity_date'])

# 3.- Obtener la fecha de la primer actividad
first_activity_date = user_activity.groupby('user_id')['activity_date'].min()

# 4.- Renombrar el objeto series para poder unirlo
first_activity_date.name = 'first_activity_date'

# 5.- Unir los dataframes "user_activity" con "first_activity_date"
user_activity = user_activity.join(first_activity_date, on = 'user_id')

# 6.- Obtener la fecha (primer día de la semana) de la semana en que cae la fecha de la actividad
user_activity['activity_week'] = pd.to_datetime(user_activity['activity_date'], unit='d') - pd.to_timedelta(user_activity['activity_date'].dt.dayofweek,unit='d')

# 6.- Obtener la fecha (primer día de la semana) de la semana en que cae la fecha de la primer actividad
user_activity['first_activity_week'] = pd.to_datetime(user_activity['first_activity_date'],unit='d') - pd.to_timedelta(user_activity['first_activity_date'].dt.dayofweek, unit='d')

# 7.- Obtener el ciclo de vida de la cohorte (en días)
user_activity['cohort_lifetime'] = user_activity['activity_week'] - user_activity['first_activity_week']

# 8.- Transformar el ciclo de vida de la cohorte a semanas
user_activity['cohort_lifetime'] = user_activity['cohort_lifetime'] / np.timedelta64(1,'W')
#print(np.timedelta64(1,'W'))

# 9.- Transformar el ciclo de vida de la cohorte a entero
user_activity['cohort_lifetime'] = user_activity['cohort_lifetime'].astype(int)

# 10.- Agrupar los datos por cohorte y ciclo de vida
cohort = user_activity.groupby(['first_activity_week', 'cohort_lifetime']).agg({'user_id':'nunique'}).reset_index()

# 11.- Obtener la cantidad inicial de usuarios de cada cohorte
initial_users_count = cohort[cohort['cohort_lifetime'] == 0][['first_activity_week','user_id']]

# 12.- Renombrar la columna del contador a "cohort_users"
initial_users_count = initial_users_count.rename(columns = {'user_id':'cohort_users'})

# 13.- Unir los datasets cohort e initial_users_count
cohort = pd.merge(cohort, initial_users_count, on = 'first_activity_week')

# 14.- Calcular la tasa de retención
cohort['retention'] = cohort['user_id'] / cohort['cohort_users']

# 15.- Crear la tabla pivote 
retention_pivot = cohort.pivot_table(index='first_activity_week', columns = 'cohort_lifetime', values = 'retention', aggfunc='sum')

# 16.- Crear mapa de calor
sns.set(style='white')
plt.figure(figsize=(13,9))
plt.title('Cohortes: Retención de usuarios/as')
sns.heatmap(retention_pivot, annot=True, fmt='.1%', linewidths=1, linecolor='gray')

#print(retention_pivot)

