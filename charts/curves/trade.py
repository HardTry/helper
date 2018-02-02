class TradeCurves(object):

    times = []
    all_rev = []
    money = []

    def __init__(self, data_path):
        self.len = 0
        self.data_path = data_path
        self.load_data()

    def load_data(self):
        try:
            with open(self.data_path, 'r') as output:
                lines = output.readlines()
                self.len = len(lines)
                for line in lines:
                    t_time, all_rev, _, money = line.split(',')[:4]
                    # print all_rev
                    self.times.append(t_time)
                    self.all_rev.append(float(all_rev))
                    self.money.append(float(money))

        except IOError:
            print "Error: No such data file. Filename: %s" % self.data_path
            exit(0)