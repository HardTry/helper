from libnrlib import *
import matplotlib.pyplot as plt

m12 = Math12()
print type(m12), m12
ret = m12.get_data_from_file('rb888', '/data/sean/10s_candle_bindata/rb888', '20171108', 1)
print 'ret =', ret

all_len = m12.get_data_length()
# for i in range(1024 * 2048, m12.get_data_length()):
#    m12.do_math(i)
#    if (i % 1000 == 0):
#        print i

curpos = (1024 + 1) * 2048
m12.do_math(curpos) #m12.get_data_length())

down_int = 1
for i in range(0, 12):
    plt.clf()
    cp = curpos / down_int - 1
    down_int *= 2
    price = []
    # m12.get_price(price, i)
    m12.get_hop_price(price, i)
    if cp - 1024 < 0:
        pos = 0
    else:
        pos = cp - 1024
    x = list(range(pos , cp))
    # print pos, curpos, cp, ">", len(price), len(x), len(price[pos : cp])
    plt.plot(x, price[pos : cp])

    ex = []
    ey = []
    m12.get_extremes(ex, ey, i)
    plt.plot(ex, ey, 'x')
    
    appx = []
    m12.get_approx_line(appx, i)
    x = list(range(cp - len(appx), cp))
    plt.plot(x, appx)
    
    predict = []
    m12.get_predict_line(predict, i)
    px = list(range(cp, cp + len(predict)))
    plt.plot(px, predict)
    
    min_x = []
    min_y = []
    max_x = []
    max_y = []
    m12.get_max_min_line(max_x, max_y, min_x, min_y, i)
    plt.plot(max_x, max_y)
    plt.plot(min_x, min_y)

    plt.show()