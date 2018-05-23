import csv
import sys
import time
from datetime import datetime

from influxdb import client as influxdb
from influxdb.resultset import ResultSet


class CandleData:
    def __init__(self):
        self.instrument = str("")
        self.period = str("")
        self.strDate = str("")
        self.strTime = str("")
        self.fltTime = float(0)
        self.Volume = float(0)
        self.Open = float(0)
        self.High = float(0)
        self.Low = float(0)
        self.Close = float(0)
        self.openInterest = float(0)

    def __init__(self, instrument, period):
        self.instrument = instrument
        self.period = period
        self.strDate = int(0)
        self.strTime = str("")
        self.fltTime = float(0)
        self.Volume = float(0)
        self.Open = float(0)
        self.High = float(0)
        self.Low = float(0)
        self.Close = float(0)
        self.openInterest = float(0)

    # 20100104, 0.09, 4500, 4503, 4464, 4469, 6136, 1338414
    # 20100104, 0.09001, 4469, 4473, 4469, 4473, 4036, 1351708
    # 20100104, 0.09002, 4473, 4475, 4472, 4473, 3800, 1352104
    # 20100104, 0.09003, 4473, 4473, 4471, 4471, 3524, 1352220
    # 20100104, 0.09004, 4470, 4473, 4470, 4472, 3114, 1358974
    # 20100104, 0.09005, 4473, 4475, 4473, 4473, 2646, 1358714
    def getData(self, row):
        ok = True
        self.strDate = row[0]
        self.strTime = row[1]
        d = str(int(float(row[1]) * 1000000 + 0.5))
        if (len(d) < 6):
            d = '0' * (6 - len(d)) + d
        # print self.strDate + d
        if (len(d) == 6):
            dt = datetime.strptime(self.strDate + d, "%Y%m%d%H%M%S")
            self.fltTime = float(time.mktime(dt.timetuple()))  # + ms
        else:
            self.fltTime = float(0)
            ok = False

        self.Open = float(row[2])
        self.High = float(row[3])
        self.Low = float(row[4])
        self.Close = float(row[5])
        self.Volume = float(row[6])
        self.openInterest = float(row[7])

        # print d, ms, self.fltTime
        return ok

    # dt, o, h, l, c, v, i
    # 2017 / 07 / 05 22:23:00, 1113.0, 1113.0, 1112.5, 1113.0, 60, 282226

    def getData_2(self, row):
        dt = datetime.strptime(row[0], "%Y/%m/%d %H:%M:%S")
        self.fltTime = float(time.mktime(dt.timetuple()))  # + ms
        self.strDate, self.strTime = row[0].split()
        self.strDate.replace('/', '')
        self.strTime.replace(':', '')
        self.Open = float(row[1])
        self.High = float(row[2])
        self.Low = float(row[3])
        self.Close = float(row[4])
        self.Volume = float(row[4])
        self.openInterest = float(row[6])

        # print d, ms, self.fltTime
        return True

    def tojson(self):
        data = {
            "measurement": self.instrument,
            "time": datetime.fromtimestamp(self.fltTime),
            "fields": {
                "open": self.Open,
                "high": self.High,
                "low": self.Low,
                "close": self.Close,
                "volume": self.Volume,
                "open_interest": self.openInterest
            }
        }
        return data

    def dict(self):
        return self.__dict__


def write_candle_to_mongo(datapath, datafile, instrument, period, format=1):
    db = influxdb.InfluxDBClient("127.0.0.1", 8086, "", "", "tick")
    data = []
    with open(datapath + '/' + datafile, "r") as tickcsv:
        lines = csv.reader(tickcsv)
        i = 0
        for row in lines:
            if (i % 5000) == 0:
                print instrument, period, i

            candle = CandleData(instrument, period)
            if format == 1:
                ok = candle.getData(row)
            else:
                ok = candle.getData_2(row)
            curr_time = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime(candle.fltTime))
            sql = "select count(volume) from %s where time = '%s'" % (instrument, curr_time)
            result = db.query(sql)
            if len(result.items()) == 0:
                data.append(candle.tojson())
            # else:
            #    print 'data exists ', curr_time
            i += 1
        db.write_points(data)
        print "finished. ", i


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print "Usage tbk2mongo.py <datapath> <datafile> <instrument> <period>"
        print "example: /data/sean/20170508 test_candle.csv 10.10.10.13:29875 rb1710 10s"
        print "period are 10s, 1m, 1h, 1d"
        exit(0)

    datapath = sys.argv[1]  # raw_input("enter datapath, default is /data/sean/20170508 :")
    datafile = sys.argv[2]  # raw_input("enter datafile, default is test_data.csv :")
    instrument = sys.argv[3]  # raw_input ("enter mongo_uri, default is 10.10.10.13:29875 :")
    period = sys.argv[4]  # raw_input ("enter instrunmet, default is rb1710 :")

    write_candle_to_mongo(datapath, datafile, instrument, period)
