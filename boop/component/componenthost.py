import collections


class ComponentHost(object):
    def __init__(self):
        self.components = collections.OrderedDict()

    def handle_event(self, event_type, state, *args, **kwargs):
        state.container = self
        for component in self.components.values():
            component.handle_event(event_type, state, *args, **kwargs)

    def add(self, component, label=None):
        if label is None:
            label = hash(component)

        self.components[label] = component
        return label

    def remove(self, component, label=None):
        if component is None and label is not None:
            if label in self.components:
                component = self.components[label]
                del self.components[label]
                return component
        else:
            for label, comp in self.components:
                if comp == component:
                    del self.components[label]
                    return comp

    def get(self, label):
        if label in self.components:
            return self.components[label]
        return None
