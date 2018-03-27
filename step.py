import importlib
from datapool import Datapool


class Step:
    def __init__(self, module_name: str, func_name: str, param_names: list,
                 result_names: list):
        if module_name:
            module = importlib.import_module(module_name)
            self.func = getattr(module, func_name)
        else:
            self.func = eval(func_name)
        self.param_names = param_names
        self.result_names = result_names

    def run(self, datapool: Datapool):
        params = {param_name: datapool.get(param_name) for param_name in
                  self.param_names}
        results = self.func(**params)
        for index, result_name in enumerate(self.result_names):
            datapool.set(result_name, results[index])
