import random
from libnrlib import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import sys

data_len = 1024
prdtlen = 128
lvl_hi  = 7
lvl_lo  = 5
alllen  = 65536
anim_interval = 10
cur_pos = data_len
predict = Predict(data_len, prdtlen)
wt = WaveletFilter(1, data_len, lvl_hi)

plt.rcParams['figure.figsize'] = [16, 7]
# plt.ion()
fig = plt.figure()
ax = plt.axes(xlim=(0, data_len * 2 + prdtlen), ylim=(-20, 20))

lPassed, = ax.plot([],[],lw=1,color='black')
lCurrent, = ax.plot([],[],lw=1,color='blue')
lFuture, = ax.plot([],[],lw=1,color='green')
lRest, = ax.plot([],[],lw=1,color='black')
lappx_hi, = ax.plot([], [], lw=1, color='yellow')
lappx_lo, = ax.plot([], [], lw=1, color='pink')
lp_hi, = ax.plot([], [], lw=1, color='red')
# lp_lo, = ax.plot([], [], lw=1, color='cyan')
lines = [lPassed, lCurrent, lFuture, lRest, lappx_hi, lappx_lo, lp_hi] #, lp_lo]


all_data = []
b = 0
for i in range(0, alllen):
    b += (random.random() - 0.5) * 3
    all_data.append(b)
allx = list(range(0, alllen))

def init():
    for line in lines:
        line.set_data([],[])
    return lines

show_future = False

def animate(i):
    global cur_pos

    xlim = list(ax.get_xlim())
    delta = curpos + prdtlen + data_len - xlim[1]
    if delta > 0:
        xlim[0] = xlim[0] + prdtlen
        xlim[1] = xlim[1] + prdtlen
    ax.set_xlim(xlim)

    ylim = list(ax.get_ylim())

    passpos = curpos - data_len
    ymax = np.amax(all_data[int(xlim[0]) : curpos + prdtlen + data_len])
    ymin = np.amin(all_data[int(xlim[0]) : curpos + prdtlen + data_len])
    if (ymin < ylim[0]) or (ymin > ylim[0] + 10):
        ylim[0] = ymin - 5
    if (ymax > ylim[1]) or (ymax < ylim[1] - 10):
        ylim[1] = ymax + 5

    ax.set_ylim(ylim)



    # predict.setdata(alldata[curpos + 1 - datalen : curpos])
    # p = predict.predict()

    wt.setdata(all_data[curpos - data_len : curpos])
    wt.set(1, data_len, lvl_hi)
    appx_hi = wt.filter()

    wt.setdata(all_data[curpos - data_len: curpos])
    wt.set(1, data_len, lvl_lo)
    appx_lo = wt.filter()

    predict.setdata(appx_hi)
    ap_hi = predict.predict()
    # predict.setdata(appx_lo)
    # ap_lo = predict.predict()

    lPassed.set_data(allx[int(xlim[0]) : passpos],
                     all_data[int(xlim[0]) : passpos])

    lCurrent.set_data(allx[passpos : curpos],
                      all_data[passpos : curpos])

    if show_future:
        lFuture.set_data(allx[curpos : curpos + prdtlen],
                         all_data[curpos: curpos + prdtlen])

        lRest.set_data(allx[curpos + prdtlen : curpos + prdtlen + data_len],
                       all_data[curpos + prdtlen : curpos + prdtlen + data_len])
    else:
        lFuture.set_data([], [])
        lRest.set_data([],[])

    lappx_hi.set_data(allx[passpos : curpos], appx_hi)
    lappx_lo.set_data(allx[passpos : curpos], appx_lo)

    lp_hi.set_data(allx[curpos : curpos + prdtlen], ap_hi)
    # lp_lo.set_data(allx[curpos : curpos + prdtlen], ap_lo)

    curpos += 1


    return tuple(lines)


anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=(alllen - data_len), interval=anim_interval, blit=True)
anim_running = True

def onClick(event):
    global anim_running, cur_pos, show_future
    # print(event.button, event.xdata, event.ydata)

    if ((event.xdata is None) or (event.ydata is None)):
        return

    if (event.button == 1):
        if anim_running:
            xpos = int(event.xdata)
            if (xpos > data_len):
                curpos = xpos
            anim.event_source.stop()
            anim_running = False
        else:
            anim.event_source.start()
            anim_running = True
    elif (event.button == 3):
        show_future = not show_future


def handle_close(evt):
    anim.event_source.stop()


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

def press(event):
    global cur_pos, all_data, trade
    # print('press', event.key)
    # sys.stdout.flush()
    if event.key == 'a':
        if (0 == len(t) % 2):
            print 'Ask ', curpos, alldata[curpos]
            t.append(Trade('a', curpos, alldata[curpos]))
    elif event.key == 'b':
        if (1 == len(t) % 2):
            print 'Bid ', curpos, alldata[curpos]
            t.append(Trade('b', curpos, alldata[curpos]))
    elif event.key == 'c':
        if (1 == len(t) % 2):
          c = Trade('c', curpos, alldata[curpos])
          if t[-1].direct == 'a':
              c.rev = c.value - t[-1].value
          else:
              c.rev = t[-1].value - c.value
          t.append(c)
          print 'Close', curpos, alldata[curpos], c.rev


fig.canvas.mpl_connect('key_press_event', press)
fig.canvas.mpl_connect('close_event', handle_close)
fig.canvas.mpl_connect('button_press_event', onClick)

plt.show()
