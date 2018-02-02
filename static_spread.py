from mongoengine import *
import pandas as pd
import matplotlib.pyplot as plt
import csv

register_connection("ctpdata", host='10.10.10.13', port=29875)
a = connect(db="ctpdata", host='10.10.10.13', port=29875)
# print a


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



# tdays is class mongoengine.base.datastructures.BaseList
tdays = Tick.objects(instrument='rb1801').distinct("strDate")
#print type(tdays), tdays
arySpread = []
# i = 0
for day in tdays:
    spread_set = Spread.objects(strDate = day)

    strDate = spread_set[0].strDate
    ary = []
    for spread in spread_set:
        # print vls
        # ary.append([spread.fltTime, spread.spdLast, spread.spdAsk1, spread.spdBid1])
        ary.append([spread.spdLast, spread.spdAsk1, spread.spdBid1])

    # cols = ['time', 'last', 'ask1', 'bid1']
    cols = ['last', 'ask1', 'bid1']
    df = pd.DataFrame(ary, columns=cols)
    # print strDate, df.max()['last'], df.min()['last'], df.max()['last'] - df.min()['last']
    arySpread.append([df.max()['last'], df.min()['last'], df.max()['last'] - df.min()['last'],
                      df.max()['ask1'], df.min()['ask1'], df.max()['ask1'] - df.min()['ask1'],
                      df.max()['bid1'], df.min()['bid1'], df.max()['bid1'] - df.min()['bid1']])
    # df.plot()
    # plt.show()
    #
    # a = str(raw_input("enter a key to continue, q = exit: "))
    # if a == 'q':
    #    break
    # i += 1
    # if i > 3:
    #     break

dfSpread = pd.DataFrame(arySpread, columns=['lmax', 'lmin', 'ldif', 'amax', 'amin', 'adif', 'bmax', 'bmin', 'bdif'])
# print dfSpread.tail(5)
print dfSpread.max(), dfSpread.min(), dfSpread.max() - dfSpread.min(), dfSpread.mean(), dfSpread.std()

dfSpread.to_csv("rb1710-rb1801-spread-20170508.csv")

fig, axes = plt.subplots(nrows=3, ncols=1)
dfSpread[['lmax', 'lmin', 'ldif']].plot(ax=axes[0]); axes[0].set_title('Last')
dfSpread[['amax', 'amin', 'adif']].plot(ax=axes[1]); axes[1].set_title('Ask1')
dfSpread[['bmax', 'bmin', 'bdif']].plot(ax=axes[2]); axes[2].set_title('Bid1')


# dfSpread.plot(subplots=True)
plt.show()
plt.savefig('rb1710-rb1801-spread-20170508.png')
