import inspect
import pyopencl as cl
import sys
import utils

from platform_list import PlatformList

def cliloop(obj):
    stack = []
    while True:
        obj.enter()
        max_index = obj.list()
        if max_index == -1:
            user_input = input("(0 for back, -1 for exit)")
        else:
            user_input = input("{0} (1 ~ {1}, 0 for back, -1 for exit): ".format(obj.prompt(),
                                                                                 max_index))

        if user_input == "-1":
            break
        elif user_input == "0":
            if len(stack) == 0:
                break
            else:
                obj = stack.pop()
                continue

        try:
            user_index = int(user_input)
        except:
            continue

        if user_index <= max_index:
            next_obj = obj.choose(user_index - 1)
            if next_obj is not None:
                stack.append(obj);
                obj = next_obj


def main():
    cliloop(PlatformList())

if __name__ == '__main__':
    main()
