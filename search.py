
def minimin(state, heur, goal, lookahead):
    if lookahead == 0 or goal(state):
        return heur(state)
    stack = [(0, state)]
    f_min = float('inf')
    while stack:
        g, top = stack.pop()
        # successors = []
        # for _, succ in top.successors():
            # h = heur(succ)
            # successors.append((g+1+h, h, succ))
        # successors.sort(key=lambda t: t[:2], reverse=True)
        # for f_succ, h_succ, successor in successors:
            # g_succ = f_succ - h_succ
        for _, successor in top.successors():
            g_succ = g + 1
            f_succ = g_succ + heur(successor)
            if f_succ >= f_min:
                continue
            elif goal(successor) or g_succ == lookahead:
                f_min = f_succ
            else:
                stack.append((g_succ, successor))
    return f_min

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

    def __init__(self, heur, goal, lookahead, lrta=False):
        self._lrta = lrta
        self._cache = {}
        self._heur = heur
        self._goal = goal
        self._lookahead = lookahead
        self._solution_len = 0

    def reset(self):
        self._cache = {}

    def step(self, env):
        current = env.state()
        if not self._goal(current):
            best = (float('inf'), None)
            second_best = (float('inf'), None)
            for action, successor in current.successors():
                try:
                    h = self._cache[successor]
                except KeyError:
                    h = minimin(successor, self._heur, self._goal, self._lookahead)
                f = 1 + h
                if f < best[0]:
                    second_best = best
                    best = (f, action)
                elif f < second_best[0]:
                    second_best = (f, action)
                if best[1] is None:
                    raise Exception("dead end")
                if self._lrta or second_best[1] is None:
                    cache[current] = best[0]
                else:
                    cache[current] = second_best[0]
                env.step(best[1])


def rta(env, heur, goal, lookahead):
    cache = {}
    current = env.state()
    while not goal(current):
        best = None
        second_best = None
        for action, successor in current.successors():
            try:
                h = cache[successor]
            except KeyError:
                h = minimin(successor, heur, goal, lookahead)
            f = 1 + h
            if best is None or f < best[0]:
                second_best = best
                best = (f, action)
            elif second_best is None or f < second_best[0]:
                second_best = (f, action)
        if best is None:
            raise Exception("No candidate node")
        cache[current] = best[0] if second_best is None else second_best[0]
        env.step(best[1])
        current = env.state()
        env.render()
        print("---")


