# -*- coding: UTF-8 -*-
# author: star at a
# created_at: 2017-12-15 11:22

import os
import collections


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.dirname('/app/data/10s_candle_bindata/')

TRADE_LOG_DIR = os.path.join(BASE_DIR, 'logs')

DRAW_DIR = os.path.join(BASE_DIR, 'images')


dir_coll = collections.namedtuple(
    'ORDER_ACTION_TYPE', ('CLOSE_TODAY', 'CLOSE_YESTERDAY', 'UNKNOW', 'OPEN')
)
ORDER_ACTION_TYPE = dir_coll(-2, -1, 0, 1)

dir_coll = collections.namedtuple(
    'DIRECTION_TYPE', ('SHORT', 'UNKNOW', 'LONG')
)
DIRECTION_TYPE = dir_coll(-1, 0, 1)

dir_coll = collections.namedtuple(
    'ORDER_PRICE_TYPE', ('LIMIT', 'MARKET')
)
ORDER_PRICE_TYPE = dir_coll(0, 1)

dir_coll = collections.namedtuple(
    'ORDER_STATUS', ('UNKNOW', 'OK', 'PART', 'ALL', 'RECALL')
)
ORDER_STATUS = dir_coll(0, 1, 2, 4, 8)

del dir_coll

g_margin = {
    "CF": 0.07,
    "FG": 0.07,
    "MA": 0.07,
    "OI": 0.07,
    "RM": 0.06,
    "SR": 0.05,
    "TA": 0.06,
    "ZC": 0.08,
    "a": 0.07,
    "ag": 0.07,
    "al": 0.08,
    "au": 0.06,
    "bu": 0.08,
    "c": 0.07,
    "cu": 0.08,
    "i": 0.1,
    "j": 0.12,
    "jd": 0.08,
    "jm": 0.12,
    "l": 0.07,
    "m": 0.07,
    "ni": 0.1,
    "p": 0.07,
    "pb": 0.08,
    "pp": 0.07,
    "rb": 0.11,
    "ru": 0.12,
    "v": 0.07,
    "y": 0.07,
    "zn": 0.08
}

g_unit = {
    "CF": 5,
    "FG": 20,
    "MA": 10,
    "OI": 10,
    "RM": 10,
    "SR": 10,
    "TA": 5,
    "ZC": 100,
    "a": 10,
    "ag": 15,
    "al": 5,
    "au": 1000,
    "bu": 10,
    "c": 10,
    "cu": 5,
    "i": 100,
    "j": 100,
    "jd": 10,
    "jm": 60,
    "l": 5,
    "m": 10,
    "ni": 1,
    "p": 10,
    "pb": 5,
    "pp": 5,
    "rb": 10,
    "ru": 10,
    "v": 5,
    "y": 10,
    "zn": 5
}

g_hop = {
    "CF": 5,
    "FG": 1,
    "MA": 1,
    "OI": 2,
    "RM": 1,
    "SR": 1,
    "TA": 2,
    "ZC": 2,
    "a": 1,
    "ag": 1,
    "al": 5,
    "au": 5,
    "bu": 2,
    "c": 1,
    "cu": 10,
    "i": 5,
    "j": 5,
    "jd": 1,
    "jm": 5,
    "l": 5,
    "m": 1,
    "ni": 10,
    "p": 2,
    "pb": 5,
    "pp": 1,
    "rb": 1,
    "ru": 5,
    "v": 5,
    "y": 2,
    "zn": 5,
    "b": 1
}

g_commision = 0.0005

g_dont_trade = {
    "jm": 0.07,
    "FG": 0.07,
    "MA": 0.07,
    "OI": 0.07,
    "RM": 0.06,
    "SR": 0.05
}
