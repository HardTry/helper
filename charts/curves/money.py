class MoneyCurves(object):

    def __init__(self, trade, start=0):
        self.y = []
        self.x = []
        self.start = start
        self.trade = trade

    def get_point_y(self):
        return self.trade.money

    def get_point_x(self):
        # ttime = []
        # self.m12.get_time(ttime)
        self.x = range(self.start, self.trade.len+self.start)
        return self.x

    def get_y_from_x(self, point):
        return self.y[point]
