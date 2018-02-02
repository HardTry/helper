from core.utils import load_file
from draw.line import Line


class DrawPrice(object):

    def __init__(self, ax, data, instrument, levels, log_path):

        self.levels = levels
        self.trade_path = log_path
        self.ax = ax
        self.inst_code = instrument
        self.x = data[0]
        self.y = data[1]

    def __load_trade_log(self, level, color):
        open_long_x = []
        open_short_x = []
        close_long_x = []
        close_short_x = []
        open_long_y = []
        open_short_y = []
        close_long_y = []
        close_short_y = []
        lines = load_file(self.trade_path % (self.inst_code, level))
        for l in lines:
            if l[0:4] == 'Open':
                direction, position = self.__get_line_data(l)
                if direction > 0:
                    open_long_x.append(position)
                    open_long_y.append(self.y[position-2099200])
                else:
                    open_short_x.append(position)
                    open_short_y.append(self.y[position-2099200])
            if l[0:5] == 'Close':
                direction, position = self.__get_line_data(l)
                if direction > 0:
                    close_long_x.append(position)
                    close_long_y.append(self.y[position-2099200])
                else:
                    close_short_x.append(position)
                    close_short_y.append(self.y[position-2099200])
        return [
            Line(self.ax, open_long_x, open_long_y, color=color, sp='^'),
            Line(self.ax, close_long_x, close_long_y, color=color, sp='*'),
            Line(self.ax, open_short_x, open_short_y, color=color, sp='v'),
            Line(self.ax, close_short_x, close_long_y, color=color, sp='x')
        ]

    def __get_line_data(self, line):
        direction, pos = line.split(',')[2:4]
        return int(direction), int(pos)

    def draw(self, colors):
        lines = [
            Line(self.ax, self.x, self.y, 'b', sp='-'),
        ]
        i = 0
        for l in self.levels:
            lines += self.__load_trade_log(l, colors[i])
            i += 1
        return lines
