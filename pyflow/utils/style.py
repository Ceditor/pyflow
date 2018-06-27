class Style:

    def serialize(self):
        return self.__dict__

    def deserialize(self, dict):
        for field in self.__dict__:
            self.__dict__[field] = dict.get(field)


class Assertion(Style):
    def __init__(self, left: str, right: str, operator: str):
        self.left = left
        self.right = right
        self.operator = operator


class StepConfig(Style):
    def __init__(self, name: str, module_name: str, func_name: str,
                 param_list: list, param_map: dict, result_name: str,
                 assertion: dict):
        self.name = name
        self.module_name = module_name
        self.func_name = func_name
        self.param_list = param_list
        self.param_map = param_map
        self.result_name = result_name
        self.assertion = assertion
