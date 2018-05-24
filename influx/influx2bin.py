import struct
import sys
import time

import os
from influxdb import client as influxdb


def write_tdays(days, path):
    file_path = os.path.join(path, 'tdays.bin')
    old_days = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as fr:
            old_days = fr.readlines()[0].split('\x00')[:-1]
        os.remove(file_path)
    with open(file_path, 'wb') as fd:
        days = list(set(old_days + days))
        days.sort()
        days.append('')
        wd = '\x00'.join(days)
        fd.write(wd)

    print 'update file: %s' % file_path


def write_data(rows, path, instrument):
    day = ''.join(days[i].split('T')[0].split('-'))
    file_name = '%s-10s-%s.bin' % (instrument, day)
    file_path = os.path.join(path, file_name)
    if os.path.exists(file_path):
        # print 'File is exists: %s' % file_path
        # return day
        os.remove(file_path)
    with open(file_path, 'wb') as fd:
        for data in rows:
            byte_objects = struct.pack(
                '7d',
                time.mktime(time.strptime(data.get('time'), '%Y-%m-%dT%H:%M:%SZ')),
                float(data.get('open')),
                float(data.get('high')),
                float(data.get('low')),
                float(data.get('close')),
                float(data.get('volume')),
                float(data.get('open_interest'))
            )
            # print data.get('time')
            fd.write(byte_objects)
    print 'save to file: %s' % file_path
    return day


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage influx2bin.py <datapath> <instrument> <start date>"
        print "example: /data/sean/datapath rb1810 20180101"
        exit(0)
    datapath = sys.argv[1]
    instrument = sys.argv[2]
    sdate = sys.argv[3]
    sdate = '%s-%s-%sT00:00:00Z' % (sdate[0:4], sdate[4:6], sdate[6:])
    # print sdate

    dir_path = os.path.join(datapath, instrument)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    db = influxdb.InfluxDBClient("127.0.0.1", 18081, "", "", "tick")

    days_sql = "select count(volume) from %s where time >= '%s' group by time(1d) tz('Asia/Shanghai')" % (instrument, sdate)
    # print days_sql
    result = db.query(days_sql)
    days = []
    for row in result[instrument]:
        if row.get('count') > 0:
            days.append(row.get('time'))
    format_days = []
    for i in range(0, len(days)):
        sql = "select * from %s where time >= '%s'" % (instrument, days[i])
        if i + 1 < len(days):
            sql = "%s and time < '%s'" % (sql, days[i+1])
        result = db.query(sql)
        if len(result) > 0:
            fday = write_data(result[instrument], dir_path, instrument)
            format_days.append(fday)
    write_tdays(format_days, dir_path)
