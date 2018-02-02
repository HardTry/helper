import tmath, trade
import sys, gc, random, datetime


if __name__ == "__main__":

    gc.disable()
    gc.enable()

    if (len(sys.argv) != 5 and len(sys.argv) != 6):
        print 'Usage: python tg.py <instrument> <r|the trade day> <data file path> <trader name> [start pos]\n' \
              '       1. r means you want a random day\n' \
              '       2  format of trade day is YYYYMMDD\n' \
              '       3. the data file path tell game where is the store of history data\n' \
              '       4. For example:\n' \
              '          get random trade-day data\n' \
              '            python tg.py rb888 r /data/sean/10s_candle_bindata s 1024000\n' \
              '          get one day data\n' \
              '            python tg.py rb888 20150601 /data/sean/10s_candle_bindata p 0\n\n'
    else:
        params = tmath.Params()

        instrument = sys.argv[1].encode('ascii')
        thedate = sys.argv[2].encode('ascii')
        datapath = sys.argv[3].encode('ascii') + '/' + instrument
        trade_name = sys.argv[4].encode('ascii')

        trade.get_instrument_code(instrument)

        ret, price, all_len, allx, the_date = \
            tmath.get_data_from_file(instrument, datapath, thedate, \
                                     params.min_data_size, params.predict_len)

        if (ret != 0) or (all_len < params.min_data_size):
            exit(ret)

        if len(sys.argv) != 6:
            spos = params.minlen
        elif sys.argv[5] == 'r':
            random.seed(datetime.datetime.now())
            spos = int(random.random() * (all_len - params.minlen) + params.minlen)
        else:
            spos = int(sys.argv[5])
        print 'start from ', spos

        params.run_status = 0
        params.curpos = spos
        params.delta = 1
        params.inst = instrument
        params.date = thedate

        dm = []
        power = 1
        hop = trade.get_hop(instrument)
        for i in range(0, 4):
            dm.append(tmath.DataMath(price, all_len, allx, the_date, hop, params))
            dm[i].down_sample(2 * power)
            power *= 10

        g_trader = trade.get_trader(trade_name)
        g_trader.set_dm(dm, params)

        while params.curpos < all_len:
            for i in range(0, 4):
                dm[i].do_math(params.curpos)
            g_trader.do_trade(instrument, params.curpos)
            params.curpos += 1

        if g_trader is not None:
            g_trader.closePosition(instrument, params.curpos - 1)
            g_trader.print_trade()