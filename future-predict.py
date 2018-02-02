from mongoengine import *
import random
import libnrlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import gc
from scipy import stats


class Order:
    def __init__(self):
        self.direct = ''
        self.pos_ = 0
        self.price = 0
        self.posrev = 0
        self.rev = 0

    def __init__(self, direct, pos, price):
        self.direct = direct
        self.pos_ = pos
        self.price = price
        self.posrev = 0  # current revenue
        self.rev = 0  # revenue


class Trade:
    order = []
    allrev = 0

    def __init__(self, dm):
        self.dm = dm

    def openLong(self, cur_pos):
        if (0 == len(self.order) % 2):
            print 'Long ', cur_pos, self.dm.all_ask[cur_pos]
            self.order.append(Order('a', cur_pos, self.dm.all_ask[cur_pos]))
            return True
        else:
            return False

    def openShort(self, cur_pos):
        if (0 == len(self.order) % 2):
            print 'Short ', cur_pos, self.dm.all_ask[cur_pos]
            self.order.append(Order('b', cur_pos, self.dm.all_bid[cur_pos]))
            return True
        else:
            return False

    def closePosition(self, cur_pos):
        if (1 == len(self.order) % 2):
            c = Order('c', cur_pos, self.dm.all_data[cur_pos])
            if self.order[-1].direct == 'a':
                c.posrev = (c.price - self.order[-1].price) * 10
                c.rev = (c.price - self.order[-1].price) * 10 \
                        - (c.price + self.order[-1].price) * 0.0015
            else:
                c.posrev = (self.order[-1].price - c.price) * 10
                c.rev = (self.order[-1].price - c.price) * 10 \
                        - (c.price + self.order[-1].price) * 0.0015
            self.order.append(c)
            self.allrev += c.rev
            print 'Close', cur_pos, self.dm.all_data[cur_pos], c.posrev, c.rev, self.allrev
            return True
        else:
            return False



def get_10s_data_from_file(inst, day, path, minsize):
    price = []
    ftime = []
    datapath = path + '/' + inst
    ret = libnrlib.load_10s_ts_from_date(inst, datapath, day, minsize, price, ftime)
    if (ret != 0):
        print "error code ", ret

    all_len = len(price)
    return ret, all_len, price, ftime


def print_ve(ve):
    for e in ve:
        print e.pos, ", ",
    print


class DataLines:
    def __init__(self):
        self.max_x = []
        self.max_y = []
        self.min_x = []
        self.min_y = []

    def set_data(self, ve, max_x, min_x, cp, prdlen):
        self.max_x = []
        self.max_y = []
        self.min_x = []
        self.min_y = []

        if (len(max_x) > 1):
            for x in max_x:
                self.max_x.append(ve[x].pos)
                self.max_y.append(ve[x].val)
            slope, intercept, r_value, p_value, std_err = stats.linregress(self.max_x, self.max_y)
            # print "MAX: ", slope, intercept, r_value, p_value, std_err
            self.max_y = []
            self.max_x.append(cp + prdlen)
            for x in self.max_x:
               self.max_y.append(intercept + slope * x)


        if (len(min_x) > 1):
            for x in min_x:
                self.min_x.append(ve[x].pos)
                self.min_y.append(ve[x].val)
            slope, intercept, r_value, p_value, std_err = stats.linregress(self.min_x, self.min_y)
            # print "MIN: ", slope, intercept, r_value, p_value, std_err
            self.min_y = []
            self.min_x.append(cp + prdlen)
            for x in self.min_x:
               self.min_y.append(intercept + slope * x)



