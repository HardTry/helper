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
    tdays = Tick.objects(instrument='i9888', strDate__gte=u'20170508').distinct("strDate")
    print len(tdays), type(tdays), tdays
    #for day in tdays:
    #    print day

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


#load0_days()

get_data()
