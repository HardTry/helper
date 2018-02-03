from libnrlib import *
import tmath, trade, animation7
import matplotlib.pyplot as plt
from matplotlib import rcParams
import sys, gc, threading, time, random, datetime
import random


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
    thedate = '20180126'
    datapath = '/app/sean/data/10s_candle_bindata'
    trade_name = ''

    params = tmath.Params()
    ppps = NRParams()

    params.run_status = 0
    params.delta = 1
    params.inst = instrument
    params.date = thedate
    params.data_len = 1024

    m12 = Math12()
    if instrument == 'rb888':
        ppps.min_data_size = int(1024 * 2048 * 3)
    else:
        ppps.min_data_size = int(1024 * 2048 * 1.5)

    m12.set_param(ppps)
    datapath += '/' + instrument
    all_len = m12.get_data_from_file(instrument, datapath, thedate, trade.get_hop(instrument))
    shot = Snapshot()

    trade.get_instrument_code(instrument)

    epos = all_len - 1
    spos = params.minlen + 2048

    print instrument, 'all data', all_len, 'start from', spos, 'to', epos, 'start at',
    spos = random.randint(spos, epos)
    params.curpos = spos
    print spos

    g_trader = None


    rc_params = {'legend.fontsize': 'small',
                 'axes.labelsize': 'small',
                 'axes.titlesize': 'small',
                 'xtick.labelsize': 'small',
                 'ytick.labelsize': 'small'}

    for key, value in sorted(rc_params.iteritems()):
        rcParams[key] = value

    m12.do_math(params.curpos)

    save_pos = []
    inst_code = trade.get_instrument_code(instrument)
    stop_pos = []

    t_figure = FigureThread(m12, shot, params, save_pos, stop_pos, g_trader)
    t_figure.start()

    params.run_status = 0
    key_level = [4, 5]

    while params.run_status >= 0 and params.curpos <= epos:
        if params.run_status == 1:
            m12.do_math(params.curpos)

            if params.curpos in stop_pos:
               print params.curpos,
               s = str(raw_input("Enter to continue:"))

            params.curpos += params.delta

        time.sleep(params.interval)

    print 'Press X and Close figure to quit'
    t_figure.join()
