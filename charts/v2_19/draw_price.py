import gc
import sys
import os

from core.config import DATA_DIR
from curves.price import PriceCurves
from core.utils import get_params, get_instrument_code, load_file
from draw.canvas import Canvas
from draw.graph import Graph
from draw.line import Line
#
# def get_line_data(line):
#     dir, pos = line.split(',')[2:4]
#     return int(dir), int(pos)
#
#
# def load_trade_log(level, inst_code):
#     file_path = '/home/zj/detail_logs/%s-%s.log' % (inst_code, level)
#     return load_file(file_path)
#
#
# def get_data_from_file(curr_price, level, instrument):
#     data_x = {
#         'o_l': [],
#         'o_s': [],
#         'c_l': [],
#         'c_s': []
#     }
#     data_y = {
#         'o_l': [],
#         'o_s': [],
#         'c_l': [],
#         'c_s': []
#     }
#     # lines = []
#     inst_code = get_instrument_code(instrument, True)
#     # for level in levels:
#     #     lines += load_trade_log(level, inst_code, end_date)
#
#     for line in load_trade_log(level, inst_code):
#         if line.startswith('Open'):
#             dir, pos = get_line_data(line)
#             if dir > 0:
#                 data_x['o_l'].append(pos)
#                 data_y['o_l'].append(curr_price.get_y_from_x(pos))
#             else:
#                 data_x['o_s'].append(pos)
#                 data_y['o_s'].append(curr_price.get_y_from_x(pos))
#         if line.startswith('Close'):
#             dir, pos = get_line_data(line)
#             if dir > 0:
#                 data_x['c_l'].append(pos)
#                 data_y['c_l'].append(curr_price.get_y_from_x(pos))
#             else:
#                 data_x['c_s'].append(pos)
#                 data_y['c_s'].append(curr_price.get_y_from_x(pos))
#     return data_x, data_y
#
#
# def draw_action_point(ax, x, y, color):
#     return [
#         Line(ax, x['o_l'], y['o_l'], color=color, sp='^', marksize=8),
#         Line(ax, x['c_l'], y['c_l'], color=color, sp='*', marksize=8),
#         Line(ax, x['o_s'], y['o_s'], color=color, sp='v', marksize=8),
#         Line(ax, x['c_s'], y['c_s'], color=color, sp='x', marksize=8)
#     ]
#
#

def draw_price(ax, instrument, end_date, levels, start, colors):
    params = get_params(instrument, end_date, 0)
    data_path = os.path.join(DATA_DIR, instrument)
    curr_price = PriceCurves(params, data_path, start)
    x = curr_price.get_point_x()
    y = curr_price.get_point_y()
    # print curr_price.len
    graph = Graph(ax, x, y)
    from v2_19.test import DrawPrice
    log_path = '/home/zj/detail_logs/%s-%s.log'
    draw_price = DrawPrice(ax, (x, y), instrument, levels, log_path)
    lines = draw_price.draw(colors)
    graph.draw_line(lines)



