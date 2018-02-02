import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mongoengine import *
import time
import re
from datetime import date, datetime, tzinfo, timedelta
from matplotlib import rcParams


margin = dict({'CF': 0.07, 'FG': 0.06, 'MA': 0.05, 'OI': 0.05, 'RM': 0.05, 'SR': 0.06, 'TA': 0.06, 'ZC': 0.05, 'a': 0.05, 'ag': 0.07, 'al': 0.05, 'au': 0.07, 'bu': 0.04, 'c': 0.05, 'cu': 0.05, 'i': 0.05, 'j': 0.05, 'jd': 0.05, 'jm': 0.05, 'l': 0.05, 'm': 0.05, 'ni': 0.05, 'p': 0.05, 'pb': 0.07, 'pp': 0.05, 'rb': 0.07, 'ru': 0.05, 'v': 0.05, 'y': 0.05, 'zn': 0.05})
unit = dict({'CF': 5, 'FG': 20, 'MA': 10, 'OI': 10, 'RM': 10, 'SR': 10, 'TA': 5, 'ZC': 100, 'a': 10, 'ag': 15, 'al': 5, 'au': 1000, 'bu': 10, 'c': 10, 'cu': 5, 'i': 100, 'j': 100, 'jd': 10, 'jm': 60, 'l': 10, 'm': 10, 'ni': 1, 'p': 10, 'pb': 5, 'pp': 5, 'rb': 10, 'ru': 10, 'v': 5, 'y': 10, 'zn': 5})
jump = dict({'CF': 5, 'FG': 1, 'MA': 1, 'OI': 2, 'RM': 1, 'SR': 1, 'TA': 2, 'ZC': 2, 'a': 1, 'ag': 1, 'al': 5, 'au': 5, 'bu': 2, 'c': 1, 'cu': 10, 'i': 5, 'j': 5, 'jd': 1, 'jm': 5, 'l': 5, 'm': 1, 'ni': 10, 'p': 2, 'pb': 5, 'pp': 1, 'rb': 1, 'ru': 5, 'v': 5, 'y': 2, 'zn': 5})


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
def get_day_close_candle(d, m, inst):
    strm = str(m)
    if (len(strm) < 6):
        strm = '0' * (6 - len(strm)) + strm
    adt = datetime.strptime(str(d) + strm, "%Y%m%d%H%M%S")
    td = timedelta(minutes=1)
    dt = adt
    for i in range(0, 10):
        dt -= td
        candles = CandleData.objects(instrument=inst, period='1m', fltTime=float(time.mktime(dt.timetuple())))
        if (len(candles) == 1):
            return candles[0]
    td = timedelta(hours=1)
    dt = adt
    for i in range(0, 10):
        dt -= td
        candles = CandleData.objects(instrument=inst, period='1m', fltTime=float(time.mktime(dt.timetuple())))
        if (len(candles) == 1):
            return candles[0]
    td -= timedelta(days=1)
    dt = datetime.strptime(str(d) + '000000', "%Y%m%d%H%M%S")
    while True:
        dt -= td
        candles = CandleData.objects(instrument=inst, period='1d', fltTime=float(time.mktime(dt.timetuple())))
        if (len(candles) == 1):
            return candles[0]


def get_price(instruments):
    prices = pd.read_csv('/data/sean/template_minutes-29175.csv')
    prices.set_index(['date', 'time'], inplace=True)
    for i in range(151, prices.shape[0]):
        r = prices.iloc[i]
        d, m = r.name
        strm = str(m)
        if (len(strm) < 6):
            strm = '0' * (6 - len(strm)) + strm
        print d, strm
        dt = datetime.strptime(str(d) + strm, "%Y%m%d%H%M%S")
        for inst in instruments:
            candles = CandleData.objects(instrument=inst, period='1m', fltTime=float(time.mktime(dt.timetuple())))
            if (len(candles) != 1):
                if i == 151:
                    candle = get_day_close_candle(d, m, inst)
                else:
                    candle = None
            else:
                candle = candles[0]
            if candle is None:
                prev = prices.iloc[i - 1]
                r['l_' + inst] = prev['l_' + inst]
                r['s_' + inst] = prev['s_' + inst]
            else:
                r['l_' + inst] = candle.Close
                r['s_' + inst] = candle.Close
            # print inst, dt, r['l_' + inst], r['s_' + inst]
    prices.to_csv('/data/sean/prices-2.csv')
    return prices



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

cfrev = []

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
            # print "close error: ", i, trade.inst, trade.trade_day, self.vol - trade.volume
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
                    print '1,' + trade.inst + ',' + str(int(vol)) + ',' + str(trade.dir) + ',' + str(trade.price) + ',' + str(trade.date) + ',' + str(trade.time)
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
                        # print 'Close ', self.crev, mp.crev, mm.my_rev, mm.mark_rev, trade.inst, trade.dir, mm.my_deposit, self.pct_all
                        print '-1,' + trade.inst + ',' + str(int(vol)) + ',' + str(trade.dir) + ',' + str(
                            trade.price) + ',' + str(trade.date) + ',' + str(trade.time)

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


    def get_revenue(self, price, trade_unit):
        frev = (price - self.price) * self.vol * trade_unit
        if not self.is_long:
            frev = -frev
        frev -= (price + self.price) * self.vol * trade_unit * mm.commision
        return self.crev, frev


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

    def get_revenue(self, price, is_long, trade_unit):
        if is_long:
            p = self.lp
        else:
            p = self.sp

        return p.get_revenue(price, trade_unit)


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

    def get_revenue(self, price, is_my, is_long, trade_unit):
        if (is_my):
            ps = self.my
        else:
            ps = self.mark
        return ps.get_revenue(price, is_long, trade_unit)



