from libnrlib import *
import tmath, trade, draw_framework
import matplotlib.pyplot as plt
from matplotlib import rcParams
import sys, gc, threading, time, random, datetime

if __name__ == "__main__":
    gc.disable()
    gc.enable()

    if (len(sys.argv) != 5):
        print 'Usage: python cppmath.py <instrument> <r|the end day> <data file path> <a|b>\n'
        exit(0)

    instrument = sys.argv[1].encode('ascii')
    thedate = sys.argv[2].encode('ascii')
    datapath = sys.argv[3].encode('ascii') + '/' + instrument
    func = sys.argv[4].encode('ascii')

    params = tmath.Params()
    ppps = NRParams()

    params.run_status = 0
    params.delta = 1
    params.inst = instrument
    params.date = thedate
    params.data_len = 1024

    m12 = Math12()
    # ppps.min_data_size = int(1024 * 2048 * 1.0000005)
    ppps.min_data_size = int(1024 * 2048 * 3)
    # ppps.min_data_size = int(1024 * 2048 * 1.5)

    m12.set_param(ppps)
    all_len = m12.get_data_from_file(instrument, datapath, thedate, trade.get_hop(instrument))

    trade.get_instrument_code(instrument)

    save_pos = [2100960, 2101439, 2102016, 2102847, 2108864, 2109567, 2130496, 2131263, 2132832, 2134079, 2134912, 2136511, 2139232, 2139455, 2141760, 2143935, 2145664, 2145727, 2145920]


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

    draw = draw_framework.DrawFramework(m12, g_trader, params, 0)

    if func == 'a':
        for pos in save_pos:
            m12.ph_clear()
            m12.do_math(pos)
            # g_trader.do_trade(instrument, g_curpos)
            draw.draw_frame(pos)
            draw.save_frame()
    elif func == 'b':
        if save_pos[0] - 1000 < params.minlen + 2048:
            spos = params.minlen + 2048
        else:
            spos = save_pos[0] - 1000
        epos = save_pos[-1] + 1

        for pos in range(spos, epos):
            m12.do_math(pos)
            if pos in save_pos:
                draw.draw_frame(pos)
                draw.save_frame()


    print 'Press X and Close figure to quit'
