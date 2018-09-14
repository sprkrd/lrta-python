#!/usr/bin/env python3

import npuzzle
import search

import matplotlib.pyplot as plt

from tqdm import tqdm

def print_usage():
    print("DOWN: "+str(npuzzle.DOWN))
    print("UP: "+str(npuzzle.UP))
    print("RIGHT: "+str(npuzzle.RIGHT))
    print("LEFT: "+str(npuzzle.LEFT))
    print("exit: -1")


def average_results(n1sqrt, lookahead, N):
    heur = npuzzle.ManhattanDistanceHeuristic(False)
    goal = npuzzle.NPuzzleBoard.done
    rta = search.Rta(heur=heur, goal=goal, lookahead=lookahead, learn=False)
    steps_sum = 0
    elapsed_sum = 0
    for seed in tqdm(range(N)):
        rta.reset()
        env = npuzzle.NPuzzle(n1sqrt=n1sqrt, difficulty=0.5, seed=seed)
        done, elapsed = rta(env, stats=True)
        steps_sum += env.steps()
        elapsed_sum += elapsed
    return steps_sum/N, elapsed_sum/N


def do():
    LA = 21
    la = list(range(LA))
    avgs = [0]*LA
    avge = [0]*LA
    for lookahead in range(LA):
        print("lookahead", lookahead)
        avg_steps, avg_elapsed = average_results(3, lookahead, 1000)
        avgs[lookahead] = avg_steps
        avge[lookahead] = avg_elapsed
    plt.subplot(2,1,1)
    plt.plot(la, avgs)
    plt.subplot(2,1,2)
    plt.plot(la, avge)
    plt.show()


def main():
    do()
    # env = npuzzle.NPuzzle(4)
    # env = npuzzle.NPuzzle(n1sqrt=4, difficulty=0.5, seed=100)
    # env.render()
    # rta = search.Rta(heur=npuzzle.ManhattanDistanceHeuristic(False),
            # goal=npuzzle.NPuzzleBoard.done,
            # lookahead=1,
            # learn=False) 
    # for _ in range(1):
        # done, elapsed = rta(env, timeout=60000, stats=True)
        # if done:
            # print("Done in {} step(s) ({:.1f}ms)!".format(env.steps(), 1000*elapsed))
        # else:
            # print("time-out after {} step(s)! ({:.1f}ms)".format(env.steps(), 1000*elapsed))
        # env.reset()
    # while not env.done():
        # print("---")
        # rta.step(env)
        # env.render()
    # print("done in {} step(s)!".format(env.steps()))
    # for la in range(26):
        # mm1, gn1, el1 = search.minimin(env.state(),
            # npuzzle.ManhattanDistanceHeuristic(False),
            # npuzzle.NPuzzleBoard.done,
            # la, stats=True)
        # mm2, gn2, el2 = search.minimin(env.state(),
            # npuzzle.ManhattanDistanceHeuristic(False),
            # npuzzle.NPuzzleBoard.done,
            # la, order=True, stats=True)
        # print("la: {}".format(la))
        # print("mm1: {}, gn1: {}, el1: {}s".format(mm1, gn1, el1))
        # print("mm2: {}, gn2: {}, el2: {}s".format(mm2, gn2, el2))
        # print("---")
        # mm1 = search.minimin(env.state(),
            # npuzzle.ManhattanDistanceHeuristic(False),
            # npuzzle.NPuzzleBoard.done,
            # la)
        # print("la: {}".format(la))
        # print("mm1: {}".format(mm1))
        # print("---")
    # while True:
        # print_usage()
        # cmd = int(input("Cmd: "))
        # if cmd == -1:
            # break
        # done = env.step(cmd)
        # env.render()
        # if done:
            # print("Done!")
            # break

if __name__ == "__main__":
    main()

