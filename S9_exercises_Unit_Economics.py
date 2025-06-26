import pandas as pd

n_users = 50000
revenue_per_user = 10

var_costs = pd.Series({'marketing': 200000, 'servers': 200000})
fixed_costs = pd.Series({'salaries': 300000, 'rent': 150000})

revenue = n_users * revenue_per_user
total_costs = var_costs.sum() + fixed_costs.sum()

one_unit_var_costs = var_costs / n_users

def unit_economics(marketing):  
    n_users = marketing / one_unit_var_costs['marketing']
    revenue = n_users * revenue_per_user
    var_costs = one_unit_var_costs * n_users
    return revenue - sum(var_costs) - sum(fixed_costs)

for m in range(300000, 1500000, 100000):
    print('Profit/loss: {} with a budget of {}'.format(unit_economics(m), m))