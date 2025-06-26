# 1.- Importar librerías 
import pandas as pd

# 2.- Cargar información
events = pd.read_csv('/datasets/coffee_home.csv')

#3.- Convertir los campos de fecha a datetime
events['coffee_time'] = pd.to_datetime(events['coffee_time'])
events['first_coffee_datetime'] = pd.to_datetime(events['first_coffee_datetime'])

# 3.- ¿Cuánto tiempo ha pasado desde que pidió su primer café? (Según la fecha del evento)
events['time_to_event'] = events['coffee_time'] - events['first_coffee_datetime']

# 4.- Obtener solo los eventos que han transcurrido antes de 30 días 
filtered_events = events[events['time_to_event'] < '30 days']

# 5.- ¿Cuántos cafés ha pedido cada usuario?
count_events_by_users = filtered_events.groupby('user_id').agg({'coffee_time':'count'}).reset_index()

# 6.- Identificar los usuarios que han pedido más de 4 cafés
count_events_by_users['is_target_behavior'] = count_events_by_users['coffee_time'] > 4

# 7.- Crear una lista independiente que almacene los usuarios que cumplen las condiciones
#user_ids_with_target_behavior = count_events_by_users[count_events_by_users['is_target_behavior']]['user_id']
user_ids_with_target_behavior = count_events_by_users.query('is_target_behavior == True')['user_id'].unique()

# 8.- Crear una lista independiente que almacene los usuarios que NO cumplen las condiciones 
#user_ids_without_target_behavior = count_events_by_users[~count_events_by_users['is_target_behavior']]['user_id']
user_ids_without_target_behavior = count_events_by_users.query('is_target_behavior == False')['user_id'].unique()

# 9.- Marcar en el dataframe los movimientos que son considerables
events.loc[events['user_id'].isin(user_ids_with_target_behavior),'is_in_behavioral_cohort'] = 'yes'


# 10.- Marcar en el dataframe los movimientos que NO son considerables
events.loc[events['user_id'].isin(user_ids_without_target_behavior),'is_in_behavioral_cohort'] = 'no'

# 11.- Crear función para determinar la tasa de retención promedio.
def printRetentionRate(df):
    cohorts = (
        df.groupby(['first_coffee_week', 'cohort_lifetime'], as_index = False)
        .agg({'user_id': 'nunique'})
        .sort_values(['first_coffee_week', 'cohort_lifetime']))

    inital_users_count = cohorts[cohorts['cohort_lifetime'] == 0][['first_coffee_week', 'user_id']]
    inital_users_count = inital_users_count.rename(columns={'user_id': 'cohort_users'})

    cohorts = cohorts.merge(inital_users_count, on='first_coffee_week')

    cohorts['retention'] = cohorts['user_id'] / cohorts['cohort_users']

    print(cohorts.groupby(['cohort_lifetime'])['retention'].mean())
    cohorts.groupby(['cohort_lifetime'])['retention'].mean().plot.bar()


# 12.- Llamar a la función
printRetentionRate(events[events['is_in_behavioral_cohort'] == 'yes'])
#printRetentionRate(events[events['is_in_behavioral_cohort'] == 'no'])