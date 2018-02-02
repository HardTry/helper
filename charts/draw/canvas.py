import matplotlib.pyplot as plt
import os

from core.config import DRAW_DIR


class Canvas(object):

    def __init__(self, index, row, col, title=None):
        self.row = int(row)
        self.col = int(col)
        self.count = self.row * self.col

        self.fig = plt.figure(index, figsize=(8, 4.5))
        self.fig.tight_layout()
        self.anim_interval = 10

        self.__ax = []
        for i in range(0, self.count):
            self.__ax.append(self.fig.add_subplot(self.row, self.col, i+1))

        if title:
            self.fig.canvas.set_window_title(title)

    def set_title(self, title):
        self.fig.canvas.set_window_title(title)

    @property
    def ax(self):
        return self.__ax

    def save_image(self, inst, image_type):
        img_path = os.path.join(DRAW_DIR, '%s-%s.png' % (inst, image_type))
        plt.savefig(img_path)
        print 'save to', img_path

    def show_image(self):
        plt.show()

