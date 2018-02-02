import threading

import sys

import gc

import os

from core.config import DATA_DIR
from core.utils import get_params


class FigureThread(threading.Thread):
    def __init__(self, m12, shot, params, save_pos, trade=None):
        super(FigureThread, self).__init__()
        self.m12 = m12
        self.shot = shot
        self.trade = trade
        self.params = params
        self.save_pos = save_pos

    def run(self):
        # ani_lines1 = price.PriceAnimation(self.m12, self.shot, self.trade, self.params, 0, self.save_pos)
        # # self.ani_dash = Dashboard(self.dm)
        # plt.show()
        pass


if __name__ == '__main__':
    gc.disable()
    gc.enable()

    if len(sys.argv) < 3 or len(sys.argv) > 5:
        print 'Usage: python cppmath.py <instrument> <r|the end day> [start pos] [end pos]\n'
        exit(0)

    instrument = sys.argv[1].encode('ascii')
    end_date = sys.argv[2].encode('ascii')
    data_path = os.path.join(DATA_DIR, instrument)
    trade_name = ''
    params = get_params(instrument, end_date, level)
