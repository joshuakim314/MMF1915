import pandas as pd
import pickle
import datetime
from dateutil.relativedelta import relativedelta

from pypfopt import HRPOpt
from pypfopt import expected_returns


def solve_quadratic_polynomial(a, b, c):
    return (-b + (b**2 - 4*a*c)**0.5) / (2*a)


def two_asset_rp(q1, q2):
    a = q1 - q2
    b = 2*q2
    c = -q2
    x1 = solve_quadratic_polynomial(a, b, c)
    x2 = 1 - x1
    return x1, x2


"""retrieve equity daily data"""
with open('data/dow_jones_30.pickle', 'rb') as f:
    equity_data = pickle.load(f)
equity_rets = expected_returns.returns_from_prices(equity_data)

"""retrieve gold daily data"""
with open('data/gold.pickle', 'rb') as f:
    # note: remove 2021-11-25 row if needed
    gold_data = pickle.load(f)
gold_rets = expected_returns.returns_from_prices(gold_data)

"""specify time period"""
start_date = datetime.datetime(2020, 8, 1, 0, 0)
end_date = datetime.datetime(2021, 8, 1, 0, 0)

"""construct portfolio"""
rp_weights = []
while end_date < datetime.datetime(2022, 10, 1, 0, 0):
    print(start_date, end_date)
    equity_rets_train = equity_rets.loc[start_date:end_date]
    gold_rets_train = gold_rets.loc[start_date:end_date]
    
    """equity HRP portfolio"""
    hrp = HRPOpt(equity_rets_train)
    hrp.optimize()
    weights = hrp.clean_weights()
    with open(f'data/hrp_weights_{end_date.strftime("%Y%m%d")}.pickle', 'wb') as outp:
        pickle.dump(weights, outp, pickle.HIGHEST_PROTOCOL)
        
    """portfolio return data"""
    equity_rets_train["portf"] = equity_rets_train.apply(lambda row: sum([row.loc[tick]*weights[tick] for tick in weights]), axis=1)
    
    """RP of equity portfolio and gold"""
    # cov = equity_rets_train["portf"].cov(gold_rets_train)
    # assert equity_weight * (equity_weight*equity_var + gold_weight*cov) - gold_weight * (equity_weight*cov + gold_weight*gold_var) < 1e-12
    equity_var = equity_rets_train["portf"].var()
    gold_var = gold_rets_train.var()
    equity_weight, gold_weight = two_asset_rp(equity_var, gold_var)
    rp_weights.append([end_date, equity_weight, gold_weight])

    start_date += relativedelta(months=+1)
    end_date += relativedelta(months=+1)

df_rp_weights = pd.DataFrame(rp_weights, columns=["Date", "equity_portf", "gold"])
df_rp_weights.to_csv("data/rp_weights.csv", encoding='utf-8', index=False)
with open(f'data/rp_weights.pickle', 'wb') as outp:
    pickle.dump(df_rp_weights, outp, pickle.HIGHEST_PROTOCOL)