class DataMath:
    def __init__(self, price, ftime, all_len, the_date):
        self.all_data = price
        self.ftime = ftime
        self.all_len = all_len
        self.the_date = the_date

        self.down_int = 1
        self.data_len = 1024
        self.predict_len = 128
        self.allx = list(range(0, all_len + self.predict_len))

        self.lvl_hi = 7
        self.lvl_ma_lo = 10
        self.lvl_ma_mid = 30
        self.lvl_ma_hi = 60

        self.predict = libnrlib.Predict(self.data_len, self.predict_len)
        self.wt = libnrlib.WaveletFilter(1, self.data_len, self.lvl_hi)
        self.ma = libnrlib.MaFilter(self.lvl_ma_lo, self.data_len);

        self.appx_hi_len = self.data_len
        self.appx_hi = []
        self.ap_hi = []
        self.ap_hi_pos = 0

        self.ma_lo = []
        self.ma_mid = []
        self.ma_hi = []

        self.ext_pos = []
        self.ext_val = []
        self.first_ext_pos = 0
        self.ve = libnrlib.VectorExtreme()

        self.veAppx = libnrlib.VectorExtreme()
        self.ext_appx_pos = []
        self.ext_appx_val = []

        self.dl = DataLines()

    def down_sample(self, down_int):
        self.down_int = down_int / 2
        self.all_data = libnrlib.sample_max_min(self.all_data, down_int)
        self.all_len = len(self.all_data)
        self.allx = list(range(0, self.all_len + self.predict_len))

    def do_math(self, cp):
        # print cp, self.all_len
        self.ma.set(self.lvl_ma_lo, self.data_len)
        self.ma.setdata(self.all_data[cp - self.data_len: cp])
        self.ma_lo = self.ma.filter()

        self.ma.set(self.lvl_ma_mid, self.data_len)
        self.ma_mid = self.ma.filter()

        self.ma.set(self.lvl_ma_hi, self.data_len)
        self.ma_hi = self.ma.filter()

        self.ext_val = []
        self.ext_pos = []
        self.ve = libnrlib.get_sample_extreme(self.all_data[cp - self.data_len: cp],
                                              50, cp - self.data_len, \
                                              self.ext_pos, self.ext_val)
        self.first_ext_pos = self.ext_pos[-1]

        pos = 0
        if (self.first_ext_pos - self.data_len < 0):
            self.appx_hi_len = self.first_ext_pos
        else:
            self.appx_hi_len = self.data_len
            pos = self.first_ext_pos - self.data_len

        self.wt.set(1, self.appx_hi_len, self.lvl_hi)
        self.wt.setdata(self.all_data[pos: self.first_ext_pos])
        self.appx_hi = self.wt.filter()

        self.ap_hi_pos = self.first_ext_pos
        self.predict.setdata(self.appx_hi)
        self.ap_hi = self.predict.predict()

        self.ext_appx_pos = []
        self.ext_appx_val = []

        self.veAppx = libnrlib.get_appx_org_extreme(
                                           self.appx_hi + self.ap_hi, \
                                           self.ve, \
                                           cp - self.data_len, \
                                           self.ext_appx_pos, \
                                           self.ext_appx_val)
        # print self.ext_appx_pos

        lastmax = []
        lastmin = []
        # print "math ", self.down_int, " ve ",
        # print_ve(self.ve)
        # print "math ", self.down_int, " veappx ",
        # print_ve(self.veAppx)
        libnrlib.get_last_slice(self.ve, self.veAppx, lastmax, lastmin)
        # print lastmax, lastmin
        self.dl.set_data(self.ve, lastmax, lastmin, cp, self.predict_len)




