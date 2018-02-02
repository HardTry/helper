from libnrlib import *
import tmath, trade, animation4
import matplotlib.pyplot as plt
from matplotlib import rcParams
import sys, gc, threading, time, random, datetime

class FigureThread(threading.Thread):
    def __init__(self, m12, shot, params, save_pos, trade = None):
        super(FigureThread, self).__init__()
        self.m12 = m12
        self.shot = shot
        self.trade = trade
        self.params = params
        self.save_pos = save_pos

    def run(self):
        ani_lines1 = animation4.SubplotAnimation4(self.m12, self.shot, self.trade, self.params, 0, self.save_pos)

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
    t_figure = FigureThread(m12, shot, params, save_pos, g_trader)
    t_figure.start()

    # params.curpos += 1
    params.run_status = 0
    key_level = [4, 5]
    stop_pos = [

2139680,
2150400,
2163200,
2231296,
2231296,
2268320,
2276352,
2279680,
2294528,
2295296,
2295296,
2298272,
2304000,
2304000,
2321600,
2340352,
2342400,
2342400,
2350560,
2355200,
2355200,
2388800,
2393600,
2439168,
2439168,
2444800,
2457600,
2462208,
2470400,
2489344,
2556928,
2556928,
2564800,
2593792,
2593792,
2608160,
2621696,
2640896,
2640896,
2668352,
2678784,
2721280,
2721280,
2724256,
2726400,
2739200,
2755584,
2755584,
2770848,
2799872,
2799872,
2844768,
2852096,
2862336,
2862336,
2893632,
2894080,
2978816,
2978816,
2984032,
3012352,
3012352,
3019680,
3021056,
3028224,
3030016,
3057152,
3081216,
3081216,
3126304,
3139328,
3148710
    ]

    while params.run_status >= 0 and params.curpos <= epos:
        if params.run_status == 1:
            m12.do_math(params.curpos)
            for level in key_level:
                changed = m12.inflexion_changed(level)
                if changed == 1:
                    if 4 == m12.get_resonance_level(params.curpos, level):
                        shot.ClearSnapshot()
                        shot.TakeSnapshot(params.curpos, level, m12)
                        # print "take shot", pos

            # if params.curpos >= stop_pos[-1]:
            #    break

            if params.curpos in stop_pos:
                a = str(raw_input(str(params.curpos) + ", enter to continue: "))

            params.curpos += params.delta

        time.sleep(params.interval)
        # if (len(save_pos) == 0):
        #    break

    # if g_trader is not None:
    #    g_trader.closePosition(instrument, params.curpos - 1)
    #    g_trader.print_trade()

    print 'Press X and Close figure to quit'
    t_figure.join()
