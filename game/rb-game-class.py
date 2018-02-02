from mongoengine import *
import random
from libnrlib import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib.lines import Line2D

class Tick(Document):
    askVolume1 = FloatField()
    lastPrice = FloatField()
    askPrice1 = FloatField()
    bidPrice1 = FloatField()
    strDate = StringField()
    Volume = FloatField()
    instrument = StringField()
    bidVolume1 = FloatField()
    openInterest = FloatField()
    strTime = StringField()
    fltTime = FloatField()

    meta = {
        'collection': 'tickdata'
    }



def get_one_day_data():
    global the_date
    register_connection("ctpdata", host='10.10.10.13', port=29875)
    conn = connect(db="ctpdata", host='10.10.10.13', port=29875)
    tdays = Tick.objects(instrument='rb888').distinct("strDate")

    SelectedDate = tdays[random.randrange(0, len(tdays))]
    prevdate = int(SelectedDate) - 1
    while(True):
        if (str(prevdate) in tdays):
            break
        prevdate -= 1

    the_date = str(prevdate)
    print SelectedDate, the_date

    prev_ticks = Tick.objects(instrument='rb888', strDate=the_date)
    last = []
    ask = []
    bid = []
    for tick in prev_ticks:
        last.append(tick.lastPrice)
        ask.append(tick.askPrice1)
        bid.append(tick.bidPrice1)

    print len(last)
    ticks = Tick.objects(instrument='rb888', strDate=SelectedDate)
    conn.close()

    for tick in ticks:
        last.append(tick.lastPrice)
        ask.append(tick.askPrice1)
        bid.append(tick.bidPrice1)

    print len(last)
    all_data = sample_max_min(last, 20)
    all_ask = sample_max_min(ask, 20)
    all_bid = sample_max_min(bid, 20)
    all_len = len(all_data)

    print len(last), all_len
    allx = list(range(0, all_len))
    return all_data, all_ask, all_bid, all_len, allx, the_date



class DataMath:
    def __init__(self):
        self.all_data, self.all_ask, self.all_bid, self.all_len, self.allx, self.the_date = get_one_day_data()

        self.data_len = 1024
        self.predict_len = 128
        self.lvl_hi = 7
        self.lvl_lo = 4
        self.anim_interval = 100
        self.cur_pos = self.data_len
        self.comm = 2
        self.max_curpos = self.cur_pos
        self.passpos = 0
        self.predict = Predict(self.data_len, self.predict_len)
        self.wt = WaveletFilter(1, self.data_len, self.lvl_hi)

        self.cur_appx_lo = []
        self.cur_appx_spos = self.cur_pos
        self.cur_appx_epos = self.cur_appx_spos + self.data_len
        self.cur_ext_pos = []
        self.cur_ext_val = []

        self.trade = []
        self.allrev = 0

    def do_math(self):
        # predict.setdata(alldata[curpos + 1 - datalen : curpos])
        # p = predict.predict()

        self.wt.setdata(self.all_data[self.cur_pos - self.data_len: self.cur_pos])
        self.wt.set(1, self.data_len, self.lvl_hi)
        appx_hi = self.wt.filter()

        self.wt.setdata(self.all_data[self.cur_pos - self.data_len: self.cur_pos])
        self.wt.set(1, self.data_len, self.lvl_lo)
        appx_lo = self.wt.filter()

        self.predict.setdata(appx_hi)
        ap_hi = self.predict.predict()

        ext_pos = []
        ext_val = []
        first = get_max_min(appx_lo, self.cur_pos - self.data_len, ext_pos, ext_val)

        # predict.setdata(appx_lo)
        # ap_lo = predict.predict()

        return appx_hi, appx_lo, ap_hi, ext_pos, ext_val, first



