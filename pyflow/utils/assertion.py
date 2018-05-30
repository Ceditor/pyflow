from utils.safe_eval import safe_eval


class Assertion:
    def __init__(self, operator: str, left, right):
        self.operator = operator
        self.left = left
        self.right = right
        self.compare_operators = {
            "=": assert_equal,
            "@": assert_in,
            "%": assert_include,
            ">": assert_larger,
            "<": assert_smaller
        }
        self.logic_operators = {
            "!": assert_not,
            "|": assert_or,
            "&": assert_and
        }

    def do_assert(self):
        left_value = safe_eval(self.left)
        right_value = safe_eval(self.right)
        operations = []
        for operator in self.operator:
            if operator in self.compare_operators:
                operations.append(self.compare_operators[operator])



def assert_equal(left, right):
    return left == right


def assert_in(left, right):
    if hasattr(right, '__iter__'):
        return left in right
    else:
        return False


def assert_include(left, right):
    if hasattr(left, '__iter__') and hasattr(right, '__iter__'):
        for item in left:
            if item not in right:
                return False
        return True
    else:
        return False


def assert_larger(left, right):
    return left > right


def assert_smaller(left, right):
    return not (assert_equal(left, right) or assert_larger(left, right))


def assert_or(func1, func2, left, right):
    return func1(left, right) or func2(left, right)


def assert_not(func1, left, right):
    return not func1(left, right)


def assert_and(func1, func2, left, right):
    return func1(left, right) and func2(left, right)
