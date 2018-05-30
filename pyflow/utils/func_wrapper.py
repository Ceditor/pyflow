import types


def wrap_self_define_func(func, modules, **params):
    func_list = {}
    exec(func, modules, func_list)
    func_list


def wrap_python_file(file_name, modules, **params):
    with open(file_name, 'r') as f:
        func_str = f.read()
    return wrap_self_define_func(func_str, modules, **params)
