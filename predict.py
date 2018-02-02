import random
from libnrlib import *
import matplotlib.pyplot as plt

def prdct():
  datalen = 1024
  prdtlen = 256
  continued = 1024
  level = 5

  a = []
  b = 1
  for i in range(0, datalen):
      b += (random.random() - 0.5) * 2
      a.append(b)

  c = []
  for i in range(0, prdtlen):
      b += (random.random() - 0.5) * 2
      c.append(b)

  d = []
  for i in range(0, continued):
      b += (random.random() - 0.5) * 2
      d.append(b)


  predict = Predict(datalen, prdtlen)
  predict.setdata(a)
  p = predict.predict()

  x1 = list(range(0, datalen))
  x2 = list(range(datalen, datalen + prdtlen))
  x3 = list(range(datalen + prdtlen, datalen + prdtlen + continued))

  wt = WaveletFilter(1, datalen, level)
  wt.setdata(a)
  appx = wt.filter()

  predict.setdata(appx)
  ap = predict.predict()

  plt.rcParams['figure.figsize'] = [11, 6]
  plt.plot(x1, a)
  # plt.plot(x2, p)
  plt.plot(x1, appx)
  plt.plot(x2, c)
  plt.plot(x2, ap)
  plt.plot(x3, d)

  plt.show()


while(True):
    q = str(raw_input("enter something: "))
    if (q == 'q'):
        break
    prdct()
