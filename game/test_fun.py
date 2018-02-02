class T:
  def  __init__(self, a):
    self.a = a
    self.f = None

  def add(self, b):
    self.f(self.a, b)

  def set_fun(self, f):
    self.f = f


def f(a, b):
  print a + b

t = T(1)
t.set_fun(f)
t.add(2)
