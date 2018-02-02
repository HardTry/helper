from libnrlib import NRParams, Math12

from core.utils import get_hop


class Model(object):

    """
    Prepare data
    """

    def __init__(self, params, datapath):
        self.params = params
        self.m12 = self.get_m12()
        self.len = self.count(datapath)

    def get_m12(self):
        ppps = NRParams()
        m12 = Math12()
        if self.params.inst == 'rb888':
            ppps.min_data_size = int(1024 * 2048 * 3)
        else:
            ppps.min_data_size = int(1024 * 2048 * 1.5)

        m12.set_param(ppps)
        return m12

    def count(self, datapath):
        ret = self.m12.get_data_from_file(self.params.inst, datapath, self.params.date, get_hop(self.params.inst))
        return ret