def init_trade_position_dataframe(instruments):
    tpdf = dict()
    for inst in instruments:
        tpdf[inst] = TradePosition(inst)
    return tpdf



def do_the_trade(i, trade, tpdf):
    # get the trade-position object
    tp = tpdf[trade.inst]
    tp.do_trade(i, trade)


def get_datetime(d, t):
    tt = str(t)
    if (len(tt) < 6):
        tt = '0' * (6 - len(tt)) + tt
    return datetime.strptime(str(d) + tt, "%Y%m%d%H%M%S")

def get_all_datetime(keys):
    d = []
    for k in keys:
        d.append(get_datetime(k[0], k[1]))
    return np.array(d)

def do_cal_rev(tpdf, instruments, prices, revn, si, ei):
    for i in range(si, ei):
        r = revn.iloc[i]
        p = prices.iloc[i]
        mrev = 0
        for inst in instruments:
            code, cc = get_instrument_code(inst)
            trade_unit = unit[code]
            # if i >= 19432 and inst == 'rb1801':
            #     pass

            tp = tpdf[inst]
            crev, frev = tp.get_revenue(p['l_' + inst], True, True, trade_unit)
            rev = crev + frev
            mrev += rev
            r['l_' + inst] = rev
            crev, frev = tp.get_revenue(p['s_' + inst], True, False, trade_unit)
            rev = crev + frev
            mrev += rev
            r['s_' + inst] = rev
        r['revn'] = mrev
        r['dpst'] = mm.my_deposit


def simulate_trade(ds, tpdf, instruments, prices, revn):
    # run all trade record
    keys = prices.index.values
    key_array = get_all_datetime(keys)

    trade_row = ds.iloc[0]
    cur_td_dt = get_datetime(trade_row.date, trade_row.mtime)

    aa = np.where(key_array == cur_td_dt)
    cur_price_pos = aa[0][0]

    for i in range(ds.shape[0]):
        trade_row = ds.iloc[i]

        td_dt = get_datetime(trade_row.date, trade_row.mtime)
        # print td_dt
        if (td_dt > cur_td_dt):
            aa = np.where(key_array == td_dt)
            price_pos = aa[0][0]
            do_cal_rev(tpdf, instruments, prices, revn, cur_price_pos, price_pos)
            cur_td_dt = td_dt
            cur_price_pos = price_pos

        do_the_trade(trade_row.index1, trade_row, tpdf)
        # if i > 10000:
        #    break

    trade_row = ds.iloc[ds.shape[0] - 1]
    td_dt = get_datetime(trade_row.date, trade_row.mtime)
    aa = np.where(key_array == td_dt)
    price_pos = aa[0][0]
    do_cal_rev(tpdf, instruments, prices, revn, cur_price_pos, price_pos + 1)


if __name__ == '__main__':
    register_connection("ctpdata", host='10.10.10.13', port=29875)
    conn = connect(db="ctpdata", host='10.10.10.13', port=29875)
    filepath = '/data/sean/analysis/73-97-en.csv'
    ds, instruments, days = get_data_source(filepath)
    dsgb = ds.groupby(['date', 'mtime'])
    # prices = get_price(instruments)
    prices = pd.read_csv('/data/sean/prices-2.csv')
    prices = prices[160:27034]
    # prices = prices[['date', 'time', 'l_rb1801', 's_rb1801', 'm_revn', 'm_dpst', 'm_risk', 'revn', 'dpst', 'risk']]
    prices.set_index(['date', 'time'], inplace=True)

    revn = pd.read_csv('/data/sean/template_minutes-29175.csv')
    revn = revn[160:27034]
    # revn = revn[['date', 'time', 'l_rb1801', 's_rb1801', 'm_revn', 'm_dpst', 'm_risk', 'revn', 'dpst', 'risk']]
    revn.set_index(['date', 'time'], inplace=True)

    mm.reset(100000000, 500000, 0.6, 0.00005)
    tpdf = init_trade_position_dataframe(instruments)
    simulate_trade(ds, tpdf, instruments, prices, revn)
    print mm.to_json()
    revn.to_csv('/data/sean/revn-50-60.csv')
    
    rcParams['figure.figsize'] = 16, 9

    for inst in instruments:
        revn[['l_' + inst, 's_' + inst]].plot(color=['r', 'g'])
        plt.suptitle(inst)
        plt.savefig('/data/sean/pppp/' + inst + '-revn.png')
        plt.close()

    pds = pd.Series(index=instruments)
    for inst in instruments:
        pds[inst] = revn.iloc[-1]['l_' + inst] + revn.iloc[-1]['s_' + inst]
    pds = pds[pds != 0]
    pds = pds.sort_values()
    pds.plot(kind='bar')
    plt.suptitle('all revenue')
    # plt.show()
    plt.savefig('/data/sean/pppp/revn-bars.png')
    plt.close()

    pds = pds[pds > 0]
    pds.plot(kind='pie')
    plt.suptitle('all revenue')
    # plt.show()
    plt.savefig('/data/sean/pppp/revn-pie.png')
    plt.close()

    a = []
    for i in range(revn.shape[0]):
        a.append(np.sum(np.array(revn.iloc[i])))

    ar = pd.Series(a, index=revn.index) / 500000 * 100
    ar.plot(color='b')
    plt.savefig('/data/sean/pppp/revn-all.png')
    plt.close()

    revn.dpst.plot(color='b')
    plt.savefig('/data/sean/pppp/revn-dpst.png')
    plt.close()