class Artist:
    def __init__(self, dm):
        self.show_future = False
        self.its_review = False
        plt.rcParams['figure.figsize'] = [16, 7]
        self.fig = plt.figure()
        self.ax = plt.axes(xlim=(0, dm.data_len + dm.predict_len), ylim=(np.amax(dm.all_data[0: dm.cur_pos]), np.amin(dm.all_data[0 : dm.cur_pos])))

        self.lPassed,  = self.ax.plot([], [], lw=1, color='black')
        self.lCurrent, = self.ax.plot([], [], lw=1, color='blue')
        self.lFuture,  = self.ax.plot([], [], lw=1, color='green')
        self.lappx_hi, = self.ax.plot([], [], lw=1, color='yellow')
        self.lappx_lo, = self.ax.plot([], [], lw=1, color='pink')
        self.lp_hi,    = self.ax.plot([], [], lw=1, color='red')
        self.lExtrem,  = self.ax.plot([], [], 'rx', lw=1)  # lw=2, color='black', marker='o', markeredgecolor='b')
        self.lNow,     = self.ax.plot([], [], lw=1, color='green')

        self.txtTrade  = self.ax.text(-1000, 8, 'text ask', fontsize=15, color='red')
        self.txtRev    = self.ax.text(-1000, 8, 'text rev', fontsize=15, color='black')
        self.txtAllRev = self.ax.text(-1000, 8, 'text all rev', fontsize=15, color='black')

        self.strTrade = ''
        self.strRev = ''
        self.strAllRev = ''

        self.lines = [self.lPassed, self.lCurrent, self.lFuture, self.lappx_hi, self.lappx_lo, self.lp_hi, self.lExtrem, self.lNow]  # , lp_lo]

    def init_animation(self):
        for line in self.lines:
            line.set_data([], [])
        return self.lines

    def update_limite(self, xlim, ylim):
        delta = dm.cur_pos + dm.predict_len - xlim[1]
        if delta > 0:
            xlim[0] = xlim[0] + dm.predict_len
            xlim[1] = xlim[1] + dm.predict_len
        self.ax.set_xlim(xlim)

        ###refactor!!
        dm.passpos = dm.cur_pos - dm.data_len
        ymax = np.amax(dm.all_data[int(xlim[0]): dm.cur_pos])
        ymin = np.amin(dm.all_data[int(xlim[0]): dm.cur_pos])
        if (ymin < ylim[0]) or (ymin > ylim[0] + 10):
            ylim[0] = ymin - 5
        if (ymax > ylim[1]) or (ymax < ylim[1] - 10):
            ylim[1] = ymax + 5
        self.ax.set_ylim(ylim)


    def update_lines(self, xlim, appx_hi, appx_lo, ap_hi, ext_pos, ext_val, first):
        if self.its_review:
            self.lPassed.set_data(dm.allx[int(xlim[0]): dm.passpos],
                                  dm.all_data[int(xlim[0]): dm.passpos])

            self.lCurrent.set_data(dm.allx[dm.passpos: dm.cur_pos],
                                   dm.all_data[dm.passpos: dm.cur_pos])

            if self.show_future:
                self.lFuture.set_data(dm.allx[dm.cur_pos: dm.cur_pos + dm.predict_len],
                                      dm.all_data[dm.cur_pos: dm.cur_pos + dm.predict_len])

            else:
                self.lFuture.set_data([], [])

                self.lNow.set_data([dm.cur_ext_pos[0], dm.cur_pos], [dm.cur_ext_val[0], dm.all_data[dm.cur_pos]])

            self.lappx_hi.set_data(dm.allx[dm.passpos: dm.cur_pos], appx_hi)
            self.lappx_lo.set_data(dm.allx[dm.passpos: dm.cur_pos], appx_lo)

            self.lp_hi.set_data(dm.allx[dm.cur_pos: dm.cur_pos + dm.predict_len], ap_hi)
            # lp_lo.set_data(allx[curpos : curpos + prdtlen], ap_lo)

            # lExtrem.set_data(cur_ext_pos, cur_ext_val)
        else:
            keep = 0
            if (len(dm.cur_appx_lo) == 0):
                dm.cur_appx_lo = appx_lo
                dm.cur_appx_epos = dm.cur_pos
                dm.cur_appx_spos = dm.cur_appx_epos - dm.data_len
                dm.cur_ext_pos = ext_pos
                dm.cur_ext_val = ext_val
                keep = 2
            else:
                # get the differ
                keep = select_appx(dm.all_data[dm.cur_pos - dm.data_len: dm.cur_pos], dm.cur_appx_lo, appx_lo, dm.cur_ext_pos, ext_pos,
                                   dm.cur_appx_spos, dm.cur_appx_epos, dm.cur_pos - dm.data_len, dm.cur_pos)
                if (keep == 2):
                    dm.cur_appx_lo = appx_lo
                    dm.cur_appx_epos = dm.cur_pos
                    dm.cur_appx_spos = dm.cur_appx_epos - dm.data_len
                    dm.cur_ext_pos = ext_pos
                    dm.cur_ext_val = ext_val

            self.lPassed.set_data(dm.allx[int(xlim[0]): dm.passpos],
                                  dm.all_data[int(xlim[0]): dm.passpos])

            self.lCurrent.set_data(dm.allx[dm.passpos: dm.cur_pos],
                                   dm.all_data[dm.passpos: dm.cur_pos])

            if self.show_future:
                self.lFuture.set_data(dm.allx[dm.cur_pos: dm.cur_pos + dm.predict_len],
                                      dm.all_data[dm.cur_pos: dm.cur_pos + dm.predict_len])

            else:
                self.lFuture.set_data([], [])

            self.lNow.set_data([dm.cur_ext_pos[0], dm.cur_pos], [dm.cur_ext_val[0], dm.all_data[dm.cur_pos]])

            if keep == 2:
                self.lappx_hi.set_data(dm.allx[dm.passpos: dm.cur_pos], appx_hi)
                self.lappx_lo.set_data(dm.allx[dm.passpos: dm.cur_pos], appx_lo)

                self.lp_hi.set_data(dm.allx[dm.cur_pos: dm.cur_pos + dm.predict_len], ap_hi)
                # lp_lo.set_data(allx[curpos : curpos + prdtlen], ap_lo)

                self.lExtrem.set_data(dm.cur_ext_pos, dm.cur_ext_val)



    def update_revenue(self, xlim, ylim):
        rev = 0
        if (1 == len(dm.trade) % 2):
            if dm.trade[-1].direct == 'a':
                rev = (dm.all_data[dm.cur_pos] - dm.trade[-1].value) * 10
                self.txtTrade.set_color('red')
            else:
                rev = (dm.trade[-1].value - dm.all_data[dm.cur_pos]) * 10
                self.txtTrade.set_color('green')
            self.strRev = str(rev)
        else:
            self.strRev = ''

        self.txtTrade.set_position((xlim[1] - 100, ylim[1] - 3))
        self.txtTrade.set_text(self.strTrade)

        self.txtRev.set_position((xlim[1] - 100, ylim[1] - 8))
        if (rev > 0):
            self.txtRev.set_color('red')
        else:
            self.txtRev.set_color('green')
        self.txtRev.set_text(self.strRev)

        self.txtAllRev.set_position((xlim[1] - 100, ylim[1] - 13))
        if (dm.allrev > 0):
            self.txtAllRev.set_color('red')
        else:
            self.txtAllRev.set_color('green')
            self.txtAllRev.set_text(self.strAllRev)


