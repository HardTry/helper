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

def find_candle_data_file(inst, period, day):
    register_connection("ctpdata", host='10.10.10.13', port=29875)
    conn = connect(db="ctpdata", host='10.10.10.13', port=29875)
    o = []
    h = []
    l = []
    c = []
    candles = CandleData.objects(instrument=inst, period=period, strDate=day)
    for candle in candles:
        if candle.Open < 2000:
            print candle.strDate, candle.strTime, candle.Open

        o.append(candle.Open)
        h.append(candle.High)
        l.append(candle.Low)
        c.append(candle.Close)
    conn.close()

    print "bars len is ", len(candles)
    return o, h, l, c


if __name__ == "__main__":
    gc.disable()
    gc.enable()

    if (len(sys.argv) != 4):
        print 'Usage: python show_candle.py <instrument> <period> <day>'
    else:
        inst = sys.argv[1].encode('ascii')
        period = sys.argv[2].encode('ascii')
        day = sys.argv[3].encode('ascii')

        o, h, l, c = find_candle_data_file(inst, period, day)
        x = list(range(0, len(o)))
        # plt.plot(x, o)
        # plt.plot(x, h)
        # plt.plot(x, l)
        # plt.plot(x, c)

        # plt.show()