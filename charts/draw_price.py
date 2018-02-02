import gc

import sys

import os

from core.config import DATA_DIR
from curves.price import PriceCurves
from core.utils import get_params, get_instrument_code
from draw.canvas import Canvas
from draw.graph import Graph
from draw.line import Line


def get_line_data(line):
    dir, pos = line.split(',')[2:4]
    return int(dir), int(pos)


def load_trade_log(level, inst_code, end_date):
    # file_path = '/home/zj/v2-17/v2_%s_logs/%s-%s.log' % (level, inst_code, end_date)
    file_path = '/home/zj/detail_logs/%s-%s.log' % (inst_code, level)
    with open(file_path, 'r') as output:
        lines = output.readlines()
    return lines


def get_data_from_file(curr_price, levels, instrument, end_date):
    data_x = {
        'o_l': [],
        'o_s': [],
        'c_l': [],
        'c_s': []
    }
    data_y = {
        'o_l': [],
        'o_s': [],
        'c_l': [],
        'c_s': []
    }
    lines = []
    # instrument = get_instrument_code(instrument, True)
    for level in levels:
        lines += load_trade_log(level, instrument, end_date)

    for line in lines:
        if line.startswith('Open'):
            dir, pos = get_line_data(line)
            if dir > 0:
                data_x['o_l'].append(pos)
                data_y['o_l'].append(curr_price.get_y_from_x(pos))
            else:
                data_x['o_s'].append(pos)
                data_y['o_s'].append(curr_price.get_y_from_x(pos))
        if line.startswith('Close'):
            dir, pos = get_line_data(line)
            if dir > 0:
                data_x['c_l'].append(pos)
                data_y['c_l'].append(curr_price.get_y_from_x(pos))
            else:
                data_x['c_s'].append(pos)
                data_y['c_s'].append(curr_price.get_y_from_x(pos))
    return data_x, data_y


def draw_price(ax, instrument, end_date, level, start):
    params = get_params(instrument, end_date, 0)
    data_path = os.path.join(DATA_DIR, instrument)
    curr_price = PriceCurves(params, data_path, start)
    x = curr_price.get_point_x()
    y = curr_price.get_point_y()
    graph = Graph(ax, x, y)
    save_pos_x, save_pos_y = get_data_from_file(curr_price, level, instrument, end_date)
    lines = [
        Line(ax, x, y, 'b', sp='-'),
        Line(ax, save_pos_x['o_l'], save_pos_y['o_l'], 'r', sp='o'),
        Line(ax, save_pos_x['c_l'], save_pos_y['c_l'], 'r', sp='^'),
        Line(ax, save_pos_x['o_s'], save_pos_y['o_s'], 'g', sp='o'),
        Line(ax, save_pos_x['c_s'], save_pos_y['c_s'], 'g', sp='^')
    ]
    graph.draw_line(lines)


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
    # end_date = sys.argv[2].encode('ascii')
    # split = int(sys.argv[3])  # worker
    # tindex = int(sys.argv[4])
    # level = 0
    start = 2099200

    canvas = Canvas(1, 1, 1)
    ax = canvas.ax[0]
    draw_price(ax, instrument, end_date, levels, start)
    # canvas.save_image(instrument, 'price')
    canvas.show_image()
    print 'Done.'
