from libnrlib import *
import tmath, trade, draw_framework4
import matplotlib.pyplot as plt
from matplotlib import rcParams
import sys, gc, threading, time, random, datetime

if __name__ == "__main__":
    gc.disable()
    gc.enable()

    if (len(sys.argv) != 5):
        print 'Usage: python dl5.py <instrument> <r|the end day> <data file path> <image save path>\n'
        exit(0)

    instrument = sys.argv[1].encode('ascii')
    thedate = sys.argv[2].encode('ascii')
    datapath = sys.argv[3].encode('ascii') + '/' + instrument

    params = tmath.Params()
    ppps = NRParams()

    params.run_status = 0
    params.delta = 1
    params.inst = instrument
    params.date = thedate
    params.data_len = 1024
    params.imgpath = sys.argv[4].encode('ascii')

    m12 = Math12()
    if instrument == 'rb888':
        # ppps.min_data_size = int(1024 * 2048 * 1.0000005)
        ppps.min_data_size = int(1024 * 2048 * 3)
    else:
        ppps.min_data_size = int(1024 * 2048 * 1.5)

    m12.set_param(ppps)
    all_len = m12.get_data_from_file(instrument, datapath, thedate, trade.get_hop(instrument))
    if (all_len <= 0):
        exit(-1001)

    shot = Snapshot()

    trade.get_instrument_code(instrument)

    g_trader = None

    rc_params = {'legend.fontsize': 'small',
                 'axes.labelsize': 'small',
                 'axes.titlesize': 'small',
                 'xtick.labelsize': 'small',
                 'ytick.labelsize': 'small'}

    for key, value in sorted(rc_params.iteritems()):
        rcParams[key] = value

    draw = draw_framework4.DrawFramework4(m12, shot, g_trader, params, 0)

    spos = params.minlen + 2048
    epos = all_len - 1

    print 'run from', spos, 'to', epos

    for pos in range(spos, epos):
        m12.do_math(pos)
        changed = m12.high_skewer_changed()
        if changed != 0:
            shot.ClearSnapshot()
            shot.TakeSnapshot(pos, 10, m12)
            # print "take shot", pos,
            draw.draw_frame(pos)
            # print
            draw.save_frame()

    print 'Done.'
