from mongoengine import *
import random
from libnrlib import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation



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


the_date = ''

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
    return all_data, all_ask, all_bid, all_len, allx


all_data, all_ask, all_bid, all_len, allx = get_one_day_data()

data_len = 1024
predict_len = 128
lvl_hi = 7
lvl_lo = 4
anim_interval = 100
cur_pos = data_len
comm = 2

show_future = False
max_curpos = cur_pos
its_review = False

predict = Predict(data_len, predict_len)
wt = WaveletFilter(1, data_len, lvl_hi)

plt.rcParams['figure.figsize'] = [16, 7]
# plt.ion()


ax = plt.axes(xlim=(0, data_len + predict_len), ylim=(np.amax(all_data[0: cur_pos]), np.amin(all_data[0 : cur_pos])))

lPassed, = ax.plot([], [], lw=1, color='black')
fig = plt.figure()
lCurrent, = ax.plot([], [], lw=1, color='blue')
lFuture, = ax.plot([], [], lw=1, color='green')
lappx_hi, = ax.plot([], [], lw=1, color='yellow')
lappx_lo, = ax.plot([], [], lw=1, color='pink')
lp_hi, = ax.plot([], [], lw=1, color='red')
lExtrem, = ax.plot([], [], 'rx', lw=1)  # lw=2, color='black', marker='o', markeredgecolor='b')
lNow, = ax.plot([], [], lw=1, color='green')

# lp_lo, = ax.plot([], [], lw=1, color='cyan')

txtTrade = ax.text(-1000, 8, 'text ask', fontsize=15, color='red')
txtRev = ax.text(-1000, 8, 'text rev', fontsize=15, color='black')
txtAllRev = ax.text(-1000, 8, 'text all rev', fontsize=15, color='black')

strTrade = ''
strRev = ''
strAllRev = ''

lines = [lPassed, lCurrent, lFuture, lappx_hi, lappx_lo, lp_hi, lExtrem, lNow]  # , lp_lo]

cur_appx_lo = []
cur_appx_spos = cur_pos
cur_appx_epos = cur_appx_spos + data_len
cur_ext_pos = []
cur_ext_val = []




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


trade = []
allrev = 0

def init():
    for line in lines:
        line.set_data([], [])
    return lines


def update_limite(xlim, ylim):
    global cur_pos, passpos
    delta = cur_pos + predict_len - xlim[1]
    if delta > 0:
        xlim[0] = xlim[0] + predict_len
        xlim[1] = xlim[1] + predict_len
    ax.set_xlim(xlim)

    passpos = cur_pos - data_len
    ymax = np.amax(all_data[int(xlim[0]): cur_pos])
    ymin = np.amin(all_data[int(xlim[0]): cur_pos])
    if (ymin < ylim[0]) or (ymin > ylim[0] + 10):
        ylim[0] = ymin - 5
    if (ymax > ylim[1]) or (ymax < ylim[1] - 10):
        ylim[1] = ymax + 5
    ax.set_ylim(ylim)


def do_math():
    global cur_pos, data_len, lvl_hi, lvl_lo
    # predict.setdata(alldata[curpos + 1 - datalen : curpos])
    # p = predict.predict()

    wt.setdata(all_data[cur_pos - data_len: cur_pos])
    wt.set(1, data_len, lvl_hi)
    appx_hi = wt.filter()

    wt.setdata(all_data[cur_pos - data_len: cur_pos])
    wt.set(1, data_len, lvl_lo)
    appx_lo = wt.filter()

    predict.setdata(appx_hi)
    ap_hi = predict.predict()

    ext_pos = []
    ext_val = []
    first = get_max_min(appx_lo, cur_pos - data_len, ext_pos, ext_val)

    # predict.setdata(appx_lo)
    # ap_lo = predict.predict()

    return appx_hi, appx_lo, ap_hi, ext_pos, ext_val, first


