# -*- coding: utf-8 -*-
"""Run-time
"""
import argparse
import json


def println(data, env):
    for d in data:
        env["builtins"]["_print"](interpret(d, env), end="")
    env["builtins"]["_print"]()


builtin_functions = {
    "print": println,
    "_print": print,
}


def interpret_list(data, env):
    builtins = env.get("builtins", {})
    func = builtins.get(data[0])
    if func is not None:
        return func(data[1:], env)
    return data


def interpret(data, env):
    if not isinstance(data, dict) or data.get("") is None:
        return data
    if isinstance(data.get(""), list):
        return interpret_list(data.get(""), env)
    return data


def main(filename):
    with open(filename, 'rb') as json_file:
        contents = json.load(json_file)
    result = interpret(contents, {"builtins": builtin_functions})
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    import sys

    parser = argparse.ArgumentParser(description="__doc__")
    parser.add_argument('infile', nargs='?', type=str, default=sys.stdin)
    args = parser.parse_args()
    main(args.infile)
