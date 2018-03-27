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
        self.schema = schema_config

    def execute(self, datapool: Datapool):
        step_name = self.schema['first_step']
        while step_name:
            current_step = self.steps[step_name]
            self.steps[step_name].run(datapool)
            step_name = self.schema[current_step.name][current_step.status]


if __name__ == "__main__":
    def double2(alist):
        return [i * 2 for i in alist]


    configs = [
        {
            "name": "step1",
            "module_name": "",
            "func_name": "max",
            "param_map": {
                "raw_list": "alist"
            },
            "result_params": ["blist"],
            "condition": {"params": [], "func": "True"}
        }
    ]
