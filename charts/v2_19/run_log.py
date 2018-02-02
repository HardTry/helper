import gc
import sys
import os
import time

from core.config import DATA_DIR, DIRECTION_TYPE
from core.utils import get_params, write_log
from curves.price import PriceCurves
from trade.gom import Gom


def get_line_data(line):
    dir, pos = line.split(',')[2:4]
    return int(dir), int(pos)


def load_trade_log(level, inst_code):
    file_path = '/home/zj/detail_logs/%s-%s.log' % (inst_code, level)
    if os.path.exists(file_path):
        with open(file_path, 'r') as output:
            lines = output.readlines()
        return lines
    return []


def load_trade_point_data(levels, instrument, end_date):
    open_long = []
    open_short = []
    close_long = []
    close_short = []
    lines = []
    for level in levels:
        lines += load_trade_log(level, instrument, end_date)

    for line in lines:
        if line.startswith('Open'):
            dir, pos = get_line_data(line)
            if dir > 0:
                open_long.append(pos)
            else:
                open_short.append(pos)
        if line.startswith('Close'):
            dir, pos = get_line_data(line)
            if dir > 0:
                close_long.append(pos)
            else:
                close_short.append(pos)
    return open_long, open_short, close_long, close_short


if __name__ == '__main__':
    gc.disable()
    gc.enable()

    if len(sys.argv) < 3:
        print 'Usage: python dl6.py <instrument> [<level>...]\n'
        exit(0)

        instrument = sys.argv[1].encode('ascii')
        levels = list(set(sys.argv[2::]))
        levels.sort()
        end_date = '20180126'
        o_l, o_s, c_l, c_s = load_trade_point_data(levels, instrument, end_date)
        if len(o_l) + len(o_s) + len(c_l) + len(c_s) == 0:
            print 'log is not'
            exit(0)
        params = get_params(instrument, end_date, 0)
        data_path = os.path.join(DATA_DIR, instrument)
        curr_price = PriceCurves(params, data_path, 2099200)
        curr_price.get_point_y()
        gom = Gom()
        file_name = '%s/%s-%s.log' % (end_date, instrument, '_'.join(levels))
        for point in curr_price.get_point_x():
            price = curr_price.get_y_from_x(point)
            if point in c_l:
                gom.close_interest(
                    instrument, DIRECTION_TYPE.LONG, c_l.count(point), price, time.time(), point
                )
            if point in c_s:
                gom.close_interest(
                    instrument, DIRECTION_TYPE.SHORT, c_s.count(point), price, time.time(), point
                )
            if point in o_l:
                gom.open_interest(
                    instrument, DIRECTION_TYPE.LONG, o_l.count(point), price, time.time(), point
                )
            if point in o_s:
                gom.open_interest(
                    instrument, DIRECTION_TYPE.SHORT, o_s.count(point), price, time.time(), point
                )

            gom.update_interest(
                params.inst, DIRECTION_TYPE.LONG, price, time.time(), point
            )
            gom.update_interest(
                params.inst, DIRECTION_TYPE.SHORT, price, time.time(), point
            )

            write_log(gom.get_total(), file_name)

    print 'Done.'
