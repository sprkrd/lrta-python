#!/usr/bin/env python3

import os

import npuzzle
import search

import matplotlib.pyplot as plt

import pickle as pkl

from scoop import futures
from tqdm import tqdm


def print_usage():
    print("DOWN: "+str(npuzzle.DOWN))
    print("UP: "+str(npuzzle.UP))
    print("RIGHT: "+str(npuzzle.RIGHT))
    print("LEFT: "+str(npuzzle.LEFT))
    print("exit: -1")


def do_individual_experiment(args):
    n1sqrt, lookahead, seed = args
    heur = npuzzle.ManhattanDistanceHeuristic(False)
    goal = npuzzle.NPuzzleBoard.done
    rta = search.Rta(heur=heur, goal=goal, lookahead=lookahead, learn=False)
    env = npuzzle.NPuzzle(n1sqrt=n1sqrt, difficulty=0.5, seed=seed)
    done, elapsed = rta(env, stats=True)
    return env.steps(), elapsed


def average_results(n1sqrt, lookahead, N):
    results = futures.map(do_individual_experiment, [(n1sqrt, lookahead, seed) for seed in range(N)])
    results = list(results)
    avg_steps = sum(steps for steps,_ in results)/N
    avg_elapsed = sum(elapsed for _,elapsed in results)/N
    return avg_steps, avg_elapsed


def experiments():
    LA = 26
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212, sharex=ax1)
    if os.path.isfile("results.pkl"):
        print("Found results.pkl, resuming from checkpoint...")
        with open("results.pkl", "rb") as f:
            avgs, avge = pkl.load(f)
        start = len(avgs)
        if start > 2:
            la = list(range(start))
            ax1.plot(la, avgs)
            ax2.plot(la, avge)
            plt.pause(0.05)
    else:
        print("results.pkl not found, starting from scratch...")
        start = 0
        avgs = []
        avge = []
    for lookahead in tqdm(range(start, LA)):
        avg_steps, avg_elapsed = average_results(3, lookahead, 1000)
        avgs.append(avg_steps)
        avge.append(avg_elapsed)
        with open("results.pkl", "wb") as f:
            pkl.dump((avgs, avge), f)
        if lookahead > 0:
            la = list(range(lookahead+1))
            ax1.clear()
            ax2.clear()
            ax1.plot(la, avgs)
            ax2.plot(la, avge)
            plt.pause(0.05)
    plt.show()


def manual_play():
    env = npuzzle.NPuzzle(n1sqrt=4, difficulty=0.5)
    env.render()
    while True:
        print("---")
        print_usage()
        cmd = int(input("Cmd: "))
        if cmd == -1:
            break
        done = env.step(cmd)
        env.render()
        if done:
            print("done in {}!".format(env.steps()))
            break


def main():
    # manual_play()
    experiments()
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

