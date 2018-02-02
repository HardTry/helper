import matplotlib.pyplot as plt
import tmath
from libnrlib import *

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
        # self.ax.set_ylim([min(self.dm.hp[0: self.dm.data_len]),
        #                  max(self.dm.hp[0: self.dm.data_len])])
        self.ax.set_ylim([min(self.dm.price[0: self.dm.data_len]),
                          max(self.dm.price[0: self.dm.data_len])])

    def update_limite(self, xlim, ylim, cp, show_future):
        # delta = cp + self.dm.predict_len - xlim[1]
        # if delta > 0:
        xlim[0] = cp - self.dm.data_len
        xlim[1] = cp + self.dm.predict_len
        self.ax.set_xlim(xlim)

        if show_future:
            # self.ax.set_ylim([min(self.dm.hp[int(xlim[0]): int(xlim[1])]),
            #                  max(self.dm.hp[int(xlim[0]): int(xlim[1])])])
            self.ax.set_ylim([min(self.dm.price[int(xlim[0]): int(xlim[1])]),
                              max(self.dm.price[int(xlim[0]): int(xlim[1])])])
        else:
            # self.ax.set_ylim([min(self.dm.hp[int(xlim[0]): cp]),
            #                  max(self.dm.hp[int(xlim[0]): cp])])
            self.ax.set_ylim([min(self.dm.price[int(xlim[0]): cp]),
                              max(self.dm.price[int(xlim[0]): cp])])

    def update_lines(self, cp, show_future):
        # self.lCurrent.set_data(self.dm.allx[cp - self.dm.data_len: cp],
        #                        self.dm.hp[cp - self.dm.data_len: cp])
        self.lCurrent.set_data(self.dm.allx[cp - self.dm.data_len: cp],
                               self.dm.price[cp - self.dm.data_len: cp])
        self.update_extreme_appx(cp)
        self.update_extreme_lo(cp)

        # self.lma_lo.set_data(self.dm.allx[cp - self.dm.data_len: cp], self.dm.ma_lo)
        # self.lma_mid.set_data(self.dm.allx[self.dm.first_ext_pos - len(self.dm.appx_hi): \
        #                       self.dm.first_ext_pos], \
        #                       self.dm.appx_hi)
        # self.lma_hi.set_data(self.dm.allx[cp - self.dm.data_len: cp], self.dm.ma_hi)

        if show_future:
            # dlen = len(self.dm.hp[cp: cp + self.dm.predict_len])
            dlen = len(self.dm.price[cp: cp + self.dm.predict_len])
            # self.lFuture.set_data(self.dm.allx[cp: cp + dlen], \
            #                      self.dm.hp[cp: cp + self.dm.predict_len])
            self.lFuture.set_data(self.dm.allx[cp: cp + dlen], \
                                  self.dm.price[cp: cp + self.dm.predict_len])
        else:
            self.lFuture.set_data([], [])


        # print self.down_int, self.dm.first_ext_pos, self.dm.cp, cp, len(self.dm.hp), len(self.dm.price)
        # self.lNow.set_data([self.dm.first_ext_pos, cp - 1], \
        #                   [self.dm.hp[self.dm.first_ext_pos], self.dm.hp[cp - 1]])
        self.lNow.set_data([self.dm.first_ext_pos, cp - 1], \
                           [self.dm.price[self.dm.first_ext_pos], self.dm.price[cp - 1]])

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

    def animate(self, cur_pos, show_future):
        cp = cur_pos / self.down_int - 1
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

        self.update_lines(cp, show_future)

        return tuple(self.lines)

    def update(self, cur_pos, show_future = True):
        cp = cur_pos / self.down_int - 1
        # if cp >= len(self.dm.hp):
        if cp >= len(self.dm.price):
            return

        #
        # if (cp + self.dm.predict_len > self.dm.all_len):
        #     return
        #
        xlim = list(self.ax.get_xlim())
        ylim = list(self.ax.get_ylim())
        #
        self.update_limite(xlim, ylim, cp, show_future)
        #
        # self.dm.do_math(cp)

        self.update_lines(cp, show_future)


