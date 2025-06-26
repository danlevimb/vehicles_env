import pandas as pd
example_date = pd.to_datetime('2010-10-25')

#print(example_date + pd.Timedelta(days=10))
#print(example_date - pd.Timedelta(days=5))

# -----------------------------------------------

dates_series = pd.Series(pd.date_range('2010-01-01', periods=10, freq='D'))
#print(dates_series)

offset_dates_series = dates_series - pd.Timedelta(days=3)
print(dates_series, offset_dates_series)
