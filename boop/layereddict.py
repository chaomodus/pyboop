from collections import OrderedDict


class LayeredDict(object):
    """
    This is a utility class that basically is a dictionary-like object that may contain several
    sub-dictionaries which may be added and removed at any time, such that accesses with be an
    ordered search through the sub-dictionaries.

    Read accesses simply iterate the sub-dictionary stack and return the first result.

    Write accesses first search for the key specified, which if found is set to the value,
    otherwise the top of the stack recieves the value.


    Each dictionary in the stack also has a label which can be used to access the values
    on that specific dictionary.
    """

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
        """Get the sub-dictionary in the stack of the specific label. (DEPRECATED)"""
        return self.get_label(label)

    def get(self, label):
        """Get the sub-dictionary in the stack of the specific label."""
        if label in self.dictstack:
            return self.dictstack[label]
        return None

    def getidx(self, index):
        """Get the sub-dictionary in the stack of the specific index."""
        if index < len(self.dictstack):
            return self.get(self.dictstack.keys()[index])
        return None

    def labels(self):
        """Return a list of labels of sub-dicitonaries."""
        return self.dictstack.keys()

    def push(self, container, label=None):
        """Push a new sub-dictionary onto the stack with a specified label (a uniquely numbered label will be assigend if none is specified)."""
        if label is None:
            self.idx += 1
            label = self.idx
        self.dictstack[label] = container
        return label

    def pop(self):  # will eat itself
        """Remove the top sub-dictionary from the stack."""
        label = self.dictstack.keys()[-1]
        return self.remove(label)

    def remove(self, label):
        """Remove a specific item from the sub-dictionary stack by label."""
        thing = None
        if label in self.dictstack:
            thing = self.dictstack[label]
            del self.dictstack[label]
        return label, thing

    def removeidx(self, idx):
        """Remove a specific item from the sub-dictionary stack by index."""
        if idx <= len(self.dictstack):
            return self.remove(self.dictstack.keys()[idx])
        return None, None

    def __repr__(self):
        out = '<LayeredDict '
        for i, k in reversed(list(enumerate(self.dictstack.keys()))):
            out += '[{i}]{k}:{v} '.format(i=i, k=k, v=self.dictstack[k].__repr__())
        return out + '>'
