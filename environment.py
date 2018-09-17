import random

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

    def steps(self):
        raise NotImplementedError()


class State:

    def __hash__(self):
        raise NotImplementedError()

    def __eq__(self, other):
        raise NotImplementedError()

    def __lt__(self, other):
        raise NotImplementedError()

    def successor(self, action):
        raise NotImplementedError()

    def successors(self):
        successors = []
        for a in self.actions():
            succ = self.successor(a)
            if succ is not None:
                successors.append((a, succ))
        return successors

    def actions(self):
        raise NotImplementedError()

    def render(self):
        raise NotImplementedError()


class Heuristic:

    def __init__(self, cached=False):
        if cached:
            self._cache = {}

    def heuristic(self, state):
        raise NotImplementedError()

    def __call__(self, state):
        try:
            h = self._cache[state]
        except AttributeError:
            h = self.heuristic(state)
        except KeyError:
            h = self.heuristic(state)
            self._cache[state] = h
        return h


def random_walk(state, random_walk_length, repeat=False, rng=None):
    rng = rng or random.Random()
    if not repeat:
        visited = set([state])
    for _ in range(random_walk_length):
        succ = state.successors()
        if not repeat:
            succ = [s for _, s in succ if s not in visited]
        if not succ:
            break
        state = rng.sample(succ, 1)[0]
        if not repeat:
            visited.add(state)
    return state

