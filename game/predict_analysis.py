from libnrlib import *
import matplotlib.pyplot as plt
from matplotlib import rcParams
import gc, sys, re
import tmath
import artist
import time
import threading

minlen = 1024000
# min_data_size = int(minlen * 1.0000005)
min_data_size = int(minlen * 3.2)
predict_len = 128

def get_hop(inst):
    hop = dict(
        {'CF': 5, 'FG': 1, 'MA': 1, 'OI': 2, 'RM': 1, 'SR': 1, 'TA': 2, 'ZC': 2, 'a': 1, 'ag': 1, 'al': 5, 'au': 5,
         'bu': 2,
         'c': 1, 'cu': 10, 'i': 5, 'j': 5, 'jd': 1, 'jm': 5, 'l': 5, 'm': 1, 'ni': 10, 'p': 2, 'pb': 5, 'pp': 1,
         'rb': 1,
         'ru': 5, 'v': 5, 'y': 2, 'zn': 5})

    match = re.match(r"([a-z]+)([0-9]+)", instrument, re.I)
    if match:
        items = match.groups()
        code = items[0]
        my_hop = hop[code]
        return my_hop
    return 0


def draw_figure(art, fig, cur_pos):
    art.update_all(cur_pos, False)
    fig.canvas.draw()

class InputThread(threading.Thread):
    def __init__(self):
        super(InputThread, self).__init__()

    def run(self):
        global running, delta, g_curpos, down_int
        while True:
            s = str(raw_input('enter command: '))
            if s == 'q':
                running = False
                break
            elif s == '=':
                delta += down_int
            elif s == '-':
                if delta - down_int >= 0:
                    delta -= down_int
            elif s == 'o':
                print g_curpos


if __name__ == "__main__":
    global running, delta, down_int, g_curpos

    gc.disable()
    gc.enable()

    thedate = '20171013'
    instrument = sys.argv[1].encode('ascii')
    datapath = '/data/sean/10s_candle_bindata' + '/' + instrument
    down_int = int(sys.argv[2])

    hop = get_hop(instrument)

    ret, price, g_all_len, allx, the_date = tmath.get_data_from_file(instrument, datapath, thedate, min_data_size, predict_len)

    dm = tmath.DataMath(price, g_all_len, allx, the_date, hop)
    dm.down_sample(2 * down_int)

    plt.ion()
    rc_params = {'legend.fontsize': 'small',
                 'figure.figsize': (16, 9),
                 'axes.labelsize': 'small',
                 'axes.titlesize': 'small',
                 'xtick.labelsize': 'small',
                 'ytick.labelsize': 'small'}

    for key, value in sorted(rc_params.iteritems()):
        rcParams[key] = value

    fig = plt.figure(0)
    ax = fig.add_subplot(1, 1, 1)
    fig.tight_layout()

    art = artist.Artist10l(dm, ax)
    art.set_dm_int(dm.down_int)
    art.init_animation()

    running = True
    delta = down_int
    g_curpos = minlen - 1

    t = InputThread()
    t.start()
    while running and g_curpos < min_data_size:
        dm.do_math(g_curpos)
        if dm.qpl.qsize() >= 10:
            draw_figure(art, fig, g_curpos)
        g_curpos += delta
        time.sleep(0.0001)
    t.join()