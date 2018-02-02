from mongoengine import *
import pandas as pd
import matplotlib.pyplot as plt


register_connection("ctpdata", host='10.10.10.13', port=29875)
a = connect(db="ctpdata", host='10.10.10.13', port=29875)
print a


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


class Spread(Document):
    inst1 = StringField()
    inst2 = StringField()
    fltTime = FloatField()
    strDate = StringField()
    spdLast = FloatField()
    spdAsk1 = FloatField()
    spdBid1 = FloatField()
    tick1 = ObjectIdField()
    tick2 = ObjectIdField()
    meta = {
        'collection': 'spread'
    }


def save_spread(ary, rb1710, rb1801):
    ary.append([rb1801.fltTime,
               rb1710.lastPrice,
               rb1710.askPrice1,
               rb1710.bidPrice1,
               rb1801.lastPrice,
               rb1801.askPrice1,
               rb1801.bidPrice1,
               rb1710.lastPrice - rb1801.lastPrice,
               rb1710.askPrice1 - rb1801.askPrice1,
               rb1710.bidPrice1 - rb1801.bidPrice1])


tdays = Tick.objects(instrument='rb1801').distinct("strDate")
j = 0
for day in tdays:
    Tick_rb1801 = Tick.objects(instrument='rb1801', strDate=day)
    ary=[]
    for rb1801 in Tick_rb1801:
        rb1710 = Tick.objects(instrument="rb1710", strDate=day, fltTime=rb1801.fltTime)
        # if j > 10:
        #    break
        if rb1710.count() == 1:
            save_spread(ary, rb1710[0], rb1801)
            j += 1
        else:
            rb1710 = Tick.objects(instrument="rb1710", strDate=day, fltTime__gt=rb1801.fltTime - 60, fltTime__lte = rb1801.fltTime)
            if rb1710.count() == 0:
                print "error:", rb1801.strDate, rb1801.fltTime
            else:
                save_spread(ary, rb1710[rb1710.count() - 1], rb1801)
                # print rb1710[rb1710.count() - 1].fltTime - rb1710[0].fltTime
                j += 1

    df = pd.DataFrame(ary, columns=['ft', '10L', '10A', '10B', '01L', '01A', '01B', 'SL', 'SA', 'SB'])
    df = (df - df.mean()) / (df.max() - df.min())
    df = df - df.min()
    df[['10L', '10A', '10B', '01L', '01A', '01B']] = df[['10L', '10A', '10B', '01L', '01A', '01B']] + 1.5

    # fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(25, 25))
    # df[['10L', '01L']].plot(ax=axes[0,0])
    # df[['10A', '01A']].plot(ax=axes[0,1])
    # df[['10B', '01B']].plot(ax=axes[1,0])
    # df[['SL', 'SA', 'SB']].plot(ax=axes[1,1])
    plt.rcParams["figure.figsize"] = [12, 0.75 * 9]
    df[['10L', 'SL', 'SA', 'SB']].plot()
    plt.savefig("/tmp/images/rbspread-" + day + '.png')
    # break