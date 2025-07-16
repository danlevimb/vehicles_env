import pandas as pd

users_data = pd.read_csv('/datasets/users_data.csv')
users_data['session_start_ts'] = pd.to_datetime(users_data['session_start_ts'])
users_data['session_end_ts'] = pd.to_datetime(users_data['session_end_ts'])
users_data['session_year'] = users_data['session_start_ts'].dt.isocalendar().year
users_data['session_month'] = users_data['session_start_ts'].dt.month
users_data['session_week'] = users_data['session_start_ts'].dt.isocalendar().week
users_data['session_date'] = users_data['session_start_ts'].dt.date

mau_total = users_data.groupby(['session_year', 'session_month']).agg({'id':'nunique'}).mean()
dau_total = users_data.groupby('session_date').agg({'id':'nunique'}).mean()
wau_total = users_data.groupby(['session_year', 'session_week']).agg({'id':'nunique'}).mean()

sticky_mau = dau_total / mau_total * 100
sticky_wau = dau_total / wau_total * 100

print(sticky_wau)
print(sticky_mau)