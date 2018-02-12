from libnrlib import *
import tmath, trade, animation7
import matplotlib.pyplot as plt
from matplotlib import rcParams
import sys, gc, threading, time, random, datetime


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
    # stop_pos = read_pos_from_file(inst_code)
    stop_pos = [
        2099273, 2099356, 2099428, 2099500, 2099726, 2099799, 2099845, 2099906, 2099920, 2100000, 2100004, 2100156, 2100158, 2100250, 2100303, 2100408, 2100532, 2100605, 2100661, 2100766, 2100872, 2100909, 2100928, 2101000, 2101214, 2101300, 2101501, 2101606, 2101758, 2101898, 2101899, 2102050, 2102331, 2102352, 2102462, 2102545, 2102719, 2102800, 2102828, 2102950, 2102953, 2103050, 2103124, 2103181, 2103205, 2103303, 2103355, 2103468, 2103500, 2103620, 2103825, 2103881, 2104058, 2104124, 2104306, 2104400, 2104407, 2104450, 2104525, 2104648, 2104781, 2104860, 2104910, 2105004, 2105319, 2105400, 2105590, 2105653, 2105866, 2105978, 2106088, 2106134, 2106248, 2106350, 2106455, 2106539, 2106592, 2106641, 2106764, 2106900, 2106908, 2107062, 2107257, 2107294, 2107450, 2107579, 2107659, 2107750, 2107756, 2107850, 2108078, 2108125, 2108147, 2108320, 2108620, 2108770, 2108832, 2108974, 2109055, 2109160
    ]

    t_figure = FigureThread(m12, shot, params, save_pos, stop_pos, g_trader)
    t_figure.start()

    # params.curpos += 1
    params.run_status = 0

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
