import time

def minimin(state, heur, goal, lookahead, order=False, stats=False):
    start = time.clock()
    generated_nodes = 0
    if lookahead == 0 or goal(state):
        f_min = heur(state)
    else:
        f_min = float('inf')
        stack = [(0, state)]
        while stack:
            g, top = stack.pop()
            successors = []
            for _, succ in top.successors():
                h = heur(succ)
                successors.append((g+1+h, h, succ))
            if order:
                successors.sort(key=lambda t: t[:2], reverse=True)
            generated_nodes += len(successors)
            for f_succ, h_succ, successor in successors:
                g_succ = f_succ - h_succ
                if f_succ >= f_min:
                    continue
                elif goal(successor) or g_succ == lookahead:
                    f_min = f_succ
                else:
                    stack.append((g_succ, successor))
    elapsed = time.clock() - start
    if stats:
        return f_min, generated_nodes, elapsed
    else:
        return f_min


def astar(state, heur, goal, lookahead):
    pass

# def minimin(state, heur, goal, lookahead, g=0, alpha=float('inf')):
    # if lookahead == 0 or goal(state):
        # return min(alpha, g + heur(state))
    # for _, successor in state.successors():
        # f = g + 1 + heur(successor)
        # if f < alpha:
            # f_min = minimin(successor, heur, goal, lookahead-1, g+1, alpha)
            # alpha = min(f_min, alpha)
    # return alpha


class Rta:

    def __init__(self, heur, goal, lookahead, learn=False):
        self._learn = learn
        self._cache = {}
        self._heur = heur
        self._goal = goal
        self._lookahead = lookahead

    def reset(self):
        self._cache = {}

    def step(self, env):
        state = env.state()
        if env.done():
            return None
        best = None
        second_best = None
        for action, successor in state.successors():
            try:
                h = self._cache[successor]
            except KeyError:
                h = minimin(successor, self._heur, self._goal, self._lookahead)
            f = 1 + h
            if best is None or f < best[0]:
                second_best = best
                best = (f, action)
            elif second_best is None or f < second_best[0]:
                second_best = (f, action)
            if best is None:
                raise Exception("reached dead end")
            if self._learn or second_best is None:
                self._cache[state] = best[0]
            else:
                self._cache[state] = second_best[0]
        return env.step(best[1])

    def __call__(self, env, timeout=float('inf'), stats=False):
        timeout = timeout/1000
        start = time.clock()
        elapsed = 0
        done = env.done()
        while not env.done() and elapsed < timeout:
            done = self.step(env)
            elapsed = time.clock() - start
        if stats:
            return done, elapsed
        else:
            return done

