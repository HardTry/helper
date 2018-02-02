import matplotlib.pyplot as plt
import pandas as pd
from mongoengine import *
import sys, time, datetime
import numpy as np
import re
import math

margin = dict({'CF': 0.07, 'FG': 0.06, 'MA': 0.05, 'OI': 0.05, 'RM': 0.05, 'SR': 0.06, 'TA': 0.06, 'ZC': 0.05, 'a': 0.05, 'ag': 0.07, 'al': 0.05, 'au': 0.07, 'bu': 0.04, 'c': 0.05, 'cu': 0.05, 'i': 0.05, 'j': 0.05, 'jd': 0.05, 'jm': 0.05, 'l': 0.05, 'm': 0.05, 'ni': 0.05, 'p': 0.05, 'pb': 0.07, 'pp': 0.05, 'rb': 0.07, 'ru': 0.05, 'v': 0.05, 'y': 0.05, 'zn': 0.05})
unit = dict({'CF': 5, 'FG': 20, 'MA': 10, 'OI': 10, 'RM': 10, 'SR': 10, 'TA': 5, 'ZC': 100, 'a': 10, 'ag': 15, 'al': 5, 'au': 1000, 'bu': 10, 'c': 10, 'cu': 5, 'i': 100, 'j': 100, 'jd': 10, 'jm': 60, 'l': 10, 'm': 10, 'ni': 1, 'p': 10, 'pb': 5, 'pp': 5, 'rb': 10, 'ru': 10, 'v': 5, 'y': 10, 'zn': 5})
jump = dict({'CF': 5, 'FG': 1, 'MA': 1, 'OI': 2, 'RM': 1, 'SR': 1, 'TA': 2, 'ZC': 2, 'a': 1, 'ag': 1, 'al': 5, 'au': 5, 'bu': 2, 'c': 1, 'cu': 10, 'i': 5, 'j': 5, 'jd': 1, 'jm': 5, 'l': 5, 'm': 1, 'ni': 10, 'p': 2, 'pb': 5, 'pp': 1, 'rb': 1, 'ru': 5, 'v': 5, 'y': 2, 'zn': 5})

class MoneyManager:
    def __init__(self, all, my, dpst_pcnt, commision):
        self.reset(all, my, dpst_pcnt, commision)


    def reset(self, all, my, dpst_pcnt, commision):
        self.all_money = all
        self.all_deposit = 0.0
        self.my_money = my
        self.my_ratio = self.my_money / self.all_money
        self.my_deposit = 0.0
        self.dpst_pcnt = dpst_pcnt
        self.max_dpst = self.my_money * self.dpst_pcnt
        self.commision = commision
        self.mark_rev = 0.0
        self.my_rev = 0.0


    def get_left_money(self):
        return self.max_dpst - self.my_deposit

    def to_json(self):
        return ' { \'all_money\': ' + str(self.all_money  ) +\
                ', \'all_deposit\': ' + str(self.all_deposit) +\
                ', \'my_ratio\': ' + str(self.my_ratio   ) +\
                ', \'my_money\': ' + str(self.my_money   ) +\
                ', \'my_deposit\': ' + str(self.my_deposit ) + \
                ', \'dpst_pcnt\': ' + str(self.dpst_pcnt) + \
                ', \'max_dpst\': ' + str(self.max_dpst) + \
                ', \'commision\': ' + str(self.commision ) +\
                ', \'mark_rev\': ' + str(self.mark_rev) +\
                ', \'my_rev\': ' + str(self.my_rev) + '}'


mm = MoneyManager(200000000, 2000000, 0.8, 0.0005)

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

