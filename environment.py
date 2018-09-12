class Environment:

    def render(self):
        raise NotImplementedError()

    def step(self, action):
        raise NotImplementedError()

    def actions(self, action):
        raise NotImplementedError()

    def reset(self):
        raise NotImplementedError()

    def done(self):
        raise NotImplementedError()

    def state(self):
        raise NotImplementedError()


class State:

    def __hash__(self):
        raise NotImplementedError()

    def __eq__(self, other):
        raise NotImplementedError()

    def successor(self, action):
        raise NotImplementedError()

    def successors(self):
        raise NotImplementedError()

    def actions(self):
        raise NotImplementedError()

    def render(self):
        raise NotImplementedError()

