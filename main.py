#!/usr/bin/env python3

import npuzzle
import search

def print_usage():
    print("DOWN: "+str(npuzzle.DOWN))
    print("UP: "+str(npuzzle.UP))
    print("RIGHT: "+str(npuzzle.RIGHT))
    print("LEFT: "+str(npuzzle.LEFT))
    print("exit: -1")

def main():
    env = npuzzle.NPuzzle(4, seed=42)
    env.render()
    print("---")
    search.rta(env,
            npuzzle.ManhattanDistanceHeuristic(False),
            npuzzle.NPuzzleBoard.done,
            15)
    # for la in range(1,20):
        # mm = search.minimin(env.state(),
            # npuzzle.ManhattanDistanceHeuristic(False),
            # npuzzle.NPuzzleBoard.done,
            # la)
        # print(mm)
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

