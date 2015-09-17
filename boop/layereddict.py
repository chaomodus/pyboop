from collections import OrderedDict


class LayeredDict(object):
    def __init__(self):
        self.dictstack = OrderedDict()
        self.idx = 0

    def __getitem__(self, key):
        for dk in self.dictstack:
            if key in self.dictstack[dk]:
                return self.dictstack[dk][key]

    def __setitem__(self, key, value):
        found = False
        for dk in self.dictstack:
            if key in self.dictstack[dk]:
                self.dictstack[dk][key] = value
                found = True
        if not found:
            self.dictstack[self.dictstack.keys()[-1]][key] = value

    def getcont(self, label):
        if label in self.dictstack:
            return self.dictstack[label]
        return None

    def labels(self):
        return self.dictstack.keys()

    def push(self, container, label=None):
        if label is None:
            self.idx += 1
            label = self.idx
        self.dictstack[label] = container

    def pop(self):  # will eat
        del self.dictstack[self.dictstack.keys()[-1]]

    def remove(self, label):
        if label in self.dictstack:
            del self.dictstack[label]

    def removeidx(self, idx):
        del self.dictstack[self.dictstack.keys()[idx]]

    def __repr__(self):
        out = '<LayeredDict '
        for i, k in reversed(list(enumerate(self.dictstack.keys()))):
            out += '[{i}]{k}:{v} '.format(i=i, k=k, v=self.dictstack[k].__repr__())
        return out + '>'
