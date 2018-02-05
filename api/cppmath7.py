from libnrlib import *
import tmath, trade, animation7
import matplotlib.pyplot as plt
from matplotlib import rcParams
import sys, gc, threading, time, random, datetime


def read_pos_from_file(inst):
    s = False
    str_pos = []
    filepath = './logs/' + inst + '.log'
    with open(filepath) as f:
        for line in f:
            if s:
                str_pos = line.split(',')
                del str_pos[-1]
                s = False
            if line[0] == '[':
                s = True

    pos = []
    for sp in str_pos:
        pos.append(int(sp))

    return pos

def write_pos_to_file(inst, save_pos):
    filepath = './logs/save_' + inst + '.log'
    with open(filepath, 'a+') as f:
        for sp in save_pos:
            f.write(str(sp[0]) + ', ')


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



if __name__ == "__main__":
    gc.disable()
    gc.enable()

    if (len(sys.argv) < 4 or len(sys.argv) > 6):
        print 'Usage: python cppmath.py <instrument> <r|the end day> <data file path> [start pos] [end pos]\n'
        exit(0)

    instrument = sys.argv[1].encode('ascii')
    thedate = sys.argv[2].encode('ascii')
    datapath = sys.argv[3].encode('ascii') + '/' + instrument
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
    #     # ppps.min_data_size = int(1024 * 2048 * 1.0000005)
        ppps.min_data_size = int(1024 * 2048 * 3)
    else:
        ppps.min_data_size = int(1024 * 2048 * 1.5)
    # ppps.min_data_size = int(1024 * 2048 *1.005)


    m12.set_param(ppps)
    all_len = m12.get_data_from_file(instrument, datapath, thedate, trade.get_hop(instrument))
    shot = Snapshot()

    trade.get_instrument_code(instrument)

    epos = 0
    spos = 0

    if (len(sys.argv) == 4):
        epos = all_len - 1
        spos = params.minlen + 2048
    elif (len(sys.argv) > 4):
        if sys.argv[4] == 'r':
            random.seed(datetime.datetime.now())
            spos = int(random.random() * (all_len - params.minlen) + params.minlen)
        else:
            spos = int(sys.argv[4])
            if spos < params.minlen + 2048:
                spos = params.minlen + 2048

        if (len(sys.argv) == 6):
            epos = int(sys.argv[5])
        else:
            epos = all_len - 1

    print 'all data', all_len, 'start from', spos, 'to ', epos
    params.curpos = spos

    g_trader = None


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

    m12.do_math(params.curpos)

    save_pos = []
    inst_code = trade.get_instrument_code(instrument)
    stop_pos = read_pos_from_file(inst_code)
    # stop_pos = [2100752]

    t_figure = FigureThread(m12, shot, params, save_pos, stop_pos, g_trader)
    t_figure.start()

    # params.curpos += 1
    params.run_status = 0
    key_level = [4, 5]

    while params.run_status >= 0 and params.curpos <= epos:
        if params.run_status == 1:
            m12.do_math(params.curpos)
            # if params.curpos in save_pos:
            #    shot.ClearSnapshot()
            #    shot.TakeSnapshot(params.curpos, 0, m12)
            #    # print "take shot", params.curpos

            if params.curpos in stop_pos:
               print params.curpos,
               s = str(raw_input("Enter to continue:"))

            params.curpos += params.delta

        time.sleep(params.interval)
        # if (len(save_pos) == 0):
        #    break

    # if g_trader is not None:
    #    g_trader.closePosition(instrument, params.curpos - 1)
    #    g_trader.print_trade()

    print 'Press X and Close figure to quit'
    t_figure.join()
    write_pos_to_file(inst_code, save_pos)

    print 'save_pos = ['
    for sp in save_pos:
        print sp, ','
    print ']'

