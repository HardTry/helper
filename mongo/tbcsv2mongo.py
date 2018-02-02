import csv, json
from pymongo import *
import sys, time, datetime, math

from pymongo.errors import DuplicateKeyError

global mongodb, tickdata


class TickData:
    def __init__(self):
        self.instrument = str("")
        self.strDate = int(0)
        self.strTime = str("")
        self.fltTime = float(0)
        self.Volume = float(0)
        self.askVolume1 = float(0)
        self.bidVolume1 = float(0)
        self.lastPrice = float(0)
        self.askPrice1 = float(0)
        self.bidPrice1 = float(0)
        self.openInterest = float(0)

    def __init__(self, instrument):
        self.instrument = instrument
        self.strDate = int(0)
        self.strTime = str("")
        self.fltTime = float(0)
        self.Volume = float(0)
        self.askVolume1 = float(0)
        self.bidVolume1 = float(0)
        self.lastPrice = float(0)
        self.askPrice1 = float(0)
        self.bidPrice1 = float(0)
        self.openInterest = float(0)

    # sscanf(buf, "%[^,],0.%[^,],%d,%d,%d,%d,%d,%lf,%lf,%lf,%lf", date, time,
    #       &ignore1, &mmd.Volume, &ignore2, &mmd.AskVolume1, &mmd.BidVolume1,
    #       &mmd.LastPrice, &mmd.AskPrice1, &mmd.BidPrice1, &mmd.OpenInterest);
    def getData(self, row):
        ok = True
        self.strDate = row[0]
        self.strTime = row[1]
        b = float(row[1]) * 1000000
        c = int(b + 0.4)
        
        ms = b - float(c)
        if ms < 0:
            c -= 1
            ms = b - float(c)

        if ms > 0.999:
           c += 1
           ms = b - float(c)

        d = str(c)

        #if abs(b- float(c)) > 0.9:
        #    print self.strDate, self.strTime, b, c, d, ms
        #    ok = False
        #    return ok

        if (len(d) < 6):
            d = '0' * (6 - len(d)) + d
        if (len(d) == 6):
            try:
              dt = datetime.datetime.strptime(self.strDate + d, "%Y%m%d%H%M%S")
              self.fltTime = float(time.mktime(dt.timetuple())) + ms
              self.Volume = float(row[3])
              self.askVolume1 = float(row[5])
              self.bidVolume1 = float(row[6])
              self.lastPrice = float(row[7])
              self.askPrice1 = float(row[8])
              self.bidPrice1 = float(row[9])
              self.openInterest = float(row[10])
              # print d, ms, self.fltTime
            except ValueError:
              print self.strDate, self.strTime, b, c, d, ms
              ok = False
        else:
            self.fltTime = float(0)
            ok = False

        return ok

    def tojson(self):
        return json.dumps(self.__dict__)

    def dict(self):
        return self.__dict__


def write_tick_to_mongo(datapath, datafile, instrument):
    global mongodb, tickdata
    with open(datapath + '/' + datafile, "r") as tickcsv:
        lines = csv.reader(tickcsv)
        i = 0
        for row in lines:
            # sprint(row), type(row)
            tick = TickData(instrument)
            ok = tick.getData(row)
            # tick.printTick()
            # print tick.dict()
            # print i, row
            if (i % 5000) == 0:
                print instrument, i

            if ok:
                try:
                    tickdata.insert_one(tick.dict())
                    # pass
                except DuplicateKeyError:
                    pass
            else:
                print instrument, i, row

            i += 1
        print "finished. ", i


# tickdata.remove()


def open_monog(mongo_uri):
    global mongodb, tickdata
    mongodb = MongoClient(mongo_uri).ctpdata
    tickdata = mongodb.tickdata
    return tickdata
    # cursor = db.tick.find() #{"lesson": 37})


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print "Usage tbcsv2mongo.py <datapath> <datafile> <mongo uri> <instrument>"
        print "Default: /data/sean/20170508 test_data.csv 10.10.10.13:29875 rb1710"
        exit(0)

    datapath = sys.argv[1]  # raw_input("enter datapath, default is /data/sean/20170508 :")
    datafile = sys.argv[2]  # raw_input("enter datafile, default is test_data.csv :")
    mongo_uri = sys.argv[3]  # raw_input ("enter mongo_uri, default is 10.10.10.13:29875 :")
    instrument = sys.argv[4]  # raw_input ("enter instrunmet, default is rb1710 :")

    open_monog(mongo_uri)
    write_tick_to_mongo(datapath, datafile, instrument)
