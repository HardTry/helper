import gc
from libnrlib import *

import matplotlib.pyplot as plt
from matplotlib import rcParams

import tmath
import trade

minlen = 1024000
min_data_size = int(minlen * 1.0000005)
# min_data_size = int(minlen * 3.2)
predict_len = 128

global g_curpos, g_run_status, g_all_len, g_delta


def get_data_from_file(instrument, datapath, thedate):
    price = []
    ftime = []

    ret = load_10s_ts_from_date_v1(instrument, datapath, thedate, min_data_size, price, ftime)
    # ret = load_10s_ts_from_date_v2(instrument, datapath, thedate, min_data_size, my_hop, price, ftime)
    if (ret != 0):
        print "error code " + str(ret)

    all_len = len(price)
    allx = list(range(0, all_len + predict_len))
    return ret, price, all_len, allx, thedate


def print_ve(ve):
    for e in ve:
        print e.pos, ", ",
    print


class Artist:
    def __init__(self, dm, ax, name):
        self.dm = dm
        self.name = name
        self.ax = ax

        self.ax.set_xlim([0, dm.data_len + dm.predict_len])
        self.ax.set_ylim([min(dm.price[0: dm.data_len]),
                          max(dm.price[0: dm.data_len])])

        # self.lPassed, = self.ax.plot([], [], lw=1, color='black')
        self.lCurrent, = self.ax.plot([], [], lw=1, color='blue')
        self.lFuture, = self.ax.plot([], [], lw=1, color='green')
        # self.lma_hi, = self.ax.plot([], [], lw=1, color='yellow')
        # self.lma_lo, = self.ax.plot([], [], lw=1, color='pink')
        # self.lma_mid, = self.ax.plot([], [], lw=1, color='black')
        self.lp_hi, = self.ax.plot([], [], lw=1, color='red')
        # self.lExtrem, = self.ax.plot([], [], 'rx', lw=1)  # lw=2, color='black', marker='o', markeredgecolor='b')
        # self.lExtremAppx, = self.ax.plot([], [], 'yo', lw=1)  # lw=2, color='black', marker='o', markeredgecolor='b')
        self.lNow, = self.ax.plot([], [], lw=1, color='green')
        self.lmax, = self.ax.plot([], [], lw=1, color='black')
        self.lmin, = self.ax.plot([], [], lw=1, color='black')

        self.down_int = 1

        self.lines = [self.lCurrent, self.lFuture, self.lp_hi, self.lNow, self.lmax, self.lmin]

    def init_animation(self):
        for line in self.lines:
            line.set_data([], [])
        return self.lines

    def set_dm_int(self, down_int):
        self.down_int = down_int
        self.ax.set_xlim([0, self.dm.data_len + self.dm.predict_len])
        self.ax.set_ylim([min(self.dm.hp[0: self.dm.data_len]),
                          max(self.dm.hp[0: self.dm.data_len])])

    def update_limite(self, xlim, ylim, cp):
        delta = cp + self.dm.predict_len - xlim[1]
        if delta > 0:
            xlim[0] = cp - self.dm.data_len
            xlim[1] = cp + self.dm.predict_len
        self.ax.set_xlim(xlim)

        self.ax.set_ylim([min(self.dm.hp[int(xlim[0]): int(xlim[1])]), \
                          max(self.dm.hp[int(xlim[0]): int(xlim[1])])])

    def update_lines(self, xlim, cp, pp, its_review, show_future):
        self.lCurrent.set_data(self.dm.allx[cp - self.dm.data_len: cp],
                               self.dm.hp[cp - self.dm.data_len: cp])
        self.update_extreme_appx(cp)
        self.update_extreme_lo(cp)

        # self.lma_lo.set_data(self.dm.allx[cp - self.dm.data_len: cp], self.dm.ma_lo)
        # self.lma_mid.set_data(self.dm.allx[self.dm.first_ext_pos - len(self.dm.appx_hi): \
        #                       self.dm.first_ext_pos], \
        #                       self.dm.appx_hi)
        # self.lma_hi.set_data(self.dm.allx[cp - self.dm.data_len: cp], self.dm.ma_hi)

        if show_future:
            dlen = len(self.dm.hp[cp: cp + self.dm.predict_len])
            self.lFuture.set_data(self.dm.allx[cp: cp + dlen], \
                                  self.dm.hp[cp: cp + self.dm.predict_len])
        else:
            self.lFuture.set_data([], [])

        # print self.name, self.dm.first_ext_pos, cp, len(self.dm.hp)
        self.lNow.set_data([self.dm.first_ext_pos, cp - 1], \
                           [self.dm.hp[self.dm.first_ext_pos], self.dm.hp[cp - 1]])

        # print 4, len(self.dm.allx[self.dm.ap_hi_pos: self.dm.ap_hi_pos + self.dm.predict_len]), len(self.dm.ap_hi)
        l = len(self.dm.allx[self.dm.ap_hi_pos: self.dm.ap_hi_pos + self.dm.predict_len])
        self.lp_hi.set_data(self.dm.allx[self.dm.ap_hi_pos: self.dm.ap_hi_pos + self.dm.predict_len], \
                            self.dm.ap_hi[0: l])

        self.lmax.set_data(self.dm.dl.max_x, self.dm.dl.max_y)
        self.lmin.set_data(self.dm.dl.min_x, self.dm.dl.min_y)

    def update_extreme_lo(self, cp):
        # print self.name, cp, len(self.dm.ext_pos)
        # self.lExtrem.set_data(self.dm.ext_pos, self.dm.ext_val)
        pass

    def update_extreme_appx(self, cp):
        # self.lExtremAppx.set_data(self.dm.ext_appx_pos, self.dm.ext_appx_val)
        pass

    def animate(self, cur_pos, pass_pos, its_review, show_future):
        cp = cur_pos / self.down_int
        pp = pass_pos / self.down_int
        #
        # if (cp + self.dm.predict_len > self.dm.all_len):
        #     return
        #
        xlim = list(self.ax.get_xlim())
        ylim = list(self.ax.get_ylim())
        #
        self.update_limite(xlim, ylim, cp)
        #
        # self.dm.do_math(cp)

        self.update_lines(xlim, cp, pp, its_review, show_future)

        return self.lines


