import importlib
from datapool import Datapool


class Step:
    def __init__(self, name: str, module_name: str, func_name: str,
                 param_map: dict, param_list: list,
                 result_name: list, condition: dict):
        self.name = name
        if module_name:
            module = importlib.import_module(module_name)
            self.func = getattr(module, func_name)
        else:
            self.func = eval(func_name)
        self.param_map = param_map
        self.param_list = param_list
        self.result_name = result_name
        self.status = None
        self.condition = condition

    def run(self, datapool: Datapool):
        args = self._parse_param_list(datapool)
        kwargs = self._parse_param_map(datapool)

        result = self.func(*args, **kwargs)
        datapool.set(self.result_name, result)

        self.status = self.check_condition(datapool)

    def check_condition(self, datapool: Datapool):
        params = self.condition['params']
        local_params = {param: datapool.get(param) for param in params}
        return eval(self.condition['func'], local_params)

    def _parse_param_map(self, datapool: Datapool):
        params = {}
        for param_name in self.param_map:
            if self.param_map[param_name].get("key"):
                params[param_name] = \
                    datapool.get(self.param_map[param_name]["name"])[
                        self.param_map[param_name]["key"]]
            else:
                params[param_name] = datapool.get(
                    self.param_map[param_name]["name"])
        return params

    def _parse_param_list(self, datapool: Datapool):
        params = []
        for param in self.param_list:
            if param.get("key"):
                params.append(datapool.get(param['name'])['key'])
            else:
                params.append(datapool.get(param['name']))
        return params
