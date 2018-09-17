import heapq
import time

def minimin(state, heur, goal, lookahead, order=False, stats=False):
    start = time.time()
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
                successors.sort(reverse=True)
            generated_nodes += len(successors)
            for f_succ, h_succ, successor in successors:
                g_succ = f_succ - h_succ
                if f_succ >= f_min:
                    continue
                elif goal(successor) or g_succ == lookahead:
                    f_min = f_succ
                else:
                    stack.append((g_succ, successor))
    elapsed = time.time() - start
    if stats:
        return f_min, generated_nodes, elapsed
    else:
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


def reconstruct_path(tree, s):
    plan = []
    while s is not None:
        t = tree[s]
        if t is None:
            s = None
        else:
            a, s = t
            plan.append(a)
    plan.reverse()
    return plan


def astar(state, heur, goal, stats=False):
    start = time.time()
    inf = float('inf')
    h_state = heur(state)
    queue = [(h_state, h_state, state)]
    g_seen = {state: 0}
    tree = {state: None}
    plan = None
    generated_nodes = 0
    while queue:
        f_s, h_s, s = heapq.heappop(queue)
        if goal(s):
            plan = reconstruct_path(tree, s)
            break
        g_s = f_s - h_s
        successors = s.successors()
        generated_nodes += len(successors)
        for a, n in s.successors():
            g_n = g_s + 1
            g_n_prev = g_seen.get(n, inf)
            if g_n < g_n_prev:
                g_seen[n] = g_n
                h_n = heur(n)
                f_n = g_n + h_n
                tree[n] = (a, s)
                heapq.heappush(queue, (f_n, h_n, n))
    if stats:
        elapsed = time.time() - start
        return plan, generated_nodes, elapsed
    else:
        return plan


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
        start = time.time()
        elapsed = 0
        done = env.done()
        while not env.done() and elapsed < timeout:
            done = self.step(env)
            elapsed = time.time() - start
        if stats:
            return done, elapsed
        else:
            return done

