# -*- coding: UTF-8 -*-
# author: star at b
# created_at: 2017-12-27 11:46
from core.config import *
# import MySQLdb
#
# # 打开数据库连接
# db = MySQLdb.connect("localhost", "testuser", "test123", "TESTDB")
#
# # 使用cursor()方法获取操作游标
# cursor = db.cursor()

# class Model(object):
#
#     def __init__(self):
#         self.host = 'localhost'
#         self.name = 'uname'
#         self.passwd = 'dbpass'
#         self.db = 'dbname'
#         self.connect = MySQLdb.connect(self.host, self.name, self.passwd, self.db)
#         self.cursor = self.connect.cursor()


class Order(object):

    def __init__(self, inst, inst_dir, id=0, sysid=0,
                 action=ORDER_ACTION_TYPE.UNKNOW, direction=DIRECTION_TYPE.UNKNOW, volume=0, price=0,
                 ptype=ORDER_PRICE_TYPE.LIMIT, ttime=0, utime=0, status=ORDER_STATUS.UNKNOW):
        self.id = id
        self.sysid = sysid
        self.inst = inst
        self.inst_dir = inst_dir
        self.action = action
        self.direction = direction
        self.volume = volume
        self.price = price
        self.ptype = ptype
        self.ttime = ttime
        self.utime = utime
        self.status = status


class TradeRecord(object):
    def __init__(self, id=0, sysid=0, order_id=0, volume=0, price=0.00, ttime=0, utime=0):
        self.id = id
        self.sysid = sysid
        self.order_id = order_id
        self.volume = volume
        self.price = price
        self.ttime = ttime
        self.utime = utime


class Interest(object):

    def __init__(self, inst='', inst_dir='', direction=DIRECTION_TYPE.UNKNOW, volume=0,
                 avg_price=0.00, flt_rev=0.00,
                 cls_rev=0.00, all_rev=0.00, money=0.00,
                 magin=0.00, unit=0.00, hop=0.00, uptime=0):
        self.inst = inst
        self.inst_dir = inst_dir
        self.direction = direction
        self.volume = volume
        self.avg_price = avg_price
        self.all_rev = all_rev
        self.flt_rev = flt_rev
        self.cls_rev = cls_rev
        self.money = money
        self.magin = magin
        self.unit = unit
        self.hop = hop
        self.uptime = uptime