def update_lines(xlim, appx_hi, appx_lo, ap_hi, ext_pos, ext_val, first):
    global cur_pos, passpos, allx, all_data
    global lPassed, lCurrent, lFuture, lappx_hi, lappx_lo, lp_hi
    global show_future
    global cur_appx_lo
    global cur_appx_spos
    global cur_appx_epos
    global cur_ext_pos, cur_ext_val
    global lExtrem

    if its_review:
        lPassed.set_data(allx[int(xlim[0]): passpos],
                         all_data[int(xlim[0]): passpos])

        lCurrent.set_data(allx[passpos: cur_pos],
                          all_data[passpos: cur_pos])

        if show_future:
            lFuture.set_data(allx[cur_pos: cur_pos + predict_len],
                             all_data[cur_pos: cur_pos + predict_len])

        else:
            lFuture.set_data([], [])

        lNow.set_data([cur_ext_pos[0], cur_pos], [cur_ext_val[0], all_data[cur_pos]])

        lappx_hi.set_data(allx[passpos: cur_pos], appx_hi)
        lappx_lo.set_data(allx[passpos: cur_pos], appx_lo)

        lp_hi.set_data(allx[cur_pos: cur_pos + predict_len], ap_hi)
        # lp_lo.set_data(allx[curpos : curpos + prdtlen], ap_lo)

        # lExtrem.set_data(cur_ext_pos, cur_ext_val)
    else:
        keep = 0
        if (len(cur_appx_lo) == 0):
            cur_appx_lo = appx_lo
            cur_appx_epos = cur_pos
            cur_appx_spos = cur_appx_epos - data_len
            cur_ext_pos = ext_pos
            cur_ext_val = ext_val
            keep = 2
        else:
            # get the differ
            keep = select_appx(all_data[cur_pos - data_len: cur_pos], cur_appx_lo, appx_lo, cur_ext_pos, ext_pos,
                               cur_appx_spos, cur_appx_epos, cur_pos - data_len, cur_pos)
            if (keep == 2):
                cur_appx_lo = appx_lo
                cur_appx_epos = cur_pos
                cur_appx_spos = cur_appx_epos - data_len
                cur_ext_pos = ext_pos
                cur_ext_val = ext_val

        lPassed.set_data(allx[int(xlim[0]): passpos],
                         all_data[int(xlim[0]): passpos])

        lCurrent.set_data(allx[passpos: cur_pos],
                          all_data[passpos: cur_pos])

        if show_future:
            lFuture.set_data(allx[cur_pos: cur_pos + predict_len],
                             all_data[cur_pos: cur_pos + predict_len])

        else:
            lFuture.set_data([], [])

        lNow.set_data([cur_ext_pos[0], cur_pos], [cur_ext_val[0], all_data[cur_pos]])

        if keep == 2:
            lappx_hi.set_data(allx[passpos: cur_pos], appx_hi)
            lappx_lo.set_data(allx[passpos: cur_pos], appx_lo)

            lp_hi.set_data(allx[cur_pos: cur_pos + predict_len], ap_hi)
            # lp_lo.set_data(allx[curpos : curpos + prdtlen], ap_lo)

            lExtrem.set_data(cur_ext_pos, cur_ext_val)


def update_revenue(xlim, ylim):
    global strRev, strAllRev, strTrade
    global allrev, trade

    rev = 0
    if (1 == len(trade) % 2):
        if trade[-1].direct == 'a':
            rev = (all_data[cur_pos] - trade[-1].value) * 10
            txtTrade.set_color('red')
        else:
            rev = (trade[-1].value - all_data[cur_pos]) * 10
            txtTrade.set_color('green')
        strRev = str(rev)
    else:
        strRev = ''

    txtTrade.set_position((xlim[1] - 100, ylim[1] - 3))
    txtTrade.set_text(strTrade)

    txtRev.set_position((xlim[1] - 100, ylim[1] - 8))
    if (rev > 0):
        txtRev.set_color('red')
    else:
        txtRev.set_color('green')
    txtRev.set_text(strRev)

    txtAllRev.set_position((xlim[1] - 100, ylim[1] - 13))
    if (allrev > 0):
        txtAllRev.set_color('red')
    else:
        txtAllRev.set_color('green')
    txtAllRev.set_text(strAllRev)


