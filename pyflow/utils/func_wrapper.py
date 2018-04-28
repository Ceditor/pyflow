import types


def wrap_arg_func(func, params):
    func = eval(func)
    return func(*params)


def wrap_self_define_func(func, **params):
    func_module = compile(func, '', 'exec')
    func_code = \
        [c for c in func_module.co_consts if
         isinstance(c, types.CodeType)][0]
    func = types.FunctionType(func_code, globals())
    return func(**params)
