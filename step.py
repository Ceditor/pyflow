import importlib
from datapool import Datapool


class Step:
    def __init__(self, name: str, module_name: str, func_name: str,
                 param_map: dict,
                 result_names: list, condition: dict):
        self.name = name
        if module_name:
            module = importlib.import_module(module_name)
            self.func = getattr(module, func_name)
        else:
            self.func = eval(func_name)
        self.param_map = param_map
        self.result_names = result_names
        self.status = None
        self.condition = condition

    def run(self, datapool: Datapool):

        params = {self.param_map[data_name]: datapool.get(data_name) for
                  data_name in self.param_map}
        results = self.func(**params)
        for index, result_name in enumerate(self.result_names):
            datapool.set(result_name, results[index])

        self.status = self.check_condition(datapool)

    def check_condition(self, datapool: Datapool):
        params = self.condition['params']
        local_params = {param: datapool.get(param) for param in params}
        return eval(self.condition['func'], local_params)
