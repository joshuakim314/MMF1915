#This is the main interface
import numpy as np
import pandas as pd
from pandas.tseries.offsets import *
from datetime import datetime, date
import matplotlib.pyplot as plt
import BenchMarkStrategy as bms
import OLPSResult_monthly as olps
from varname import nameof
import copy
from xone import calendar


#all-in-one function, compare multiple strategies on the same dataset
def compare_strats(strats:list, df:pd.DataFrame, df_name = "", print_option=True, plot_option=True):
    results = []
    for s in strats:
        s_result = s.run(df)
        results.append(copy.copy(s_result))
        if print_option:
            print("{} Strategy on {} dataset{}{}".format(s.name(),df_name, "\n", s_result.__str__()))
    if plot_option:
        labels = [type(s).__name__ for s in strats]
        olps.olps_plot(results, labels=labels, title = df_name)

if __name__ == "__main__":
    # load data
    # df_nyseo = pd.read_excel("Datasets/nyse-o.xlsx", engine='openpyxl')
    # df_nysen = pd.read_excel("Datasets/nyse-n.xlsx", engine='openpyxl')
    # df_tse = pd.read_excel("Datasets/tse.xlsx", engine='openpyxl')
    df_sp500_monthly_clean = pd.read_excel("Datasets/sp500_monthly_clean.xlsx", engine='openpyxl')
    # df_msci = pd.read_excel("Datasets/msci.xlsx", engine='openpyxl')
    # df_djia = pd.read_excel("Datasets/djia.xlsx", engine='openpyxl')

    # #add time column as index
    # add_time(df_nyseo, "1962-07-03", "1984-12-31")
    # add_time(df_nysen, "1985-01-01", "2010-06-30")
    # add_time(df_tse, "1994-01-04", "1998-12-31")
    # add_time(df_sp500_monthly_clean)
    df_sp500_monthly_clean.index = df_sp500_monthly_clean.tick_datetime
    df_sp500_monthly_clean = df_sp500_monthly_clean.drop(columns = ["tick_datetime"])
    # add_time(df_msci, "2006-04-01", "2010-03-31")
    # add_time(df_djia, "2001-01-14", "2003-01-17")


    df_name = "SP500_monthly"
    #uniformly distribute wealth on all stocks
    num_stocks = df_sp500_monthly_clean.shape[1]
    portfolio = [1/num_stocks for i in range(num_stocks)]
    #a list of all strategies to be tested
    #strats = [bms.CRP(portfolio), bms.BS(), bms.BCRP()]
    strats = []
    strats.append(PAMR())
    strats.append(RMR())
    # strats.append(CWMR(type='var'))
    #compare them on S&P500
    compare_strats(strats, df_sp500_monthly_clean, df_name=df_name, print_option=True,plot_option=True )