class Position:
    def __init__(self, inst, prefix, is_long):
        self.inst = inst
        self.prefix = prefix
        self.vol = int(0)           # volume
        self.price = 0              # price
        self.deposit = 0.0          # deposit
        self.crev = 0.0             # revenue when closed
        self.pct_dpt = 0.0          # percent of all deposit
        self.pct_all = 0.0          # percent of all
        self.is_long = is_long      # long or short

    def open(self, i, trade):
        self.vol += trade.volume
        self.deposit += trade.money
        self.price = self.deposit / (self.vol * trade.margin * trade.unit)
        mm.all_deposit += trade.money
        self.pct_dpt = self.deposit / mm.all_deposit
        self.pct_all = self.deposit / mm.all_money


    def close(self, i, trade):
        closed = 0
        if self.vol < trade.volume:
            vdelta = self.vol
            print "close error: ", i, trade.inst, trade.trade_day, self.vol - trade.volume
        else:
            vdelta = trade.volume
        self.vol -= vdelta
        if self == 0:
            closed = 5

        delta = self.price * vdelta * trade.unit * trade.margin
        if self.vol == 0:
            delta = self.deposit
            self.deposit = 0
        else:
            self.deposit -= delta
        mm.all_deposit -= delta
        self.pct_all = self.deposit / mm.all_money
        self.pct_dpt = self.deposit / mm.all_deposit

        # keep ps.price
        if vdelta > 0:
            revenue = (trade.price - self.price) * vdelta * trade.unit
            if not self.is_long:
                revenue = -revenue
            revenue -= (trade.price + self.price) * vdelta * trade.unit * mm.commision
            self.crev += revenue
            mm.mark_rev += revenue
        return closed

    # mp is benchmark's position
    def my_open(self, i, trade, mp):
        # this instrument-deposit would take how many my money
        this_deposit = mp.pct_all * mm.max_dpst
        # new add deposit
        new_delta = this_deposit - self.deposit
        if new_delta <= 0:
            # cant understand if it's negative
            new_delta = 0
        else:
            if new_delta + mm.my_deposit > mm.max_dpst:
                # print "can not open new position", i, trade.inst, trade.trade_day
                # can i make a part of new position?
                new_delta = mm.max_dpst - mm.my_deposit
                if new_delta <= 0:
                    # can not understatnd
                    new_delta = 0
        # cal how many volume i can open
        if new_delta > 0:
            vol = int(new_delta / (trade.price * trade.unit * trade.margin))
            if vol > 0:
                new_delta = trade.price * vol * trade.unit * trade.margin
                self.vol += vol
                self.deposit += new_delta
                self.price = self.deposit / (self.vol * trade.unit * trade.margin)
                mm.my_deposit += new_delta
                self.pct_dpt = self.deposit / mm.my_deposit  # my percent in all my deposit
                self.pct_all = self.deposit / mm.max_dpst  # my percent in all my money
                if 'my' in self.prefix:
                    print 'Open ', i, trade.inst, vol, self.vol, trade.dir, trade.price, self.deposit, mm.my_deposit, self.pct_all
                # keep ps.revenue, calculate when close?

    # mp is benchmark's position
    def my_close(self, i, trade, mp):
        if self.vol > 0:
            #how many deposit of this instrument i should take?
            delta = self.deposit - mp.pct_all * mm.max_dpst
            if delta > 0:
                vol = int(delta / (self.price * trade.unit * trade.margin))
                if (vol > 0):
                    if vol > self.vol:
                        vol = self.vol
                        delta = self.deposit
                    else:
                        delta = self.price * trade.unit * trade.margin * vol
                    self.vol -= vol
                    self.deposit -= delta
                    mm.my_deposit -= delta
                    myrev = (trade.price - self.price) * vol * trade.unit
                    if not self.is_long:
                        myrev = -myrev
                    myrev -= (trade.price + self.price) * vol * trade.unit * mm.commision
                    self.crev += myrev
                    mm.my_rev += myrev
                    self.pct_dpt = self.deposit / mm.my_deposit  # my percent in all my deposit
                    self.pct_all = self.deposit / mm.max_dpst  # my percent in all my money
                    if 'my' in self.prefix:
                        # print 'Close ', i, self.crev, mp.crev, mm.my_rev, mm.mark_rev, trade.inst, trade.dir, mm.my_deposit, self.pct_all
                        print 'Close ', self.crev, mp.crev, mm.my_rev, mm.mark_rev, trade.inst, trade.dir, mm.my_deposit, self.pct_all

    def my_clear(self, i, trade, mp):
        if self.vol > 0:
            #how many deposit of this instrument i should take?
            vol = self.vol
            delta = self.price * trade.unit * trade.margin * vol
            self.vol -= vol
            self.deposit -= delta
            mm.my_deposit -= delta
            myrev = (trade.price - self.price) * vol * trade.unit
            if not self.is_long:
                myrev = -myrev
            myrev -= (trade.price + self.price) * vol * trade.unit * mm.commision
            self.crev += myrev
            mm.my_rev += myrev
            self.pct_dpt = self.deposit / mm.my_deposit  # my percent in all my deposit
            self.pct_all = self.deposit / mm.max_dpst  # my percent in all my money
            if 'my' in self.prefix:
                print 'Clear ', i, self.crev, mp.crev, mm.my_rev, mm.mark_rev, trade.inst, trade.dir, mm.my_deposit, self.pct_all


    def to_dataframe(self):
        pass


