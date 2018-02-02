import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mongoengine import *
import time

unit = dict({\
'MA709': 10, 'OI709': 10, 'RM709': 10, 'TA709': 5, 'm1709': 10, 'y1709': 10, 'ag1712': 15,\
'al1709': 5, 'au1712': 1000, 'bu1709': 10, 'cu1709': 5, 'rb1801': 10, 'zn1709': 5, 'FG709': 20,\
'a1709': 10, 'i1709': 100, 'j1709': 100, 'jm1709': 60, 'ZC709': 100, 'jd1709': 10, 'p1709': 10,\
'c1801': 10, 'l1709': 5, 'p1801': 10, 'pp1709': 5, 'ru1709': 10, 'm1801': 10, 'CF801': 5,\
'OI801': 10, 'y1801': 10, 'ni1709': 1, 'SR801': 10, 'v1709': 5, 'l1801': 5, 'TA801': 5,\
'a1801': 10, 'jd1801': 10, 'RM801': 10, 'zn1710': 5, 'al1710': 5, 'cu1710': 5, 'FG801': 20,\
'i1801': 100, 'j1801': 100, 'jm1801': 60, 'MA801': 10, 'ZC801': 100, 'bu1712': 10, 'ru1801': 10,\
'pp1801': 5, 'ni1801': 1, 'v1801': 5, 'al1711': 5, 'cu1711': 5, 'pb1710': 5, 'rb1710': 10,\
'pb1708': 5, 'CF709': 5, 'pb1709': 5, 'pb1711': 5})

commitment = dict({\
'MA709': 0.05 , 'OI709': 0.05, 'RM709': 0.05, 'TA709': 0.06, 'm1709': 0.05, 'y1709': 10, 'ag1712': 0.07,\
'al1709': 0.05, 'au1712': 0.07, 'bu1709': 0.04, 'cu1709': 0.05, 'rb1801': 0.07, 'zn1709': 0.05, 'FG709': 0.06,\
'a1709': 0.05, 'i1709': 0.05, 'j1709': 0.05, 'jm1709': 0.05, 'ZC709': 0.05, 'jd1709': 0.05, 'p1709': 0.05,\
'c1801': 0.05, 'l1709': 0.05, 'p1801': 0.05, 'pp1709': 0.05, 'ru1709': 0.05, 'm1801': 0.05, 'CF801': 0.07,\
'OI801': 0.05, 'y1801': 0.05, 'ni1709': 0.05, 'SR801': 0.06, 'v1709': 0.05, 'l1801': 0.05, 'TA801': 0.06,\
'a1801': 0.05, 'jd1801': 0.05, 'RM801': 0.05, 'zn1710': 0.05, 'al1710': 0.05, 'cu1710': 0.05, 'FG801': 0.06,\
'i1801': 0.05 , 'j1801': 0.05, 'jm1801': 0.05, 'MA801': 0.05, 'ZC801': 0.05, 'bu1712': 0.04, 'ru1801': 0.05,\
'pp1801': 0.05, 'ni1801': 0.05, 'v1801': 0.05, 'al1711':0.05 , 'cu1711': 0.05, 'pb1710': 0.07, 'rb1710': 0.05,\
'pb1708': 0.07, 'CF709': 0.07, 'pb1709': 0.07, 'pb1711': 0.07})

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



def get_candles(inst):
    register_connection("ctpdata", host='10.10.10.13', port=29875)
    conn = connect(db="ctpdata", host='10.10.10.13', port=29875)
    return CandleData.objects(instrument=inst, period='1m', strDate__gt='20170701')


time_x = dict()


def get_price_list(candles):
    global time_x
    price = []
    i = 0
    for candle in candles:
        price.append(candle.Open)
        time_x[int(candle.fltTime)] = i
        i += 1
    allx = range(0, len(price))
    return allx, price, time_x


