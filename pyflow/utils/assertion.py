from utils.safe_eval import safe_eval
from utils.style import Assertion


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
    return left < right


compare_operators = {
    "=": assert_equal,
    "@": assert_in,
    "%": assert_include,
    ">": assert_larger,
    "<": assert_smaller
}


def do_assert(assertion: Assertion, param=None) -> bool:
    left_value = safe_eval(assertion.left, param)
    right_value = safe_eval(assertion.right, param)
    operator = assertion.operator
    if operator in compare_operators:
        return compare_operators[operator](left_value,
                                           right_value)
    elif operator.startswith('!'):
        if operator[1] in compare_operators:
            return not (compare_operators[operator[1]](left_value,
                                                       right_value))


if __name__ == "__main__":
    assertion = Assertion('[1]', '[[1],2]', '@')
    print(do_assert(assertion))
