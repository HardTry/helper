from libnrlib import *
import tmath, trade, draw_framework8
import matplotlib.pyplot as plt
from matplotlib import rcParams
import sys, gc, threading, time, random, datetime
import random


def read_pos_from_file(inst):
    s = False
    str_pos = []
    # filepath = './logs/' + inst + '.log'
    filepath = '/app/sean/bin/gom/bin/v3_logs/' + inst + '.log'
    with open(filepath) as f:
        for line in f:
            if s:
                str_pos = line.split(',')
                del str_pos[-1]
                s = False
            if line.startswith('['):
                s = True
            if line.startswith(']'):
                break

    pos = []
    for sp in str_pos:
        pos.append(int(sp))

    if (len(pos) % 2 != 0):
        print 'Error position number'
        return None

    l = random.randint(500, len(pos) / 2 - 1)
    return pos[l * 2], pos[l * 2 + 1]


class FigureThread(threading.Thread):
    def __init__(self, m12, shot, params, save_pos, stop_pos, trade = None):
        super(FigureThread, self).__init__()
        self.m12 = m12
        self.shot = shot
        self.trade = trade
        self.params = params
        self.save_pos = save_pos
        self.stop_pos = stop_pos

    def run(self):
        ani_lines1 = animation7.SubplotAnimation7(self.m12, self.shot, self.trade, self.params, 0, self.save_pos, self.stop_pos)

        # self.ani_dash = Dashboard(self.dm)
        plt.show()

def get_random_instrument():
    ic = ['a9888',
      'ag888',
      'al888',
      'au888',
      'bu888',
      'c9888',
      'CF888',
      'cu888',
      'FG888',
      'i9888',
      'j9888',
      'jm888',
      'l9888',
      'm9888',
      'MA888',
      'ni888',
      'OI888',
      'p9888',
      'rb888',
      'RM888',
      'SR888',
      'TA888',
      'v9888',
      'y9888',
      'zn888']
    return ic[random.randint(0, len(ic) - 1)]



if __name__ == "__main__":
    gc.disable()
    gc.enable()

    instrument = get_random_instrument()
    # thedate = '20180126'
    thedate = '20171108'
    datapath = '/app/sean/data/10s_candle_bindata'
    trade_name = ''

    params = tmath.Params()
    ppps = NRParams()

    params.run_status = 0
    params.delta = 1
    params.inst = instrument
    params.date = thedate
    params.data_len = 1024
    params.imgpath = '/app/sean/tmp'

    m12 = Math12()
    if instrument == 'rb888':
        ppps.min_data_size = int(1024 * 2048 * 3)
    else:
        ppps.min_data_size = int(1024 * 2048 * 1.5)

    m12.set_param(ppps)
    datapath += '/' + instrument
    all_len = m12.get_data_from_file(instrument, datapath, thedate, trade.get_hop(instrument))
    shot = None

    inst_code = trade.get_instrument_code(instrument)
    spos = 0
    while spos < params.minlen + 2048:
        spos, epos = read_pos_from_file(inst_code)
        spos -= 5000

    print instrument, 'all data', all_len, 'start from', spos, 'to', epos

    g_trader = None

    rc_params = {'legend.fontsize': 'small',
                 'axes.labelsize': 'small',
                 'axes.titlesize': 'small',
                 'xtick.labelsize': 'small',
                 'ytick.labelsize': 'small'}

    for key, value in sorted(rc_params.iteritems()):
        rcParams[key] = value

    params.curpos = spos

    save_pos = []
    stop_pos = [spos + 5000, epos]


    draw = draw_framework8.DrawFramework8(m12, shot, g_trader, params, 0)
    pos = spos
    while pos <= epos:
        m12.do_math(pos)
        draw.draw_frame(pos)
        if pos in stop_pos:
            print pos, 'save'
            draw.save_frame()
        pos += 1
    print 'Done.'
