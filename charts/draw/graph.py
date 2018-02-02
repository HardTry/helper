class Graph(object):

    def __init__(self, ax, data_x, data_y):
        self.ax = ax
        self.data_x = data_x
        self.data_y = data_y

    def draw_limit(self):
        self.ax.set_xlim([min(self.data_x), max(self.data_x)])
        self.ax.set_ylim([min(self.data_y), max(self.data_y)])

    def draw_line(self, lines):
        # self.draw_limit()
        for line in lines:
            line.plot()