class Artist:
    def __init__(self, dm, ax, name):
        self.dm = dm
        self.name = name
        self.ax = ax

        self.ax.set_xlim([0, dm.data_len + dm.predict_len])
        self.ax.set_ylim([min(dm.all_data[0: dm.data_len]),
                          max(dm.all_data[0: dm.data_len])])

        # self.lPassed, = self.ax.plot([], [], lw=1, color='black')
        self.lCurrent, = self.ax.plot([], [], lw=1, color='blue')
        self.lFuture, = self.ax.plot([], [], lw=1, color='green')
        # self.lma_hi, = self.ax.plot([], [], lw=1, color='yellow')
        # self.lma_lo, = self.ax.plot([], [], lw=1, color='pink')
        # self.lma_mid, = self.ax.plot([], [], lw=1, color='black')
        self.lp_hi, = self.ax.plot([], [], lw=1, color='red')
        self.lExtrem, = self.ax.plot([], [], 'rx', lw=1)  # lw=2, color='black', marker='o', markeredgecolor='b')
        self.lExtremAppx, = self.ax.plot([], [], 'yo', lw=1)  # lw=2, color='black', marker='o', markeredgecolor='b')
        self.lNow, = self.ax.plot([], [], lw=1, color='green')
        self.lmax, = self.ax.plot([], [], lw = 1, color = 'black')
        self.lmin, = self.ax.plot([], [], lw = 1, color = 'black')

        self.down_int = 1

        self.lines = [self.lCurrent, self.lFuture, self.lp_hi, self.lExtrem, self.lExtremAppx, self.lNow, self.lmax, self.lmin]


    def init_animation(self):
        for line in self.lines:
            line.set_data([], [])
        return self.lines

    def set_dm_int(self, down_int):
        self.down_int = down_int
        self.ax.set_xlim([0, self.dm.data_len + self.dm.predict_len])
        self.ax.set_ylim([min(self.dm.all_data[0: self.dm.data_len]),
                          max(self.dm.all_data[0: self.dm.data_len])])

    def update_limite(self, xlim, ylim, cp):
        delta = cp + self.dm.predict_len - xlim[1]
        if delta > 0:
            xlim[0] = cp - self.dm.data_len
            xlim[1] = cp + self.dm.predict_len
        self.ax.set_xlim(xlim)

        ymax = max(self.dm.all_data[int(xlim[0]): cp])
        ymin = min(self.dm.all_data[int(xlim[0]): cp])
        if (ymin < ylim[0]) or (ymin > ylim[0] + 10):
            ylim[0] = ymin - 5
        if (ymax > ylim[1]) or (ymax < ylim[1] - 10):
            ylim[1] = ymax + 5
        self.ax.set_ylim(ylim)

    def update_lines(self, xlim, cp, pp, its_review, show_future):
        self.lCurrent.set_data(self.dm.allx[cp - self.dm.data_len: cp],
                               self.dm.all_data[cp - self.dm.data_len: cp])
        self.update_extreme_appx(cp)
        self.update_extreme_lo(cp)

        # self.lma_lo.set_data(self.dm.allx[cp - self.dm.data_len: cp], self.dm.ma_lo)
        # self.lma_mid.set_data(self.dm.allx[self.dm.first_ext_pos - len(self.dm.appx_hi): \
        #                       self.dm.first_ext_pos], \
        #                       self.dm.appx_hi)
        # self.lma_hi.set_data(self.dm.allx[cp - self.dm.data_len: cp], self.dm.ma_hi)

        if show_future:
            self.lFuture.set_data(self.dm.allx[cp: cp + self.dm.predict_len], \
                                  self.dm.all_data[cp: cp + self.dm.predict_len])
        else:
            self.lFuture.set_data([], [])

        self.lNow.set_data([self.dm.first_ext_pos, cp], \
                           [self.dm.all_data[self.dm.first_ext_pos], self.dm.all_data[cp]])

        # print len(self.dm.allx[self.dm.ap_hi_pos: self.dm.ap_hi_pos + self.dm.predict_len]), len(self.dm.ap_hi)
        self.lp_hi.set_data(self.dm.allx[self.dm.ap_hi_pos: self.dm.ap_hi_pos + self.dm.predict_len], \
                            self.dm.ap_hi)

        self.lmax.set_data(self.dm.dl.max_x, self.dm.dl.max_y)
        self.lmin.set_data(self.dm.dl.min_x, self.dm.dl.min_y)


    def update_extreme_lo(self, cp):
        # print self.name, cp, len(self.dm.ext_pos)
        self.lExtrem.set_data(self.dm.ext_pos, self.dm.ext_val)

    def update_extreme_appx(self, cp):
        self.lExtremAppx.set_data(self.dm.ext_appx_pos, self.dm.ext_appx_val)

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
        self.dm.do_math(cp)

        self.update_lines(xlim, cp, pp, its_review, show_future)

        return tuple(self.lines)


