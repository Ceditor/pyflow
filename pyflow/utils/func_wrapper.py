import types


def wrap_self_define_func(func, **params):
    func_module = compile(func, '', 'exec')
    func_code = [c for c in func_module.co_consts if
                 isinstance(c, types.CodeType)][0]
    func = types.FunctionType(func_code, globals())
    return func(**params)


def wrap_python_file(file_name, modules, **params):
    with open(file_name, 'r') as f:
        func_str = f.read()
    return wrap_self_define_func(func_str, **params)
