import gc

import sys

import os

from core.config import TRADE_LOG_DIR
from core.utils import get_instrument_code
from curves.trade import TradeCurves
from draw.canvas import Canvas
from draw_money import draw_money
from draw_price import draw_price
from draw_rev import draw_rev

if __name__ == '__main__':
    gc.disable()
    gc.enable()

    if len(sys.argv) != 3:
        print 'Usage: python dl6.py <instrument>\n'
        exit(0)

    inst_code = sys.argv[1].encode('ascii')
    end_date = sys.argv[2].encode('ascii')
    level = 0
    start = 2099200
    # inst_code = get_instrument_code(instrument, True)
    canvas = Canvas(1, 2, 2)

    draw_price(canvas.ax[0], inst_code, end_date, level, start)

    data_path = os.path.join(TRADE_LOG_DIR, '%s.log' % inst_code)
    trade = TradeCurves(data_path)
    draw_rev(canvas.ax[2], trade)
    draw_money(canvas.ax[3], trade)
    canvas.show_image()
    print 'Done.'
