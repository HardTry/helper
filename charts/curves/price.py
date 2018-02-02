from curves.model import Model


class PriceCurves(Model):

    """
    Prepare data
    """

    def __init__(self, params, datapath, start=0):
        self.y = []
        self.x = []
        self.level = params.level
        self.start = start
        super(PriceCurves, self).__init__(params, datapath)

    def get_point_y(self):
        self.m12.get_price(self.y, self.level)
        return self.y[self.start:]

    def get_point_x(self):
        # ttime = []
        # self.m12.get_time(ttime)
        self.x = range(self.start, self.len)
        return self.x

    def get_y_from_x(self, point):
        return self.y[point-1]
