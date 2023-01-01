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
        the_print(_eval(d, env), end="")
    the_print()


def lit(data, env):
    return data[0]


def serialize(data, env):
    return env["_json_dumps"](_eval(data[0], env))


def deserialize(data, env):
    return env["_json_loads"](_eval(data[0], env))


def plus(data, env):
    return sum(_eval(d, env) for d in data)


def not_(data, env):
    return not _eval(data[0], env)


def type_(data, env):
    return type(_eval(data[0], env)).__name__


def any_(data, env):
    return any(_eval(d, env) for d in data)


def all_(data, env):
    return all(_eval(d, env) for d in data)


def apply(data, env):
    func, *params = data
    print(f"{func} {params}")
    func_def = _eval(func, env)
    new_env = env
    if isinstance(func_def, dict):
        if len(func_def[""][0]) == 1 and len(params) == 0:
            func_to_call = func_def
        else:
            if len(func_def[""][0]) > len(params):
                print("!!!!", func_def[""][0], params)
            args = {k: v for (k, v) in zip(func_def[""][0], params)}
            new_env = ChainMap(args, env)
            func_to_call = lambda d, e: _eval([_eval(dd, new_env) for dd in func_def[""][1:]], new_env)
    else:
        func_to_call = func_def
    if callable(func_to_call):
        result = func_to_call(params, new_env)
    else:
        result = func_to_call
    return result


def _eval(data, env):
    result = env["eval"](data, env)
    return result


def eval(data, env):
    if isinstance(data, list):
        return env["apply"](data, env)
    if isinstance(data, str):
        return _eval(env.get(data), env)  # data from variable
    return data


def lambda_(data, env):
    return {
        "": [data[0], _eval(data[1], env)]
    }


builtin_functions = {
    "lit": lit,
    "print": println,
    "type": type_,
    "_print": print,
    "_json_loads": json.loads,
    "_json_dumps": json.dumps,
    "deserialize": deserialize,
    "serialize": serialize,
    "+": plus,
    "apply": apply,
    "eval": eval,
    "lambda": lambda_,
    "not": not_,
    "any": any_,
    "all": all_,
}


def interpret_main(data, env):
    if not isinstance(data, dict):
        return data
    func_body = data.get("")
    if func_body is None:
        return data  # ???
    new_env = ChainMap(data, env)
    return _eval(func_body, new_env)


def main(contents):
    return interpret_main(contents, builtin_functions)


if __name__ == '__main__':
    import sys

    parser = argparse.ArgumentParser(description="__doc__")
    parser.add_argument('infile', nargs='?', type=str, default=sys.stdin)
    args = parser.parse_args()
    with open(args.infile, 'rb') as json_file:
        result = main(json.load(json_file))
        print(json.dumps(result, indent=2))