def animate(i):
    global cur_pos, max_curpos, its_review

    xlim = list(ax.get_xlim())
    ylim = list(ax.get_ylim())
    update_limite(xlim, ylim)

    appx_hi, appx_lo, ap_hi, ext_pos, ext_val, first = do_math()

    update_lines(xlim, appx_hi, appx_lo, ap_hi, ext_pos, ext_val, first)

    update_revenue(xlim, ylim)

    if (cur_pos > max_curpos):
        its_review = False
    max_curpos = max(cur_pos, max_curpos)

    if cur_pos < all_len - predict_len:
        cur_pos += 1

    return tuple(lines) + (txtTrade, txtRev, txtAllRev)


anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=(all_len - data_len), interval=anim_interval, blit=True)
anim_running = True


def onClick(event):
    global anim_running, cur_pos, show_future, its_review
    # print(event.button, event.xdata, event.ydata)

    if (event.button == 1):
        if anim_running:
            anim.event_source.stop()

            if ((event.xdata is None) or (event.ydata is None) or (event.xdata > cur_pos)):
                return

            xpos = int(event.xdata)
            if (xpos > data_len):
                cur_pos = xpos
                its_review = True
            anim_running = False
        else:
            anim.event_source.start()
            anim_running = True
    elif (event.button == 3):
        show_future = not show_future


def handle_close(evt):
    anim.event_source.stop()


def get_prev_ext():
    global cur_pos, cur_ext_pos


def get_next_ext():
    global cur_pos, cur_ext_pos


def press(event):
    global cur_pos, all_data, trade, allrev, strTrade, strAllRev, anim_running
    global max_curpos, its_review
    # print('press', event.key)
    # sys.stdout.flush()
    if event.key == 'a':
        if (0 == len(trade) % 2):
            print 'Long ', cur_pos, all_ask[cur_pos]
            strTrade = 'Long'
            trade.append(Trade('a', cur_pos, all_ask[cur_pos]))
    elif event.key == 'b':
        if (0 == len(trade) % 2):
            print 'Short ', cur_pos, all_bid[cur_pos]
            strTrade = 'Short'
            trade.append(Trade('b', cur_pos, all_bid[cur_pos]))
    elif event.key == 'c':
        if (1 == len(trade) % 2):
            strTrade = ''
            c = Trade('c', cur_pos, all_data[cur_pos])
            if trade[-1].direct == 'a':
                c.rev = (c.value - trade[-1].value) * 10 - (c.value + trade[-1].value) * 0.0015
            else:
                c.rev = (trade[-1].value - c.value) * 10 - (c.value + trade[-1].value) * 0.0015
            trade.append(c)
            allrev += c.rev
            strAllRev = str(allrev)
            print 'Close', cur_pos, all_data[cur_pos], c.rev, allrev
    elif event.key == 'p':
        if anim_running:
            anim.event_source.stop()
            anim_running = False
        else:
            anim.event_source.start()
            anim_running = True
    elif event.key == 'j':
        if cur_pos > data_len:
            cur_pos -= 1
            its_review = True
    elif event.key == 'h':
        if cur_pos - 10 > data_len:
            cur_pos -= 10
            its_review = True
    elif event.key == 'k':
        if cur_pos + 1 < max_curpos:
            cur_pos += 1
            its_review = True
    elif event.key == 'l':
        if cur_pos + 10 < max_curpos:
            cur_pos += 8
            its_review = True
    elif event.key == 'i':
        cur_pos = get_prev_ext()
        its_review = True
    elif event.key == 'o':
        cur_pos = get_next_ext()
        its_review = True
    elif event.key == 'e':
	print the_date, cur_pos, " has Error"        


fig.canvas.mpl_connect('key_press_event', press)
fig.canvas.mpl_connect('close_event', handle_close)
fig.canvas.mpl_connect('button_press_event', onClick)

plt.show()