class Trade:
    def __init__(self):
        self.direct = ''
        self.pos_ = 0
        self.value = 0
        self.rev = 0

    def __init__(self, direct, pos, value):
        self.direct = direct
        self.pos_ = pos
        self.value = value
        self.rev = 0


dm = DataMath()
art = Artist(dm)


def init():
    return art.init_animation()


def animate(i):
    global dm, art

    xlim = list(art.ax.get_xlim())
    ylim = list(art.ax.get_ylim())
    art.update_limite(xlim, ylim)

    appx_hi, appx_lo, ap_hi, ext_pos, ext_val, first = dm.do_math()

    art.update_lines(xlim, appx_hi, appx_lo, ap_hi, ext_pos, ext_val, first)

    art.update_revenue(xlim, ylim)

    if (dm.cur_pos > dm.max_curpos):
        art.its_review = False
    dm.max_curpos = max(dm.cur_pos, dm.max_curpos)

    if dm.cur_pos < dm.all_len - dm.predict_len:
        dm.cur_pos += 1

    return tuple(art.lines) + (art.txtTrade, art.txtRev, art.txtAllRev)


anim = animation.FuncAnimation(art.fig, animate, init_func=init,
                               frames=(dm.all_len - dm.data_len), interval=dm.anim_interval, blit=True)
