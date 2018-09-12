#!/usr/bin/env python3

import npuzzle

def print_usage():
    print("DOWN: "+str(npuzzle.DOWN))
    print("UP: "+str(npuzzle.UP))
    print("RIGHT: "+str(npuzzle.RIGHT))
    print("LEFT: "+str(npuzzle.LEFT))
    print("exit: -1")

def main():
    env = npuzzle.NPuzzle(3)
    env.render()
    while True:
        print_usage()
        cmd = int(input("Cmd: "))
        if cmd == -1:
            break
        done = env.step(cmd)
        env.render()
        if done:
            print("Done!")
            break

if __name__ == "__main__":
    main()

