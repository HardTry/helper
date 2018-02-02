from libnrlib import *
import tmath, trade, draw_framework4
import matplotlib.pyplot as plt
from matplotlib import rcParams
import sys, gc, threading, time, random, datetime

if __name__ == "__main__":
    gc.disable()
    gc.enable()

    if (len(sys.argv) != 7):
        print 'Usage: python dl4.py <instrument> <r|the end day> <data file path> <split> <index> <level>\n'
        exit(0)

    instrument = sys.argv[1].encode('ascii')
    thedate = sys.argv[2].encode('ascii')
    datapath = sys.argv[3].encode('ascii') + '/' + instrument
    split = int(sys.argv[4])
    tindex = int(sys.argv[5])
    level = int(sys.argv[6])

    params = tmath.Params()
    ppps = NRParams()

    params.run_status = 0
    params.delta = 1
    params.inst = instrument
    params.date = thedate
    params.data_len = 1024
    params.level = level

    m12 = Math12()
    if instrument == 'rb888':
        # ppps.min_data_size = int(1024 * 2048 * 1.0000005)
        ppps.min_data_size = int(1024 * 2048 * 3)
    else:
        ppps.min_data_size = int(1024 * 2048 * 1.5)

    m12.set_param(ppps)
    all_len = m12.get_data_from_file(instrument, datapath, thedate, trade.get_hop(instrument))
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

    amount = all_len - params.minlen - 2048
    pice = int(float(amount)/float(split))
    spos = params.minlen + 2048 + pice * tindex
    epos = spos + pice
    if spos - 1000 < params.minlen + 2048:
        spos = params.minlen + 2048
    else:
        spos = spos - 1000

    if epos >= all_len:
        epos = all_len - 1

    if tindex == split - 1:
        epos = all_len - 1


    print 'from', spos, 'to', epos

    save_pos = [
            2209600, 2210624, 2210688, 2231296, 2267904, 2269072, 2269168, 2269200, 2269448, 2269540, 2269720, 2270400, 2272000, 2272148, 2272178, 2272180, 2272232, 2273560, 2273600, 2291200, 2355200, 2373184, 2375200, 2492608, 2497792, 2517688, 2518752, 2525696, 2631936, 2632000, 2632624, 2705952, 2706216, 2713280, 2713296, 2715500, 2715550, 2720000, 2721600, 2721724, 2722104, 2723536, 2744960, 2745600, 2745800, 2745804, 2745808, 2745812, 2745817, 2745820, 2746036, 2746043, 2746046, 2746140, 2746400, 2747504, 2798656, 2798706, 2798755, 2798799, 2798818, 2799000, 2799496, 2800896, 2807712, 2807876, 2807930, 2808082, 2808183, 2808358, 2808588, 2809200, 2809520, 2903424, 2904576, 2905152, 2905392, 2905424, 2905600, 2939776, 2939900, 2939985, 2940000, 2940800, 2982400, 3059716, 3059800, 3059852, 3060400, 3061600, 3064288, 3064400, 3064680, 3065232, 3133152, 3133744, 3133747, 3133892, 3133912, 3134240

        ]
    for level in [4, 5]:
        for pos in range(spos, epos):
            m12.do_math(pos)
            changed = m12.inflexion_changed(level)
            if changed != 0:
                if 4 == m12.get_resonance_level(pos, level):
                    shot.ClearSnapshot()
                    shot.TakeSnapshot(pos, level, m12)

            if pos in save_pos:
                draw.draw_frame(pos)
                draw.save_frame()
                params.level = level
                save_pos.remove(pos)

    print 'Done.'