class Artist10l(Artist):
    def __init__(self, dm, ax):
        Artist.__init__(self, dm, ax, '')
        self.pls = []
        colors = [ (13.0 / 255.0, 57.0 / 255.0, 0.0 / 255.0),
                   (21.0 / 255.0, 96.0 / 255.0, 0.0 / 255.0),
                   (29.0 / 255.0, 125.0 / 255.0, 0.0 / 255.0),
                   (35.0 / 255.0, 155.0 / 255.0, 0.0 / 255.0),
                   (44.0 / 255.0, 196.0 / 255.0, 0.0 / 255.0),
                   (51.0 / 255.0, 227.0 / 255.0, 0.0 / 255.0),
                   (63.0 / 255.0, 255.0 / 255.0, 0.0 / 255.0),
                   (97.0 / 255.0, 255.0 / 255.0, 51.0 / 255.0),
                   (156.0 / 255.0, 255.0 / 255.0, 128.0 / 255.0),
                   (194.0 / 255.0, 255.0 / 255.0, 176.0 / 255.0)
                 ]
        change_pnt_color = (128.0 / 255.0, 28.0 / 255.0, 188.0 / 255.0)
        for i in range(self.dm.params.queue_pl_size):
            l, = self.ax.plot([], [], lw=1, color=colors[i])
            self.pls.append(l)



    def clean_predict_lines(self):
        for ppll in self.pls:
            ppll.set_data([], [])

    def update_all(self, cur_pos, show_future):
        Artist.update(self, cur_pos, show_future)

        cp = cur_pos/self.down_int - 1
        # if cp >= len(self.dm.hp):
        if cp >= len(self.dm.price):
            return

        amount = self.dm.ph.get_amount_results()
        for i in range(min(amount, len(self.pls))):
            bpl = []
            pl = PredictLine()
            self.dm.ph.get_best_predict(self.dm.cp, i, bpl, pl)
            if (len(bpl) > 0) and (pl.spos + pl.plen > self.dm.cp):
                x = list(range(pl.spos, pl.spos + pl.plen))
                self.pls[i].set_data(x, bpl)
            else:
                self.pls[i].set_data([], [])
            # self.ph.show_size()

        for i in range(min(amount, len(self.pls)), len(self.pls)):
            self.pls[i].set_data([], [])

            # Artist.update(self, cur_pos, False)
        # pr = list(self.dm.qpl.queue)
        # for i in range(0, min(len(self.pls), len(pr)) - 1):
        #     self.pls[i].set_data(list(range(pr[i].pos, pr[i].pos + len(pr[i].pl))),
        #                          pr[i].pl)
        # if len(pr) < len(self.pls):
        #     for i in range(len(pr), len(self.pls)):
        #         self.pls[i].set_data([], [])
        #
        # pr = list(self.dm.qcp.queue)
        # # print len(self.cpls), len(pr)
        # for i in range(0, min(len(self.cpls), self.dm.qcp.qsize()) - 1):
        #     if pr[i].pos + self.dm.predict_len > self.dm.cp:
        #         self.cpls[i].set_data(list(range(pr[i].pos, pr[i].pos + len(pr[i].pl))),
        #                               pr[i].pl)
        #     else:
        #         self.cpls[i].set_data([], [])
        # if len(pr) < len(self.cpls):
        #     for i in range(len(pr), len(self.cpls)):
        #         self.cpls[i].set_data([], [])

                    # self.l_change_pnt.set_data(list(range(self.dm.change_point.pos,
        #                                       self.dm.change_point.pos +
        #                                       len(self.dm.change_point.pl))),
        #                          self.dm.change_point.pl)

    def animate(self, cur_pos, show_future):
        self.update_all(cur_pos, show_future)

        return tuple(self.lines) + tuple(self.pls)
