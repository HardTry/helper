import tmath, trade, animation
import matplotlib.pyplot as plt
from matplotlib import rcParams
import sys, gc, threading, time, random, datetime
from libnrlib import *

class FigureThread(threading.Thread):
    def __init__(self, dm, params, save_pos, trade = None):
        super(FigureThread, self).__init__()
        self.dm = dm
        self.trade = trade
        self.params = params
        self.save_pos = save_pos

    def run(self):
        ani_lines1 = animation.SubplotAnimation(self.dm, self.trade, self.params, 0, self.save_pos)

        # self.ani_dash = Dashboard(self.dm)
        plt.show()

if __name__ == "__main__":
    gc.disable()
    gc.enable()

    if (len(sys.argv) != 5 and len(sys.argv) != 6):
        print 'Usage: python auto_game.py <instrument> <r|the trade day> <data file path> <trader name> [start pos]\n' \
              '       1. r means you want a random day\n' \
              '          format of trade day is YYYYMMDD\n' \
              '       2. trade name: <s|p> \'s\' for SimpleTrade, \'p\' for PrepareTrade\n' \
              '       3. the data file path tell game where is the store of history data\n' \
              '       4. For example:\n' \
              '          get random trade-day data\n' \
              '            python auto_game.py rb888 r /data/sean/10s_candle_bindata 1 s 1024000\n' \
              '          get one day data\n' \
              '            python auto_game.py rb888 20150601 /data/sean/10s_candle_bindata p 0\n\n' \
              '  Keyboard:                              \n' \
              '      t: toggle to show/hiden future data\n' \
              '      r: pause/run\n' \
              '      x: quit   \n'
    else:
        params = tmath.Params()

        instrument = sys.argv[1].encode('ascii')
        thedate = sys.argv[2].encode('ascii')
        datapath = sys.argv[3].encode('ascii') + '/' + instrument
        trade_name = sys.argv[4].encode('ascii')

        trade.get_instrument_code(instrument)

        params.run_status = 0
        params.delta = 1
        params.inst = instrument
        params.date = thedate
        params.data_len = 1024

        pointer, price, all_len, allx, the_date = \
            tmath.get_data_from_file(instrument, datapath, thedate, \
                                     params.min_data_size, params.predict_len)
        if (pointer == 0) or (all_len < params.min_data_size):
            exit(-100)

        params.all_len = all_len

        if len(sys.argv) != 6:
             spos = params.minlen + 2048
        elif sys.argv[5] == 'r':
            random.seed(datetime.datetime.now())
            spos = int(random.random() * (all_len - params.minlen) + params.minlen)
        else:
            spos = int(sys.argv[5])
            # dt = sys.argv[5].encode('ascii')
            # spos = get_time_pos(pointer, dt)
            # if spos < 0:
            #     print 'error when get time pos'
            #     exit(-101)
            # elif spos < params.minlen:
            #     print 'less than minlen'
            #    exit(-102)

        tmath.release_time_pos_map(pointer)

        print 'all data', all_len, 'start from ', spos

        params.curpos = spos

        # g_trader = trade.get_trader(trade_name)
        # g_trader.set_dm(dm)
        g_trader = None

        dm = []
        power = 1
        lendm = 12
        hop = trade.get_hop(instrument)
        for i in range(0, lendm):
            dm.append(tmath.DataMath(price, all_len, allx, the_date, hop, params))
            dm[i].down_sample(2 * power)
            power *= 2

        # opq = str(raw_input("enter something to draw: (q = quit)"))
        # if (opq == 'q'):
        #    exit(0)

        rc_params = {'legend.fontsize': 'small',
                     'axes.labelsize': 'small',
                     'axes.titlesize': 'small',
                     'xtick.labelsize': 'small',
                     'ytick.labelsize': 'small'}

        for key, value in sorted(rc_params.iteritems()):
            rcParams[key] = value

        for i in range(0, len(dm)):
            dm[i].do_math(params.curpos)

        save_pos = [all_len - 1]
        t_figure = FigureThread(dm, params, save_pos, g_trader)
        t_figure.start()

        if len(save_pos) > 0:
            last_pos = save_pos[-1] + 1
        else:
            last_pos = all_len

        # params.run_status = 1
        while params.run_status >= 0 and params.curpos < last_pos:
            if params.run_status == 1:
                for i in range(0, len(dm)):
                    dm[i].do_math(params.curpos)

                if params.curpos in save_pos:
                    time.sleep(3)

                # g_trader.do_trade(instrument, g_curpos)
                params.curpos += params.delta

            time.sleep(params.interval)

        # if g_trader is not None:
        #    g_trader.closePosition(instrument, params.curpos - 1)
        #    g_trader.print_trade()

        print 'Close figure to quit'
        t_figure.join()
