# -*- coding: UTF-8 -*-
# author: star at gom
# created_at: 2017-12-27 17:49
# import Interest
import re

import time

from core.config import *
from core.utils import get_margin, get_unit, get_hop
from model import Interest


class Gom(object):
    interests = {}
    total = Interest()

    def open_interest(self, inst, direction, vol, price, uptime, pos):
        inst_dir, interest = self.get_interest(inst, direction)
        if interest is None:
            interest = Interest(inst, inst_dir,
                                magin=get_margin(inst), unit=get_unit(inst), hop=get_hop(inst))
            self.interests.setdefault(inst_dir, interest)
        m = price * vol * interest.magin * interest.unit # zhan yong zi jin
        interest.money += m  # price * vol * inte->magin * inte->unit;
        interest.volume += vol
        interest.avg_price = interest.money / (interest.volume * interest.magin * interest.unit)
        self.total.uptime = interest.uptime = uptime
        self.total.money += m
        self.total.volume += vol

        # print "Open %s, %d, %ld %.02lf > %.02lf, %.02lf\n" % \
        #       (inst, direction, pos, price, interest.money, self.total.money)

    def close_interest(self, inst, direction, vol, price, uptime, pos):
        inst_dir, interest = self.get_interest(inst, direction)
        if interest is None:
            return -1
        if interest.volume < vol:
            return -2
        rev = (price - interest.avg_price) * interest.unit * vol
        if direction < 0:
            rev = -rev
        rev -= (price + interest.avg_price) * interest.unit * vol * g_commision
        interest.cls_rev += rev
        self.total.cls_rev += rev
        self.total.flt_rev -= interest.flt_rev
        self.total.all_rev -= interest.all_rev

        m = interest.avg_price * interest.magin * interest.unit * vol
        interest.money -= m
        interest.volume -= vol

        if interest.volume > 0:
            interest.avg_price = interest.money / (interest.volume * interest.magin * interest.unit)
            rev = (price - interest.avg_price) * interest.unit * interest.volume
            if direction < 0:
                rev = -rev
            rev -= (price + interest.avg_price) * interest.unit * interest.volume * g_commision
            interest.flt_rev = rev
        else:
            interest.avg_price = 0
            interest.flt_rev = 0

        interest.all_rev = interest.flt_rev + interest.cls_rev

        self.total.flt_rev += interest.flt_rev
        self.total.all_rev += interest.all_rev
        self.total.uptime = interest.uptime = uptime
        self.total.money -= m
        self.total.volume -= vol

        # print "%d, %.02lf, %.02lf, %d--->%.02lf" % (direction, price, interest.avg_price, pos, self.total.all_rev)

        # print "Close %s, %d, %ld %.02lf> %.02lf, %.02lf |%.02lf, %.02lf| %.02lf, %.02lf\n" % \
        #       (inst, direction, pos, price, interest.all_rev, interest.cls_rev, self.total.all_rev,
        #        self.total.cls_rev, interest.money, self.total.money)

    def update_interest(self, inst, direction, price, uptime, pos):
        inst_dir, interest = self.get_interest(inst, direction)
        if interest is None:
            return -1

        rev = (price - interest.avg_price) * interest.unit * interest.volume

        if direction < 0:
            rev = -rev

        rev -= (price + interest.avg_price) * interest.unit * interest.volume * g_commision

        self.total.flt_rev -= interest.flt_rev
        self.total.all_rev -= interest.all_rev

        interest.flt_rev = rev
        interest.all_rev = interest.flt_rev + interest.cls_rev

        self.total.flt_rev += interest.flt_rev
        self.total.all_rev += interest.all_rev
        self.total.uptime = interest.uptime = uptime
        # print self.total.all_rev
        # ji suan shape a
        # ji suan shi jian an mei tian zui hou yi ci ji lu
        # print "Update %s, %d, %ld %.02lf> %.02lf, %.02lf |%.02lf, %.02lf| %.02lf, %.02lf\n" % \
        #       (inst, direction, pos, price, interest.all_rev, interest.flt_rev, self.total.all_rev,
        #        self.total.cls_rev, interest.money, self.total.money)
        return 0

    def get_sharpe_ratio(self):
        pass

    def get_rp(self):
        pass

    def get_op(self):
        pass

    def get_interest(self, inst, direction):
        inst_dir = "%s%d" % (inst, direction)
        interest = self.interests.get(inst_dir)
        return inst_dir, interest

    def get_total(self):
        return self.total

# vol = 10
# price = 10000
# ttime = 1516888704
# gom = Gom()
# gom.open_interest('rb888', DIRECTION_TYPE.LONG, vol, price, ttime, 10000)
#
# for i in range(1, 500):
#     price += i * 10
#     ttime += i * 1000
# gom.update_interest('rb888', DIRECTION_TYPE.LONG, price, ttime, 11000)
#
# for i in range(1, 500):
#     price -= i * 10
#     ttime += i * 1000
#     gom.update_interest('rb888', DIRECTION_TYPE.LONG, price, ttime, 11000)
#
# gom.close_interest('rb888', DIRECTION_TYPE.LONG, vol, price, ttime, 12000)
# print gom.interests.get('rb8881').volume