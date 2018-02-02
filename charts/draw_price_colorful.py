import gc

import sys

import os

from core.config import DATA_DIR
from curves.price import PriceCurves
from core.utils import get_params, get_instrument_code
from draw.canvas import Canvas
from draw.graph import Graph
from draw.line import Line


colors = [(13.0 / 255.0, 57.0 / 255.0, 0.0 / 255.0),
          (21.0 / 255.0, 96.0 / 255.0, 0.0 / 255.0),
          (29.0 / 255.0, 125.0 / 255.0, 0.0 / 255.0),
          (35.0 / 255.0, 155.0 / 255.0, 0.0 / 255.0),
          (44.0 / 255.0, 196.0 / 255.0, 0.0 / 255.0),
          (51.0 / 255.0, 227.0 / 255.0, 0.0 / 255.0),
          (63.0 / 255.0, 255.0 / 255.0, 0.0 / 255.0),
          (97.0 / 255.0, 255.0 / 255.0, 51.0 / 255.0),
          (156.0 / 255.0, 255.0 / 255.0, 128.0 / 255.0),
          (194.0 / 255.0, 255.0 / 255.0, 176.0 / 255.0)
          ]

def get_line_data(line):
    dir, pos = line.split(',')[2:4]
    return int(dir), int(pos)


def load_trade_log(level, inst_code, end_date):
    # file_path = '/home/zj/v2-17/v2_%s_logs/%s-%s.log' % (level, inst_code, end_date)
    file_path = '/home/zj/detail_logs/%s-%s.log' % (inst_code, level)
    with open(file_path, 'r') as output:
        lines = output.readlines()
    return lines


def get_data_from_sigle_file(curr_price, level, instrument, end_date):
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
    # instrument = get_instrument_code(instrument, True)
    lines = load_trade_log(level, instrument, end_date)

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
    iii = 0
    lines = [Line(ax, x, y, 'black', sz='0.5', sp='--', zo=1)]
    for lvl in level:
        save_pos_x, save_pos_y = get_data_from_sigle_file(curr_price, lvl, instrument, end_date)
        line_color = colors[iii % 10]
        lines += [
                Line(ax, save_pos_x['o_l'], save_pos_y['o_l'], line_color, sz='5', sp='o', zo=2, ap=0.3),
                Line(ax, save_pos_x['c_l'], save_pos_y['c_l'], line_color, sz='5', sp='x', zo=2, ap=0.3),
                Line(ax, save_pos_x['o_s'], save_pos_y['o_s'], line_color, sz='5', sp='s', zo=2, ap=0.3),
                Line(ax, save_pos_x['c_s'], save_pos_y['c_s'], line_color, sz='5', sp='^', zo=2, ap=0.3),
            ]
        iii += 1
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