class SubplotAnimation():
    def __init__(self, dm):
        self.fig = plt.figure()
        self.ax = [self.fig.add_subplot(2, 2, 1),
                   self.fig.add_subplot(2, 2, 2),
                   self.fig.add_subplot(2, 2, 3),
                   self.fig.add_subplot(2, 2, 4)]
        self.fig.tight_layout()
        self.dm = dm

        self.art = []
        for i in range(0, len(dm)):
            self.art.append(Artist(dm[i], self.ax[i], "art" + str(i)))
            self.art[i].set_dm_int(dm[i].down_int)

        self.anim_running = True
        self.anim_interval = 300

        self.cur_pos = dm[0].data_len
        self.max_curpos = self.cur_pos
        self.pass_pos = 0
        self.show_future = True

    def draw_frame(self, cur_pos):
        global instrument, thedate
        self.cur_pos = cur_pos

        if (self.cur_pos > self.max_curpos):
            self.its_review = False

        for i in range(0, 4):
            self.art[i].animate(self.cur_pos, self.pass_pos, self.its_review, self.show_future)

        self.max_curpos = max(self.cur_pos, self.max_curpos)
        self.pass_pos = self.cur_pos - self.dm[0].data_len
        self.fig.suptitle(instrument + '-' + thedate + '-' + str(cur_pos))
        self.fig.canvas.draw()

    def new_frame_seq(self):
        return iter(range(self.dm[0].all_len))

    def init_draw(self):
        for i in range(0, 4):
            self.art[i].init_animation()


if __name__ == "__main__":
    global instrument, thedate

    gc.disable()
    gc.enable()

    # price, all_ask, all_bid, all_len, allx, the_date = get_data()
    instrument = 'zn888'
    thedate = '20171013'
    datapath = '/data/sean/10s_candle_bindata/' + instrument

    params = tmath.Params()
    params.run_status = 0
    params.delta = 1
    params.inst = instrument
    params.date = thedate
    params.data_len = 1024
    params.curpos = 1024000

    ret, price, g_all_len, allx, the_date = get_data_from_file(instrument, datapath, thedate)

    params.all_len = g_all_len

    # plt.plot(list(range(0, all_len)), price)
    # plt.show()
    if (ret == 0) and (g_all_len >= min_data_size):
        dm = []
        power = 1
        hop = trade.get_hop(instrument)
        for i in range(0, 4):
            dm.append(tmath.DataMath(price, g_all_len, allx, the_date, hop, params))
            dm[i].down_sample(2 * power)
            power *= 10

        # opq = str(raw_input("enter something to draw: (q = quit)"))
        # if (opq == 'q'):
        #    exit(0)

        plt.ion()

        rc_params = {'legend.fontsize': 'small',
                     'figure.figsize': (9, 5),
                     'axes.labelsize': 'small',
                     'axes.titlesize': 'small',
                     'xtick.labelsize': 'small',
                     'ytick.labelsize': 'small'}

        for key, value in sorted(rc_params.iteritems()):
            rcParams[key] = value

        ani = SubplotAnimation(dm)
        ani.init_draw()

        spos = [1024000]
        for g_curpos in spos:
            print g_curpos
            for i in range(0, 4):
                dm[i].do_math(g_curpos)
            ani.draw_frame(g_curpos)
            plt.savefig('/home/sean/tmp/trade/' + instrument + '-' + thedate + '-' + str(g_curpos) + '.png')
