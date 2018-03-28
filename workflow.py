from datapool import Datapool
from step import Step

'''
config:
{
    "name": "step1",
    "module_name": "pandas",
    "func_name": "read_csv",
    "param_names":{"file_name": "filepath_or_buffer"}
}
'''


class Workflow:
    def __init__(self, configs: list, schema_config: dict):
        self.steps = {}
        for config in configs:
            self.steps[config['name']] = Step(**config)
        self.schema = schema_config['schema']
        self.first_step = schema['first_step']

    def execute(self, datapool: Datapool):
        step_name = self.first_step
        while step_name:
            current_step = self.steps[step_name]
            self.steps[step_name].run(datapool)
            step_name = self.schema[current_step.name][current_step.status]


if __name__ == "__main__":
    configs = [
        {
            "name": "step1",
            "module_name": "test_func",
            "func_name": "double2",
            "param_map": {
                "alist": "raw_list1"
            },
            "result_name": "raw_list1",
            "condition": {"params": [], "func": "True"}
        },
        {
            "name": "step2",
            "module_name": "utils.func_wrapper",
            "func_name": "wrap_arg_func",
            "param_map": {
                "params": "raw_list1",
                "func": "max"
            },
            "result_name": "max1",
            "condition": {"params": ["max1", "max2"], "func": "max1 > max2"}
        },
        {
            "name": "step3",
            "module_name": "utils.func_wrapper",
            "func_name": "wrap_arg_func",
            "param_map": {
                "params": "raw_list2",
                "func": "max"
            },
            "result_name": "max2",
            "condition": {"params": [], "func": "True"}
        },
    ]

    schema = {
        "first_step": "step3",
        "schema": {
            "step1": {
                True: "step2"
            },
            "step2": {
                True: None,
                False: "step1"
            },
            "step3": {
                True: "step2"
            }
        }
    }
    workflow = Workflow(configs, schema)
    datapool = Datapool(
        **{"raw_list1": [1, 2, 3], "raw_list2": [8, 9, 10], "max": max})
    workflow.execute(datapool)
    print(datapool.pool)
