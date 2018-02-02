import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mongoengine import *
import sys, time
import re
import math
from datetime import date, datetime, tzinfo, timedelta

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
        cleared = 0
        if self.vol < trade.volume:
            vdelta = self.vol
            print "close error: ", i, trade.inst, trade.trade_day, self.vol - trade.volume
        else:
            vdelta = trade.volume
        self.vol -= vdelta
        if self.vol == 0:
            cleared = 5

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
        return cleared

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
                print "can not open new position", i, trade.inst, trade.trade_day
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
                    print 'Open ', i, trade.inst, vol, self.vol, trade.dir, self.price, self.deposit, mm.my_deposit, self.pct_all
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
                        print 'Close ', i, self.crev, mp.crev, mm.my_rev, mm.mark_rev, trade.inst, trade.dir, mm.my_deposit, self.pct_all


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

    def do_trade(self, i, trade, date, time):
        self.inst = trade.inst
        self.up_day = trade.trade_day
        self.up_date = date
        self.uptime = time

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
    # set the moneyd
    ds['money'] = ds.price * ds.volume * ds.unit * ds.margin
    ds['mtime'] = ds['time'].apply(lambda x: int(x / 100) * 100)
    #sort
    ds = ds.sort_values(['date', 'time'],
                        ascending = [True, True])
    ds['index1'] = ds.index
    #get all instruments
    instruments = ds['inst'].unique()
    #get all trade days
    days = ds['date'].unique()

    # set index
    # ds.index.names = [None]
    # ds.set_index(['trade_day', 'inst', 'action', 'dir'], inplace=True)

    return ds, instruments, days


'''
myvol = pd.read_csv("/home/sean/Downloads/myvol.csv")
myvol['minus'] = myvol[['ivol', 'before', 'after']].apply(lambda x: int((float(x['before'] - x['after']))/float(x['before']) * float(x['ivol']) + 0.5), axis=1)
myvol['hold'] = myvol['ivol'] - myvol['minus']
myvol.set_index(['code'], inplace=True)
'''

def do_the_trade(i, trade, tpdf, day, minute):
    # get the trade-position object
    tp = tpdf[trade.inst]
    tp.do_trade(i, trade, day, minute)

def get_every_tick_taik(d):
    # 21:00 - 23:00, 23:00 - 23:30, 23:30 - 02:30, 9:00 - 10:15, 10:15 - 11:30, 13:30 - 15:00
    # 0:00 - 02:30, 9:00 - 10:15, 10:30 - 11:30, 13:30 - 15:00, 21:00 - 23:00, 23:00 - 23:30, 23:30 - 23:59
    # 2 * 24 + 30, 10*24+15 - 9*24, ....

    r = list()
    r.append(list(range(0, 2 * 60 + 30)))
    r.append(list(range(9 * 60, 10 * 60 + 15)))
    r.append(list(range(10 * 60 + 30, 11 * 60 + 30)))
    r.append(list(range(13 * 60 + 30, 15 * 60)))
    r.append(list(range(21 * 60, 23 * 60 + 60)))

    day = 20170101
    y = day / 10000
    m = (day - y * 10000) / 100
    d = day - y * 10000 - m * 100
    stime = datetime(y, m, d, 0, 0, 0)
    allm = []
    for i in range(0, len(r)):
        M = [(stime + timedelta(minutes=x)).strftime('%Y%m%d %H%M%S').split()[1] for x in r[i]]
        allm += M
    return allm


def get_rr(candle, tp, rev_row):
    s = 'l_' + tp.inst
    code, cc = get_instrument_code(tp.inst)
    rev_row['l_' + tp.inst] = (candle.Close - tp.my.lp.price) * tp.my.lp.vol * margin[code] * unit[code]\
                              - (candle.Close + tp.my.lp.price) * tp.my.lp.vol * margin[code] * unit[code] * mm.commision\
                              + tp.my.lp.crev
    rev_row['s_' + tp.inst] = (tp.my.lp.price - candle.Close) * tp.my.lp.vol * margin[code] * unit[code]\
                              - (candle.Close + tp.my.lp.price) * tp.my.lp.vol * margin[code] * unit[code] * mm.commision\
                              + tp.my.sp.crev
    l_m_rev = (candle.Close - tp.mark.lp.price) * tp.mark.lp.vol * margin[code] * unit[code]\
                              - (candle.Close + tp.mark.lp.price) * tp.mark.lp.vol * margin[code] * unit[code] * mm.commision\
                              + tp.mark.lp.crev
    s_m_rev = (tp.mark.lp.price - candle.Close) * tp.mark.lp.vol * margin[code] * unit[code]\
                              - (candle.Close + tp.mark.lp.price) * tp.mark.lp.vol * margin[code] * unit[code] * mm.commision\
                              + tp.mark.sp.crev
    return l_m_rev, s_m_rev


