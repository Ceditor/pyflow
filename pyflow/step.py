import importlib
from datapool import Datapool
from utils.assertion import do_assert
from utils.safe_eval import safe_eval
from utils.style import Assertion


class Step:
    def __init__(self, name: str, module_name: str, func_name: str,
                 param_map: dict, param_list: list,
                 result_name: list, assertion: dict):
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
        self.assertion = Assertion(**assertion)

    def run(self, datapool: Datapool):
        args = self._parse_param_list(datapool)
        kwargs = self._parse_param_map(datapool)

        result = self.func(*args, **kwargs)
        datapool.set(self.result_name, result)

        self.status = self.check_condition(datapool)

    def check_condition(self, datapool: Datapool):
        return do_assert(self.assertion, datapool.pool)

    def _parse_param_map(self, datapool: Datapool):
        params = {}
        for param_name in self.param_map:
            params[param_name] = safe_eval(self.param_map[param_name],
                                           datapool.pool)
        return params

    def _parse_param_list(self, datapool: Datapool):
        params = []
        for param in self.param_list:
            params.append(safe_eval(param, datapool.pool))
        return params
