from mongoengine import *


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


def save_spread(rb1710, rb1801):
    assert isinstance(rb1710, Tick)
    assert isinstance(rb1801, Tick)
    if rb1801.strDate != rb1710.strDate:
        print "warning: trade day is not same at time", rb1801.fltTime, rb1801.strDate, rb1710.strDate

    spread = Spread(inst1="rb1710", inst2="rb1801",
                    fltTime=rb1801.fltTime,
                    strDate=rb1801.strDate,
                    spdLast=rb1710.lastPrice - rb1801.lastPrice,
                    spdAsk1=rb1710.askPrice1 - rb1801.askPrice1,
                    spdBid1=rb1710.bidPrice1 - rb1801.bidPrice1,
                    tick1=rb1710.id, tick2=rb1801.id)
    spread.save()


Tick_rb1801 = Tick.objects(instrument='rb1801')
j = 0
for rb1801 in Tick_rb1801:
    assert isinstance(rb1801, Tick)
    rb1710 = Tick.objects(instrument="rb1710", fltTime=rb1801.fltTime)
    if rb1710.count() == 1:
        save_spread(rb1710[0], rb1801)
        j += 1
    else:
        rb1710 = Tick.objects(instrument="rb1710", fltTime__gt=rb1801.fltTime - 60, fltTime__lte = rb1801.fltTime)
        if rb1710.count() == 0:
            print "error:", rb1801.strDate, rb1801.fltTime
        else:
            save_spread(rb1710[rb1710.count() - 1], rb1801)
            # print rb1710[rb1710.count() - 1].fltTime - rb1710[0].fltTime
            j += 1


print j
