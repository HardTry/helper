import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
from datetime import datetime
from matplotlib import rcParams

margin = dict(
    {'CF': 0.07, 'FG': 0.06, 'MA': 0.05, 'OI': 0.05, 'RM': 0.05, 'SR': 0.06, 'TA': 0.06, 'ZC': 0.05, 'a': 0.05,
     'ag': 0.07, 'al': 0.05, 'au': 0.07, 'bu': 0.04, 'c': 0.05, 'cu': 0.05, 'i': 0.05, 'j': 0.05, 'jd': 0.05,
     'jm': 0.05, 'l': 0.05, 'm': 0.05, 'ni': 0.05, 'p': 0.05, 'pb': 0.07, 'pp': 0.05, 'rb': 0.07, 'ru': 0.05, 'v': 0.05,
     'y': 0.05, 'zn': 0.05})
unit = dict({'CF': 5, 'FG': 20, 'MA': 10, 'OI': 10, 'RM': 10, 'SR': 10, 'TA': 5, 'ZC': 100, 'a': 10, 'ag': 15, 'al': 5,
             'au': 1000, 'bu': 10, 'c': 10, 'cu': 5, 'i': 100, 'j': 100, 'jd': 10, 'jm': 60, 'l': 10, 'm': 10, 'ni': 1,
             'p': 10, 'pb': 5, 'pp': 5, 'rb': 10, 'ru': 10, 'v': 5, 'y': 10, 'zn': 5})
jump = dict(
    {'CF': 5, 'FG': 1, 'MA': 1, 'OI': 2, 'RM': 1, 'SR': 1, 'TA': 2, 'ZC': 2, 'a': 1, 'ag': 1, 'al': 5, 'au': 5, 'bu': 2,
     'c': 1, 'cu': 10, 'i': 5, 'j': 5, 'jd': 1, 'jm': 5, 'l': 5, 'm': 1, 'ni': 10, 'p': 2, 'pb': 5, 'pp': 1, 'rb': 1,
     'ru': 5, 'v': 5, 'y': 2, 'zn': 5})


def get_instrument_code(inst):
    match = re.match(r"([a-z]+)([0-9]+)", inst, re.I)
    code = ''
    code_continue = ''
    if match:
        items = match.groups()
        code = items[0]
        if len(code) == 1:
            code_continue = code + '9888'
        else:
            code_continue = code + '888'

    return code, code_continue


def set_margin_unit(s):
    inst = s['inst']
    code, cc = get_instrument_code(inst)
    m = margin[code]
    u = unit[code]
    return pd.Series(dict(margin=m, unit=u))


def get_data_source(filepath):
    ds = pd.read_csv(filepath)
    ds['dir'] = ds[['dir', 'action']].apply(lambda x: x['dir'] if x['action'] > 0 else -x['dir'], axis=1)
    ds[['margin', 'unit']] = ds.apply(set_margin_unit, axis=1)
    # set the moneyd
    ds['money'] = ds.price * ds.volume * ds.unit * ds.margin
    ds['mtime'] = ds['time'].apply(lambda x: int(x / 100) * 100)
    # sort
    ds = ds.sort_values(['date', 'time'],
                        ascending=[True, True])
    ds['index1'] = ds.index
    # get all instruments
    instruments = ds['inst'].unique()
    # get all trade days
    days = ds['date'].unique()

    # set index
    # ds.index.names = [None]
    # ds.set_index(['trade_day', 'inst', 'action', 'dir'], inplace=True)

    return ds, instruments, days

def get_xy_data(prices, trade, a, d, i):
    df = trade[(trade.action == a) & (trade.dir == d) & (trade.inst == i)]
    xxx = []
    yyy = []
    for i in np.arange(df.shape[0]):
        t = df.iloc[i]
        rown = prices.index.get_loc((t.date, t.mtime))
        xxx.append(rown)
        yyy.append(t.price)
    return xxx, yyy

if __name__ == '__main__':
    filepath = '/data/sean/analysis/73-97-en.csv'
    ds, instruments, days = get_data_source(filepath)
    dsgb = ds.groupby(['date', 'mtime'])
    # prices = get_price(instruments)
    prices = pd.read_csv('/data/sean/prices-2.csv')
    prices = prices[160:27034]
    prices.set_index(['date', 'time'], inplace=True)


    trade = pd.read_csv('/data/sean/revn-50-60/tt.csv')
    trade['mtime'] = trade['time'].apply(lambda x: int(x / 100) * 100)

    rcParams['figure.figsize'] = 16, 9

    x = np.arange(prices.shape[0])
    for inst in instruments:
        y = np.array(prices['l_' + inst])

        plt.plot(x, y, color='b')
        b_has_fig = 0
        x_ol, y_ol = get_xy_data(prices, trade, 1, 1, inst)
        plt.plot(x_ol, y_ol, 'rx')
        if (len(x_ol) != 0):
            b_has_fig += 1
        x_cl, y_cl = get_xy_data(prices, trade, -1, 1, inst)
        plt.plot(x_cl, y_cl, 'ro')
        if (len(x_cl) != 0):
            b_has_fig += 1
        x_os, y_os = get_xy_data(prices, trade, 1, -1, inst)
        plt.plot(x_os, y_os, 'gx')
        if (len(x_os) != 0):
            b_has_fig += 1
        x_cs, y_cs = get_xy_data(prices, trade, -1, -1, inst)
        plt.plot(x_cs, y_cs, 'go')
        if (len(x_cs) != 0):
            b_has_fig += 1

        plt.suptitle(inst)
        if (b_has_fig == 2 or b_has_fig == 4):
            plt.savefig('/data/sean/revn-50-60/pos/' + inst + '-pos.png')
        plt.close()
