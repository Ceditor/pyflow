import ast
import operator

binOps = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Mod: operator.mod,
    ast.Div: operator.truediv,
}


def safe_eval(expr, locals=None):
    if locals is None:
        locals = {}
    node = ast.parse(expr, mode='eval')

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Str):
            return node.s
        elif isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.Name):
            if node.id in locals:
                return locals[node.id]
            else:
                raise NameError("name '{0}' is not defined".format(node.id))
        elif isinstance(node, ast.BinOp):
            return binOps[type(node.op)](_eval(node.left), _eval(node.right))
        elif isinstance(node, ast.Subscript):
            return _eval(node.value)[_eval(node.slice)]
        elif isinstance(node, ast.Index):
            return _eval(node.value)
        elif isinstance(node, ast.Attribute):
            return getattr(_eval(node.value), node.attr)
        elif isinstance(node, ast.List):
            return [_eval(elt) for elt in node.elts]
        elif isinstance(node, ast.Dict):
            return {_eval(key): _eval(node.values[index]) for
                    index, key in enumerate(node.keys)}
        else:
            raise Exception('Unsupported type {}'.format(node))

    return _eval(node.body)