def get_day_close_candle(d, m, inst):
    candles = None
    dt = datetime.strptime(str(d) + '000000', "%Y%m%d%H%M%S")
    while True:
        dt -= timedelta(days=1)
        # strTime = '0'
        candles = CandleData.objects(instrument=inst, period='1d', fltTime=float(time.mktime(dt.timetuple())))
        if (len(candles) == 1):
            break
    return candles


def cal_revnue_risk(d, m, instruments, tpdf, revn):
    mrev = 0
    rev = 0
    strm = str(m)
    if (len(strm) < 6):
        strm = '0' * (6 - len(strm)) + strm
    dt = datetime.strptime(str(d) + strm, "%Y%m%d%H%M%S")
    for inst in instruments:
        candles = CandleData.objects(instrument=inst, period = '1m', fltTime=float(time.mktime(dt.timetuple())))
        if (len(candles) != 1):
            candles = get_day_close_candle(d, m, inst)
        tp = tpdf[inst]
        l_m_rev, s_m_rev = get_rr(candles[0], tp, revn)
        mrev += l_m_rev + s_m_rev
        rev += revn['l_' + inst] + revn['s_' + inst]

    if (mm.all_money + mrev != 0):
        mrisk = mm.all_deposit / (mm.all_money + mrev)
    else:
        mrisk = 1e10
    if (mm.my_money + rev != 0):
        risk = mm.my_deposit / (mm.my_money + rev)
    else:
        risk = 1e10

    return [mrev, mm.all_deposit, mrisk, rev, mm.my_deposit, risk]




def get_dt(day):
    r = list()
    r.append(list(range(0, 2 * 60 + 30)))
    r.append(list(range(9 * 60, 10 * 60 + 15)))
    r.append(list(range(10 * 60 + 30, 11 * 60 + 30)))
    r.append(list(range(13 * 60 + 30, 15 * 60)))
    r.append(list(range(21 * 60, 23 * 60 + 60)))

    y = day / 10000
    m = (day - y * 10000) / 100
    d = day - y * 10000 - m * 100
    stime = datetime(y, m, d, 0, 0, 0)
    allm = []
    for i in range(0, len(r)):
        M = [(stime + timedelta(minutes=x)).strftime('%Y%m%d %H%M%S').split() for x in r[i]]
        allm += M
    return allm


def init_by_minutes(instruments, dates):
    cols = np.append('l_' + instruments, 's_' + instruments)
    cols = np.append(cols, ['m_revn', 'm_dpst', 'm_risk', 'revn', 'dpst', 'risk', 'date', 'time'])
    df = pd.DataFrame(columns=cols)
    i = 0
    z = np.zeros((1, len(cols) - 2))

    for d in dates:
        allm = get_dt(d)
        for m in allm:
            df.loc[-1] = np.append(z, m)
            df.index += 1
            i += 1
    df.set_index(['date', 'time'], inplace=True)
    return df


def simulate_trade(dsgb, tpdf, instruments, days, trade_time):
    # run all trade record
    # revn_minutes = init_by_minutes(instruments, days)
    # revn_minutes = pd.read_csv('/data/sean/revn-180.csv')
    revn_minutes = pd.read_csv('/data/sean/template_minutes-29175.csv')
    revn_minutes.set_index(['date', 'time'], inplace=True)

    for i in range(151, revn_minutes.shape[0]):
    # for i in range(17910, revn_minutes.shape[0]):
        r = revn_minutes.iloc[i]
        d, m = r.name
        # print i, d, m, (int(d), int(m)) in trade_time
        if (int(d), int(m)) in trade_time:
            g = dsgb.get_group((int(d), int(m)))
            g = g.sort_values('time', ascending=True)
            # print g
            for i in np.arange(g.shape[0]):
                trade_row = g.iloc[i]
                do_the_trade(trade_row.index1, trade_row, tpdf, d, int(m))
        r['m_revn', 'm_dpst', 'm_risk', 'revn', 'dpst', 'risk'] = cal_revnue_risk(d, m, instruments, tpdf, r)

                   # candle = CandleData.objects(instrument=inst, period='1m', strDate=dt[0], strTime=dt[1])
    return revn_minutes



if __name__ == '__main__':
    register_connection("ctpdata", host='10.10.10.13', port=29875)
    conn = connect(db="ctpdata", host='10.10.10.13', port=29875)
    # filepath = "/home/sean/Downloads/830-en.csv"
    filepath = '/home/sean/Downloads/73-97-en.csv'
    ds, instruments, days = get_data_source(filepath)
    dsgb = ds.groupby(['date', 'mtime'])
    trade_time = list(dsgb.groups.keys())

    mm.reset(100000000, 1000000, 0.8, 0.00005)
    tpdf = init_trade_position_dataframe(instruments)
    revn_minutes = simulate_trade(dsgb, tpdf, instruments, days, trade_time)
    revn_minutes.to_csv("/data/sean/revn.csv")
    print mm.to_json()
