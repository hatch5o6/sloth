import os
import shutil
import yaml
import json
import functools

def read_lines(f):
    with open(f) as inf:
        lines = [l.rstrip() for l in inf.readlines()]
    return lines

def read_content(f):
    with open(f) as inf:
        content = inf.read()
    return content

def read_json(f):
    with open(f) as inf:
        data = json.load(inf)
    return data

def read_yaml(f):
    with open(f) as inf:
        config = yaml.safe_load(inf)
    return config

def log_function_call(f):
    @functools.wraps(f)
    def wrapper(**args):
        print(f"\n---------------- Calling {f.__name__} ----------------")
        for arg, value in args.items():
            print(f"\t{arg}=`{value}`")
        result = f(**args)
        print(f"\n---------------- Ending {f.__name__} ----------------")
        return result
    return wrapper

def create_directory(d, destroy=True):
    if destroy:
        if os.path.exists(d):
            print(f"DELETING: {d}")
            shutil.rmtree(d)
    print(f"CREATING: {d}")
        os.makedirs(d, exist_ok=True)