anim_running = True


def onClick(event):
    global anim_running, dm, art
    # print(event.button, event.xdata, event.ydata)

    if (event.button == 1):
        if anim_running:
            anim.event_source.stop()

            if ((event.xdata is None) or (event.ydata is None) or (event.xdata > dm.cur_pos)):
                return

            xpos = int(event.xdata)
            if (xpos > dm.data_len):
                dm.cur_pos = xpos
                art.its_review = True
            anim_running = False
        else:
            anim.event_source.start()
            anim_running = True
    elif (event.button == 3):
        art.show_future = not art.show_future


def handle_close(evt):
    anim.event_source.stop()


def get_prev_ext():
    global dm, art


def get_next_ext():
    global dm, art


def press(event):
    global dm, art, anim_running
    # print('press', event.key)
    # sys.stdout.flush()
    if event.key == 'a':
        if (0 == len(dm.trade) % 2):
            print 'Long ', dm.cur_pos, dm.all_ask[dm.cur_pos]
            art.strTrade = 'Long'
            dm.trade.append(Trade('a', dm.cur_pos, dm.all_ask[dm.cur_pos]))
    elif event.key == 'b':
        if (0 == len(dm.trade) % 2):
            print 'Short ', dm.cur_pos, dm.all_bid[dm.cur_pos]
            art.strTrade = 'Short'
            dm.trade.append(Trade('b', dm.cur_pos, dm.all_bid[dm.cur_pos]))
    elif event.key == 'c':
        if (1 == len(dm.trade) % 2):
            art.strTrade = ''
            c = Trade('c', dm.cur_pos, dm.all_data[dm.cur_pos])
            if dm.trade[-1].direct == 'a':
                c.rev = (c.value - dm.trade[-1].value) * 10 - (c.value + dm.trade[-1].value) * 0.0015
            else:
                c.rev = (dm.trade[-1].value - c.value) * 10 - (c.value + dm.trade[-1].value) * 0.0015
            dm.trade.append(c)
            dm.allrev += c.rev
            art.strAllRev = str(dm.allrev)
            print 'Close', dm.cur_pos, dm.all_data[dm.cur_pos], c.rev, dm.allrev
    elif event.key == 'p':
        if anim_running:
            anim.event_source.stop()
            anim_running = False
        else:
            anim.event_source.start()
            anim_running = True
    elif event.key == 'j':
        if dm.cur_pos > dm.data_len:
            dm.cur_pos -= 1
            art.its_review = True
    elif event.key == 'h':
        if dm.cur_pos - 10 > dm.data_len:
            dm.cur_pos -= 10
            art.its_review = True
    elif event.key == 'k':
        if dm.cur_pos + 1 < dm.max_curpos:
            dm.cur_pos += 1
            art.its_review = True
    elif event.key == 'l':
        if dm.cur_pos + 10 < dm.max_curpos:
            dm.cur_pos += 8
            art.its_review = True
    elif event.key == 'i':
        dm.cur_pos = get_prev_ext()
        art.its_review = True
    elif event.key == 'o':
        dm.cur_pos = get_next_ext()
        art.its_review = True
    elif event.key == 'e':
	    print dm.the_date, dm.cur_pos, " has Error"


art.fig.canvas.mpl_connect('key_press_event', press)
art.fig.canvas.mpl_connect('close_event', handle_close)
art.fig.canvas.mpl_connect('button_press_event', onClick)

plt.show()