# ds = pd.read_csv("/home/sean/Downloads/history.csv")
# accounts = ds['account'].unique()
# trades = ds[ds['account'] == accounts[0]]
# j1709 = trades[trades['instrument'] == 'j1709']



def dt_2_timet(s):
    global time_x

    idate = s['date']
    itime = s['time']
    price = s['price']
    volume = s['volume']
    inst = s['inst']
    y = idate / 10000
    M = (idate - y * 10000) / 100
    d = idate - y * 10000 - M * 100
    h = itime / 10000
    m = (itime - h * 10000) / 100
    # s = itime - h * 10000 - m * 100
    s = 0
    tt = time.mktime((y, M , d, h, m, s, 0, 0, 0))
    mins = int(h * 10000 + m * 100)
    money = price * volume * unit[inst]
    x = time_x[int(tt)]
    if x is None:
        print s, x, tt
    return pd.Series(dict(x=time_x[int(tt)], ftime=tt, mins=mins, money = money))


def get_trade_by_inst(ds, inst):
    trade_inst = ds[ds['inst'] == inst]
    trade_inst = trade_inst.merge(trade_inst.apply(dt_2_timet, axis=1), left_index=True, right_index=True)
    trade_inst.ftime = trade_inst.ftime.astype(int)
    trade_inst.mins = trade_inst.mins.astype(int)
    return trade_inst


# DO NOT REMOVE
# cols = ['ftime', 'mins']
# j1709[cols] = j1709[cols].applymap(np.int64)
# 
# j1709['mins'] = j1709['mins'].apply(np.int64)
# j1709.drop([col for col in ['p_m', 'crev','frev', 'setp'] if col in j1709],
#            axis=1, inplace=True)

# def has_price(s):
#    return pd.Series(dict(has=len(CandleData.objects(instrument='j1709', period='1m', fltTime=s.ftime)) == 1))

# j1709.apply(has_price, axis=1)






# rb1710 = trades[trades['instrument'] == 'rb1710']
# rb1801 = trades[trades['instrument'] == 'rb1801']
# j1801 = trades[trades['instrument'] == 'j1801']

# for account in accounts:
#   trades = ds[ds['account'] == account]
#   instrument = trades['instrument'].unique()
#   for inst in instrument:
#     inst_trades = trades[trades['instrument'] == instrument[0]]
#     print (inst_trades)
#
#


#1. first , group by the trade_no

def average_price(s):
    money = s['money']
    volume = s['volume']
    inst = s['inst']
    price = money / volume / unit[inst]
    return pd.Series(dict(avgprice = price))

def change_act_dir(s):
    action = s['action']
    dir = s['dir']
    if (action < 0):
        dir = -dir
        action = -1
    return pd.Series(dict(ddir = dir, act = action))

def average_price_2(s):
    money = s['money']
    volume = s['volume']
    inst = s['inst']
    price = money / volume / unit[inst]
    return pd.Series(dict(price = price))


def get_trade_group(trade_inst):
    jg_tno = trade_inst.groupby(['trade_day', 'trade_no']).agg({'account': 'first', 'trade_no': 'first', \
                                        'trade_day': 'first', 'date': 'first', \
                                        'time': 'first', 'inst': 'first', 'dir': 'first', \
                                        'action': 'first', 'price': 'first', 'volume': 'sum', \
                                        'ftime': 'first', 'mins': 'first', 'x': 'first',\
                                        'money': 'sum'})
    jg_tno = jg_tno.merge(jg_tno.apply(average_price, axis=1), left_index=True, right_index=True)
    jg_tno = jg_tno.merge(jg_tno.apply(change_act_dir, axis=1), left_index=True, right_index=True)
    jg_tno = jg_tno.sort_values(['ftime'], ascending=[True])
    jg_tno.ddir = jg_tno.ddir.astype(int)
    jg_tno.act = jg_tno.act.astype(int)

    jg_tno.drop([col for col in ['price', 'dir', 'action'] if col in jg_tno], axis=1, inplace=True)
    jg_tno = jg_tno.groupby(['ftime']).agg({'account': 'first', 'trade_no': 'first', \
                                   'trade_day': 'first', 'date': 'first', \
                                   'time': 'first', 'inst': 'first',\
                                   'avgprice': 'first', 'volume': 'sum', \
                                   'ftime': 'first', 'mins': 'first', 'x': 'first',\
                                   'money': 'sum', 'act': 'first', 'ddir': 'first'})
    jg_tno = jg_tno.sort_values(['ftime'], ascending=[True])

    jg_tno = jg_tno.merge(jg_tno.apply(average_price_2, axis=1), left_index=True, right_index=True)
    jg_tno.drop([col for col in ['avgprice'] if col in jg_tno], axis=1, inplace=True)
    return jg_tno


