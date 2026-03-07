import os
import shutil
import yaml
import json
import functools
import inspect
from argparse import Namespace

def read_lines(f):
    with open(f) as inf:
        lines = [l.rstrip() for l in inf.readlines()]
    return lines

def write_lines(lines, f):
    with open(f, "w") as outf:
        outf.write("\n".join(lines) + "\n")

def read_content(f):
    with open(f) as inf:
        content = inf.read()
    return content

def write_content(content, f):
    with open(f, "w") as outf:
        outf.write(content)

def read_json(f):
    with open(f) as inf:
        data = json.load(inf)
    return data

def write_json(data:dict, f, indent=2, ensure_ascii=True):
    with open(f, "w") as outf:
        outf.write(json.dumps(data, indent=indent, ensure_ascii=ensure_ascii))

def read_yaml(f):
    with open(f) as inf:
        config = yaml.safe_load(inf)
    return config

def create_directory(d, destroy=True):
    if destroy:
        if os.path.exists(d):
            print(f"DELETING: {d}")
            shutil.rmtree(d)
    print(f"CREATING: {d}")
    os.makedirs(d, exist_ok=True)

def log_function_call(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        print(f"\n---------------- Calling {f.__name__} ----------------")
        
        # Get parameter names from the function signature
        sig = inspect.signature(f)
        bound = sig.bind(*args, **kwargs)  # Map args and kwargs to parameter names
        bound.apply_defaults()             # Fill in default values

        for name, value in bound.arguments.items():
            if isinstance(value, str):
                value = f'"{value}"'
            print(f"-{name}={value} ({type(value)})")
        print("\n")

        result = f(*args, **kwargs)
        print(f"---------------- Ending {f.__name__} -----------------\n")
        return result
    return wrapper

def read_lines_from_path_args(f):
    @functools.wraps(f)
    def wrapper(*args):
        args = [read_lines(a) for a in args if isinstance(a, str) and a.endswith(".txt") and os.path.exists(a)]
        result = f(*args)
        return result
    return wrapper

def log_python_script(package, name):
    name = name.split("/")[-1]
    name = f"{name}.py"
    if package and package.strip() != "":
        name = f"{package}.{name}"
    name = f"## {name} ##"
    border = "#" * len(name)
    print("\n".join([border, name, border]))

def log_parsed_args(f):
    def wrapper():
        args = f()
        if not isinstance(args, Namespace):
            raise ValueError(f"To use log_parsed_args decorator, function must return object type argparse.Namespace.")
        print("Arguments:")
        for arg, value in vars(args).items():
            print(f"\t-{arg}=`{value}` ({type(value)})")
        return args
    return wrapper

