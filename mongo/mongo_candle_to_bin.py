from mongoengine import *
import libnrlib
import matplotlib.pyplot as plt
import gc
import sys
import os

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


def candle_2_candle(candle):
    return libnrlib.CandleData(
        candle.fltTime     ,
        candle.Open        ,
        candle.High        ,
        candle.Low         ,
        candle.Close       ,
        candle.Volume      ,
        candle.openInterest,
        candle.instrument.encode('ascii'),
        candle.period.encode('ascii'),
        candle.strDate.encode('ascii'),
        candle.strTime.encode('ascii'))


def candle_2_candle_bar(candle):
    return libnrlib.CandleBar(
        candle.fltTime     ,
        candle.Open        ,
        candle.High        ,
        candle.Low         ,
        candle.Close       ,
        candle.Volume      ,
        candle.openInterest)


def save_candle_data_file(inst, period, datapath, from_day):
    register_connection("ctpdata", host='10.10.10.13', port=29875)
    conn = connect(db="ctpdata", host='10.10.10.13', port=29875)
    tdays = CandleData.objects(instrument=inst, period=period).distinct("strDate")

    for day in tdays:
        if day < from_day:
            continue

        print day,
        # bars = libnrlib.VecCandleData()
        bars = libnrlib.VecCandleBar()
        candles = CandleData.objects(instrument=inst, period=period, strDate=day)
        for candle in candles:
            # bar = candle_2_candle(candle)
            bar = candle_2_candle_bar(candle)
            bars.append(bar)

        print " bars len is ", len(bars)

        filepath = datapath + '/' + inst + '/' + inst + '-10s-' + day + ".bin"
        print filepath
        # libnrlib.write_mongo_candle(filepath.encode('ascii'), bars)
        libnrlib.write_mongo_candle_v4(filepath.encode('ascii'), bars)

    conn.close()

def test_read_data(inst, day):
    last = []
    ask = []
    bid = []
    filepath = "/data/sean/10s_candle_20170808/bindata/" + inst + "-10s-" + day + ".bin"

    libnrlib.read_mongo_tick(filepath, 20, last, ask, bid)

    x = list(range(0, len(last)))

    plt.plot(x, last)
    plt.plot(x, ask)
    plt.plot(x, bid)

    plt.show()

# get_data()

def save_days(inst, period, path):
    register_connection("ctpdata", host='10.10.10.13', port=29875)
    conn = connect(db="ctpdata", host='10.10.10.13', port=29875)
    tdays = CandleData.objects(instrument=inst, period= period).distinct("strDate")
    conn.close()

    vs = libnrlib.VectorString()
    vs.extend(libnrlib.CppString(day.encode("ascii")) for day in tdays)
    filepath = path + '/' + inst + '/tdays.bin'
    ret = libnrlib.save_trade_days(filepath.encode("ascii"), vs)

    print ret


# save_days()

def load_days(path):
    days = libnrlib.VectorString()
    ret = libnrlib.load_trade_days_2(path, days)
    # for day in days:
    #    print day
    print "days ", ret, len(days)


def load_bars(inst, period, path, day):
    filepath = path + '/' + inst + '/' + inst + '-' + period + '-' + day + '.bin'
    print filepath

    bars = libnrlib.VecCandleData()
    ret = libnrlib.load_mongo_candle(filepath, bars)
    print "bars ", ret, len(bars)
    for bar in bars:
        print bar.ftime, bar.Open, bar.High, bar.Low, bar.Close, bar.Volume


def load_ts(inst, period, path, day):
    if period != '10s':
        return False

    datapath = path + '/' + inst
    minsize = 102400
    price = []
    ftime = []
    # ret = libnrlib.load_ts_from_10s_candle(inst, datapath, day, minsize, price, ftime)
    ret = libnrlib.load_10s_ts_from_date(inst, datapath, day, minsize, price, ftime)
    print " load ts ret is ", ret, len(price), len(ftime)
    # plt.plot(ftime, price)
    x = range(0, len(price))
    plt.plot(x, price)
    plt.show()



if __name__ == "__main__":
    gc.disable()
    gc.enable()

    if (len(sys.argv) < 5):
        print 'Usage: python mongo_candle_to_bin.py <options> <instrument> <period> <data file path> [day]\n'\
              '    python mongo_candle_to_bin.py s al888 10s /data/sean/10s_candle_20170808/bindata\n'\
              's for save candle data file\n'\
              'l for load bars\n'\
              't for load time series\n'
    else:
        op = sys.argv[1].encode('ascii')
        inst = sys.argv[2].encode('ascii')
        period = sys.argv[3].encode('ascii')
        path = sys.argv[4].encode('ascii')
        day = ''
        if len(sys.argv) == 6:
          day = sys.argv[5].encode('ascii')

        if op == 's':
            # try:
            #   os.mkdir(path + '/' + inst, 0700)
            # finally:
            #   pass
            save_candle_data_file(inst, period, path, day)
            save_days(inst, period, path)
        elif op == 'l':
            filepath = path + '/' + inst + '/tdays.bin'
            load_days(filepath)
            load_bars(inst, period, path, day)
        elif op == 't':
            load_ts(inst, period, path, day)