def draw_trade(df, inst):
    ol = []
    cl = []
    os = []
    cs = []
    pol = []
    pcl = []
    pos = []
    pcs = []

    for i in range(0, df.shape[0]):
        trade = df.iloc[i]
        if trade.act == 1:
            if trade.ddir == 1:
                ol.append(int(trade.x))
                pol.append(price[int(trade.x)])
            else:
                os.append(int(trade.x))
                pos.append(price[int(trade.x)])
        else:
            if trade.ddir == 1:
                cl.append(int(trade.x))
                pcl.append(price[int(trade.x)])
            else:
                cs.append(int(trade.x))
                pcs.append(price[int(trade.x)])


    plt.rcParams['figure.figsize'] = [16, 9]
    plt.plot(allx, price)
    if (len(cl) > 0):
        plt.plot(cl, pcl, 'ko')
    if (len(ol) > 0):
        plt.plot(ol, pol, 'rx')
    if (len(cs) > 0):
        plt.plot(cs, pcl, 'yo')
    if (len(os) > 0):
        plt.plot(os, pol, 'gx')
    plt.savefig("/home/sean/tmp/aaa/" + inst)
    plt.show()

    # return ol, cl, os, cs, pol, pcl, pos, pcs


ds = pd.read_csv("/home/sean/Downloads/830-en.csv")
instruments = ds['inst'].unique()

inst = 'j1709'
# for inst in instruments:
if (inst != ''):
    candles = get_candles(inst)
    print inst,
    if len(candles) < 1:
        print 'Can not get candles of'
        # continue
    else:
        print len(candles)
        allx, price, time_x = get_price_list(candles)
        trade_inst = get_trade_by_inst(ds, inst)
        jg_tno = get_trade_group(trade_inst)
        draw_trade(jg_tno, inst)


'''
import matplotlib.pyplot as plt
import pd as pd

def get_money(s):                                                            
  u = s['unit']                                                            
  p = s['price']
  v = s['volume']
  m = u * p * v
  return pd.Series(dict(money=m))

df = pd.read_csv('/home/sean/tmp/cc-20170830-232138.csv')
df.apply(get_money, axis=1)
df.to_csv('/home/sean/tmp/cc-20170830-232138.csv')

plt.figure(figsize=(9,9))
df1.plot(kind='pie', y = 'money', autopct='%1.1f%%', 
 startangle=90, shadow=False, labels=df['inst'], legend = False)
plt.show()
'''
'''
df.mymoney = df.mpercent * 10000000 * 0.01
df.vol = df.mymoney / (df.price * df.unit)
df['relvol'] = df.vol + 0.5
df['myvol'] = df.relvol.astype(int)
df['rmoney'] = df.myvol * df.price * df.myvol
myallm = df.rmoney.sum()
myallm
14280815.0
'''

candles = get_candles(inst)
allx, price, time_x = get_price_list(candles)
trade_inst = get_trade_by_inst(ds, inst)
jg_tno = get_trade_group(trade_inst)
draw_trade(jg_tno, inst)


hm = pd.DataFrame(columns=['money', 'revenue'] + ds.inst.unique(), \
                  index=list(ds.sort_values('trade_day').trade_day.unique()))