class SubplotAnimation:
    def __init__(self, dm1, dm2, dm3):
        self.fig = plt.figure()
        self.fig.set_size_inches(12, 9);

        # self.fig.set_dpi(720);
        self.ax1 = self.fig.add_subplot(2, 2, 1)
        self.ax2 = self.fig.add_subplot(2, 2, 2)
        self.ax3 = self.fig.add_subplot(2, 2, 3)
        self.ax4 = self.fig.add_subplot(2, 2, 4)
        self.dm1 = dm1
        self.dm2 = dm2
        self.dm3 = dm3

        self.trade = Trade(dm1)

        self.art1 = Artist(dm1, self.ax1, "art1")

        self.art2 = Artist(dm2, self.ax2, "art2")
        self.art2.set_dm_int(dm2.down_int)

        self.art3 = Artist(dm3, self.ax3, "art3")
        self.art3.set_dm_int(dm3.down_int)

        self.anim_running = True
        self.anim_interval = 500

        self.cur_pos = dm1.data_len
        self.max_curpos = self.cur_pos
        self.pass_pos = 0
        self.show_future = False
        self.its_review = False

        self.fig.canvas.mpl_connect('key_press_event', self.press)
        self.fig.canvas.mpl_connect('close_event', self.handle_close)
        self.fig.canvas.mpl_connect('resize_event', self.on_resize)
        # self.fig.canvas.mpl_connect('button_press_event', self.onClick)

        self.art1.init_animation()
        self.art2.init_animation()
        self.art3.init_animation()

    # def onClick(self, event):
    #    # print(event.button, event.xdata, event.ydata)
    #    # if (event.button == 3):
    #    self.show_future = not self.show_future

    def on_resize(self, event):
        pass

    def handle_close(self, event):
        pass

    def press(self, event):
        pass


    def draw_frame(self, curpos):
        self.cur_pos = curpos
        if (self.cur_pos > self.max_curpos):
            self.its_review = False

        self._drawn_artists = self.art1.animate(self.cur_pos, self.pass_pos, self.its_review, self.show_future) \
                              + self.art2.animate(self.cur_pos, self.pass_pos, self.its_review, self.show_future) \
                              + self.art3.animate(self.cur_pos, self.pass_pos, self.its_review, self.show_future)

        self.max_curpos = max(self.cur_pos, self.max_curpos)

        self.pass_pos = self.cur_pos - dm1.data_len

        if self.cur_pos < dm1.all_len - dm1.predict_len:
            self.cur_pos += 1




if __name__ == "__main__":
    gc.disable()
    gc.enable()

    if (len(sys.argv) != 4):
        print 'Usage: python future-predict.py <inst> <the trade day> <data file path>\n' \
              '       For example:\n' \
              '           python future-predict.py al888 20150601 /data/sean/data/sean/10s_candle_bindata\n'
    else:
        inst = sys.argv[1].encode('ascii')
        day = sys.argv[2].encode('ascii')
        path = sys.argv[3].encode('ascii')

        # all_data, all_ask, all_bid, all_len, allx, the_date = get_data()
        ret, all_len, price, ftime = get_10s_data_from_file(inst, day, path, 102400)
        if (ret == 0) and (all_len >= 102400):
            dm1 = DataMath(price, ftime, all_len, day)
            dm2 = DataMath(price, ftime, all_len, day)
            dm2.down_sample(20)
            dm3 = DataMath(price, ftime, all_len, day)
            dm3.down_sample(200)
            # print dm1.all_len, dm2.all_len, dm3.all_len

            # opq = str(raw_input("enter something to draw: (q = quit)"))
            # if (opq == 'q'):
            #     exit(0)

            # params = {'legend.fontsize': 'small',
            #           'figure.figsize': (48, 21),
            #           'axes.labelsize': 'small',
            #           'axes.titlesize': 'small',
            #           'xtick.labelsize': 'small',
            #           'ytick.labelsize': 'small'}

            ani = SubplotAnimation(dm1, dm2, dm3)
            plt.suptitle(inst + " - " + day, fontsize=16)

            ani.draw_frame(all_len - 1)
            # ani.save('test_sub.mp4')
            # plt.savefig('/home/sean/tmp/' + inst + "-" + day + '.png')
            plt.show()

