# -*- coding: utf-8 -*-
"""Run-time
"""
import argparse
import json


def get_builtin(env, key):
    return env["builtins"][key]


def println(data, env):
    the_print = get_builtin(env, "_print")
    for d in data:
        the_print(interpret(d, env), end="")
    the_print()


def serialize(data, env):
    return get_builtin(env, "_json_dumps")(data[0])


def deserialize(data, env):
    return get_builtin(env, "_json_loads")(data[0])


builtin_functions = {
    "print": println,
    "_print": print,
    "_json_loads": json.loads,
    "_json_dumps": json.dumps,
    "deserialize": deserialize,
    "serialize": serialize,
}


def interpret_list(data, env):
    builtins = env.get("builtins", {})
    func = builtins.get(data[0])
    if func is not None:
        return func(data[1:], env)
    return data


def interpret(data, env):
    if isinstance(data, list):
        return interpret_list(data, env)
    return data


def interpret_main(data, env):
    if not isinstance(data, dict) or data.get("") is None:
        return data
    return interpret(data.get(""), env)


def main(filename):
    with open(filename, 'rb') as json_file:
        contents = json.load(json_file)
    result = interpret_main(contents, {"builtins": builtin_functions})
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    import sys

    parser = argparse.ArgumentParser(description="__doc__")
    parser.add_argument('infile', nargs='?', type=str, default=sys.stdin)
    args = parser.parse_args()
    main(args.infile)
