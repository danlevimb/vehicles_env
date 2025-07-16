# Importar librerias
import pandas as pd

# Cargar archivos
sessions_df = pd.read_csv('/datasets/users_sessions_data.csv')

# Convertir las fechas en tipo datetime
sessions_df['session_start_ts'] = pd.to_datetime(sessions_df['session_start_ts'], format='%Y-%m-%d %H:%M')
sessions_df['session_end_ts'] = pd.to_datetime(sessions_df['session_end_ts'], format='%Y-%m-%d %H:%M')

# Encontrar las sesiones por año y mes
sessions_df['session_year'] = sessions_df['session_start_ts'].dt.year
sessions_df['session_month'] = sessions_df['session_start_ts'].dt.month

# Encontrar la cantidad de sesiones y usuarios por mes
sessions_per_user = sessions_df.groupby(['session_year', 'session_month']).agg({'client_id':['count', 'nunique']})
sessions_per_user.columns = ['n_sessions', 'n_users']

# Encontrar la cantidad de sesiones por usuario
sessions_per_user['sess_per_user'] = sessions_per_user['n_sessions'] / sessions_per_user['n_users']

# Encontrar la duración en segundos de las sesiones
sessions_df['session_duration_sec'] = (sessions_df['session_end_ts'] - sessions_df['session_start_ts']).dt.seconds

# Encontrar la moda en la duración de las sesiones
print(sessions_df['session_duration_sec'].mode())

# Graficar la duración de las sesiones
#sessions_df['session_duration_sec'].hist(bins=50)
