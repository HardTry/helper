import tmath, trade
import sys, gc, random, datetime
from libnrlib import *

if __name__ == "__main__":
    gc.disable()
    gc.enable()

    if (len(sys.argv) != 4 and len(sys.argv) != 5):
        print 'Usage: python find-shape.py <instrument> <the trade day> <data file path> [start pos]\n'
    else:
        params = tmath.Params()

        instrument = sys.argv[1].encode('ascii')
        thedate = sys.argv[2].encode('ascii')
        datapath = sys.argv[3].encode('ascii') + '/' + instrument

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

        if len(sys.argv) != 5:
            spos = params.minlen
        elif sys.argv[4] == 'r':
            random.seed(datetime.datetime.now())
            spos = int(random.random() * (all_len - params.minlen) + params.minlen)
        else:
            dt = sys.argv[4].encode('ascii')
            spos = get_time_pos(pointer, dt)
            if spos < 0:
                print 'error when get time pos'
                exit(-101)
            elif spos < params.minlen:
                print 'less than minlen'
                exit(-102)

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

        # params.run_status = 1
        for i in range(spos, all_len):
            for i in range(0, len(dm)):
                dm[i].do_math(params.curpos)
                dm[i].find_shape()

            # g_trader.do_trade(instrument, g_curpos)
            params.curpos += 1
