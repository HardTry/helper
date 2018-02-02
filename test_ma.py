import random
from libnrlib import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import sys

data_len = 1024
level = 10
alllen  = 1024

all_data = []
b = 0
for i in range(0, alllen):
    b += (random.random() - 0.5) * 3
    all_data.append(b)
allx = list(range(0, alllen))


ma = MaFilter(level, data_len)

ma.set(level, data_len)
ma.setdata(all_data[0: data_len])
f1 = ma.filter()

ma.set(20, data_len)
f2 = ma.filter()
ma.set(30, data_len)
f3 = ma.filter()

plt.plot(allx, all_data)
plt.plot(allx[0: data_len], f1)
plt.plot(allx[0: data_len], f2)
plt.plot(allx[0: data_len], f3)
plt.show()
