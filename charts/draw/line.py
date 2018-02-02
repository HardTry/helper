class Line(object):
    def __init__(self, ax, data_x, data_y, color='g', sz='8', sp='o', zo=1, ap=1):
        self.ax = ax
        self.color = color
        self.size = sz
        self.shape = sp
        self.data_x = data_x
        self.data_y = data_y
        self.zorder = zo
        self.alpha = ap

    def plot(self):
        # print self.shape
        self.ax.plot(self.data_x, self.data_y, self.shape, color=self.color, markersize=self.size, lw=1, zorder=self.zorder, alpha=self.alpha)

    def set_color(self, color):
        self.color = color
