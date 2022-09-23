import pandas as pd
import pickle
import datetime
from dateutil.relativedelta import relativedelta

from pypfopt import HRPOpt
from pypfopt import expected_returns


with open('data/dow_jones_30.pickle', 'rb') as f:
    data = pickle.load(f)

rets = expected_returns.returns_from_prices(data)

start_date = datetime.datetime(2020, 8, 1, 0, 0)
end_date = datetime.datetime(2021, 8, 1, 0, 0)

while end_date < datetime.datetime(2022, 10, 1, 0, 0):
    print(start_date, end_date)
    hrp = HRPOpt(rets[start_date:end_date])
    hrp.optimize()
    weights = hrp.clean_weights()
    print(weights)
    with open(f'data/hrp_weights_{end_date.strftime("%Y%m%d")}.pickle', 'wb') as outp:
        pickle.dump(weights, outp, pickle.HIGHEST_PROTOCOL)
    start_date += relativedelta(months=+1)
    end_date += relativedelta(months=+1)