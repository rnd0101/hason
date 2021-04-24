# -*- coding: utf-8 -*-
"""Run-time
"""
import argparse
import json
import yaml
from collections import ChainMap


def println(data, env):
    the_print = env["_print"]
    for d in data:
        the_print(eval(d, env), end="")
    the_print()


def lit(data, env):
    return data


def serialize(data, env):
    return env["_json_dumps"](data[0])


def deserialize(data, env):
    return env["_json_loads"](data[0])


builtin_functions = {
    "lit": lit,
    "print": println,
    "_print": print,
    "_json_loads": json.loads,
    "_json_dumps": json.dumps,
    "deserialize": deserialize,
    "serialize": serialize,
}


def apply(func, params, env):
    func = eval(func, env)   # env.get(data[0])
    if func is not None:
        return func(params, env)
    return [func] + params


def eval(data, env):
    if isinstance(data, list):
        return apply(data[0], data[1:], env)
    return data


def interpret_main(data, env):
    if not isinstance(data, dict):
        return data
    func_body = data.get("")
    if func_body is None:
        return data   #???
    new_env = ChainMap(data, env)
    return eval(func_body, new_env)


def main(filename):
    with open(filename, 'rb') as json_file:
        contents = json.load(json_file)
    result = interpret_main(contents, builtin_functions)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    import sys

    parser = argparse.ArgumentParser(description="__doc__")
    parser.add_argument('infile', nargs='?', type=str, default=sys.stdin)
    args = parser.parse_args()
    main(args.infile)
