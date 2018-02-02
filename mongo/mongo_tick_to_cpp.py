from mongoengine import *
import libnrlib
import matplotlib.pyplot as plt

class Tick(Document):
    askVolume1 = FloatField()
    lastPrice = FloatField()
    askPrice1 = FloatField()
    bidPrice1 = FloatField()
    strDate = StringField()
    Volume = FloatField()
    instrument = StringField()
    bidVolume1 = FloatField()
    openInterest = FloatField()
    strTime = StringField()
    fltTime = FloatField()

    meta = {
        'collection': 'tickdata'
    }




def get_data():
    register_connection("ctpdata", host='10.10.10.13', port=29875)
    conn = connect(db="ctpdata", host='10.10.10.13', port=29875)
    tdays = Tick.objects(instrument='rb888').distinct("strDate")

    j = 0
    for day in tdays:
        ticks = Tick.objects(instrument='rb888', strDate=day)
        j += 1
        print j, day
        mtptr = libnrlib.new_mongo_tick_array(len(ticks))
        i = 0
        for tick in ticks:
            libnrlib.new_mongo_tick(mtptr, i,
                           tick.lastPrice,
                           tick.askPrice1,
                           tick.bidPrice1,
                           tick.Volume,
                           tick.askVolume1,
                           tick.bidVolume1,
                           tick.openInterest,
                           tick.fltTime,
                           tick.strDate.encode("ascii"),
                           tick.strTime.encode("ascii"))
            i += 1

        filepath = "/data/sean/20170508/bindata/rb888/" + day + ".bin"
        libnrlib.write_mongo_tick(filepath.encode("ascii"), mtptr, len(ticks))
        libnrlib.free_mongo_tick_array(mtptr)

    conn.close()

def test_read_data():
    last = []
    ask = []
    bid = []
    filepath = "/data/sean/20170508/bindata/rb888/20100104.bin"

    libnrlib.read_mongo_tick(filepath, 20, last, ask, bid)

    x = list(range(0, len(last)))

    plt.plot(x, last)
    plt.plot(x, ask)
    plt.plot(x, bid)

    plt.show()

# get_data()

def save_days():
    register_connection("ctpdata", host='10.10.10.13', port=29875)
    conn = connect(db="ctpdata", host='10.10.10.13', port=29875)
    tdays = Tick.objects(instrument='rb888').distinct("strDate")
    conn.close()

    vs = libnrlib.VectorString()
    vs.extend(libnrlib.CppString(day.encode("ascii")) for day in tdays)
    filepath = "/data/sean/20170508/bindata/rb888/tdays.bin"
    ret = libnrlib.save_trade_days(filepath.encode("ascii"), vs)

    print ret


# save_days()

def load_days():
    filepath = "/data/sean/20170508/bindata/rb888"
    date = '20150601'
    last = []
    ask = []
    bid = []
    ret = libnrlib.load_trade_datay(date, filepath, 20, 20480, last, ask, bid)

    print ret, len(last)


load_days()