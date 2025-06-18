import pandas as pd

funnel_daily = pd.read_csv('/datasets/funnel_daily.csv')
funnel_daily['date'] = pd.to_datetime(funnel_daily['date'])
funnel_daily['week'] = funnel_daily['date'].dt.week

grp = funnel_daily.groupby('week')
agg_dict = {'impressions':'sum', 'clicks':'sum', 'registrations':'sum'}

funnel_weekly = grp.agg(agg_dict)
funnel_weekly['ctr, %'] = funnel_weekly['clicks'] / funnel_weekly['impressions'] * 100
funnel_weekly['cr, %'] = funnel_weekly['registrations'] / funnel_weekly['clicks'] * 100

#print(funnel_daily)
print(funnel_weekly)