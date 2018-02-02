import matplotlib.pyplot as plt
import pandas as pd
from mongoengine import *
import sys, time, os
from datetime import date, datetime, time, tzinfo, timedelta
import numpy as np
import re
import math

class CandleData(Document):
    High = FloatField()
    period = StringField()
    strDate = StringField()
    Volume = FloatField()
    instrument = StringField()
    Low = FloatField()
    Close = FloatField()
    openInterest = FloatField()
    Open = FloatField()
    strTime = StringField()
    fltTime = FloatField()

    meta = {
        'collection': 'candledata'
    }


def get_instruments_days(filepath):
    ds = pd.read_csv(filepath)

    instruments = ds['inst'].unique()
    days = ds['date'].unique()

    # set index
    # ds.index.names = [None]
    # ds.set_index(['trade_day', 'inst', 'action', 'dir'], inplace=True)

    return instruments, days

def get_every_tick_taik(day):
    # 21:00 - 23:00, 23:00 - 23:30, 23:30 - 02:30, 9:00 - 10:15, 10:15 - 11:30, 13:30 - 15:00
    # 0:00 - 02:30, 9:00 - 10:15, 10:30 - 11:30, 13:30 - 15:00, 21:00 - 23:00, 23:00 - 23:30, 23:30 - 23:59
    # 2 * 24 + 30, 10*24+15 - 9*24, ....

    r = []
    r.append(list(range(0, 2 * 60 + 30)))
    r.append(list(range(9 * 60, 10 * 60 + 15)      ))
    r.append(list(range(10 * 60 + 30, 11 * 60 + 30)))
    r.append(list(range(13 * 60 + 30, 15 * 60)     ))
    r.append(list(range(21 * 30, 23 * 60)          ))
    r.append(list(range(23 * 60, 23 * 60 + 30)     ))
    r.append(list(range(23 * 60 + 30, 23 * 60 + 59)))

    y = day / 10000
    m = (day - y * 10000) / 100
    d = day - y * 10000 - m * 100
    stime = datetime(y, m, d, 0, 0, 0)
    delta = timedelta(minutes=1)
    M = []
    allm = []
    for i in range(0, 7):
        M = [tuple((stime + timedelta(minutes=x)).strftime('%Y%M%d %H%M%S').split()) for x in r[i]]
        allm.append(M)
    return allm


def check_candle(inst, day):
    allm = get_every_tick_taik(day)

    for i in range(0, 7):
        dt = allm[i][0]
        c = CandleData.objects(instrument=inst, period='1m', strDate=dt[0], strTime=dt[1])
        if len(c) == 1:
            for dt in allm[i]:
                c = CandleData.objects(instrument=inst, period='1m', strDate=dt[0], strTime=dt[1])
                if (len(c) != 1):
                    print 'Error ', inst, dt


# allm = get_every_tick_taik(20170707)
filepath = '/home/sean/Downloads/73-97-en.csv'
instruments, days = get_instruments_days(filepath)

register_connection("ctpdata", host='10.10.10.13', port=29875)
conn = connect(db="ctpdata", host='10.10.10.13', port=29875)

for inst in instruments:
    for day in days:
        check_candle(inst, day)