class PositionStatus:
    def __init__(self, inst, prefix):
        self.prefix = prefix
        self.lp = Position(inst, 'L_' + prefix, True)            # long position
        self.sp = Position(inst, 'S_' + prefix, False)            # short position
        # self.tp = Position(inst, 'T_' + prefix)            # all position ???

    def do_trade(self, i, trade):
        if trade.dir > 0:
            p = self.lp
        else:
            p = self.sp

        if trade.action > 0:
            p.open(i, trade)
            return 0
        else:
            return p.close(i, trade)

    # mps is benchmark's position-status
    def do_my_trade(self, i, trade, mp):
        if trade.dir > 0:
            p = self.lp
        else:
            p = self.sp

        if trade.action > 0:
            p.my_open(i, trade, mp)
        else:
            p.my_close(i, trade, mp)



    def do_my_clear(self, i, trade, mp):
        if trade.dir > 0:
            p = self.lp
        else:
            p = self.sp

        p.my_clear(i, trade, mp)



    def to_dataframe(self):
        pass


class TradePosition:
    def __init__(self, inst):
        self.inst = inst
        self.mark = PositionStatus(inst, 'mark')
        self.my = PositionStatus(inst, 'my')
        self.up_day = 0                 # update trade day
        self.up_date = 0                # update date
        self.up_tiem = 0                # update time

    def do_trade(self, i, trade):
        self.inst = trade.inst
        self.up_day = trade.trade_day
        self.up_date = trade.date
        self.uptime = trade.time

        if self.mark.do_trade(i, trade) == 5:
            if trade.dir > 0:
                self.my.do_my_clear(i, trade, self.mark.lp)
            else:
                self.my.do_my_clear(i, trade, self.mark.sp)
        else:
            if trade.dir > 0:
                self.my.do_my_trade(i, trade, self.mark.lp)
            else:
                self.my.do_my_trade(i, trade, self.mark.sp)

    def to_dataframe(self):
        pass


def init_trade_position_dataframe(instruments):
    tpdf = dict()
    for inst in instruments:
        tpdf[inst] = TradePosition(inst)
    return tpdf


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
    ds[['magin', 'unit']] = ds.apply(set_margin_unit, axis=1)
    # set the moneyd
    ds['money'] = ds.price * ds.volume * ds.unit * ds.margin

    #sort
    ds = ds.sort_values(['date', 'time'],
                        ascending = [True, True])

    ds['index1'] = ds.index
    #get all instruments
    instruments = ds['inst'].unique()
    #get all trade days
    trade_days = ds['trade_day'].unique()

    # set index
    # ds.index.names = [None]
    # ds.set_index(['trade_day', 'inst', 'action', 'dir'], inplace=True)

    return ds, instruments, trade_days



def get_1d_candle(day, inst):
    dt = datetime.datetime.strptime(str(day) + '000000', "%Y%m%d%H%M%S")
    fltTime = float(time.mktime(dt.timetuple()))  # + ms

    candles = CandleData.objects(instrument=inst, period='1d', fltTime=fltTime)
    if len(candles) != 1:
        print "Error get 1d candle data: ", inst, ', @', day
        return None

    return candles[0]

def check_candle(trade_days, instruments):
    candles = pd.DataFrame(columns=instruments, index=trade_days)
    no_exists = set()
    for day in trade_days:
        for inst in instruments:
            candle = get_1d_candle(day, inst)
            if candle is None:
                no_exists.add(inst)

            candles.loc[day][inst] = candle
    return candles, no_exists


'''
myvol = pd.read_csv("/home/sean/Downloads/myvol.csv")
myvol['minus'] = myvol[['ivol', 'before', 'after']].apply(lambda x: int((float(x['before'] - x['after']))/float(x['before']) * float(x['ivol']) + 0.5), axis=1)
myvol['hold'] = myvol['ivol'] - myvol['minus']
myvol.set_index(['code'], inplace=True)
'''

def do_the_trade(i, trade, tpdf):
    # get the trade-position object
    tp = tpdf[trade.inst]
    tp.do_trade(i, trade)


ZC709 = [1674, 3021, 3302, 16292, 21593, 32691]

def simulate_trade(ds, instruments, trade_days, candles, tpdf):
    # run all trade record
    for i in np.arange(ds.shape[0]):
        trade_row = ds.iloc[i]
        do_the_trade(trade_row.index1, trade_row, tpdf)
        # if i > 10000:
        #    break


if __name__ == '__main__':
    register_connection("ctpdata", host='10.10.10.13', port=29875)
    conn = connect(db="ctpdata", host='10.10.10.13', port=29875)
    # filepath = "/home/sean/Downloads/830-en.csv"
    # filepath = '/home/sean/Downloads/73-97-en.csv'
    # filepath = '/home/sean/Downloads/cj-20170928-162410.csv'
    filepath = '/data/sean/ppp'
    ds, instruments, trade_days = get_data_source(filepath)

    candles, no_exists = check_candle(trade_days, instruments)
    if (len(no_exists) > 0):
        print "Warning: ", no_exists

    mm.reset(100000000, 1000000, 0.8, 0.00005)
    tpdf = init_trade_position_dataframe(instruments)
    simulate_trade(ds, instruments, trade_days, candles, tpdf)
    print mm.to_json()