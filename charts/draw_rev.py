import gc

import sys

import os

from core.config import TRADE_LOG_DIR
from core.utils import get_instrument_code
from curves.revenue import RevenueCurves
from curves.trade import TradeCurves
from draw.canvas import Canvas
from draw.graph import Graph
from draw.line import Line


def get_model(inst_code):
    data_path = os.path.join(TRADE_LOG_DIR, '%s.log' % inst_code)
    curr_price = RevenueCurves(TradeCurves(data_path), 2099200)
    return curr_price


def draw_rev(ax, trade):
    curr_price = RevenueCurves(trade, 2099200)
    x = curr_price.get_point_x()
    y = curr_price.get_point_y()
    graph = Graph(ax, x, y)
    lines = [
        Line(ax, x, y, 'b', sp='-')
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
    file_name = '%s-%s-%s.log' % (instrument, end_date, '_'.join(levels))
    canvas = Canvas(2, 1, 1)
    ax = canvas.ax[0]
    data_path = os.path.join(TRADE_LOG_DIR, file_name)
    draw_rev(ax, TradeCurves(data_path))
    # canvas.save_image(instrument, 'revenue')
    canvas.show_image()
    print 'Done.'
