from datapool import Datapool
from step import Step



class Workflow:
    def __init__(self, configs: list, schema_config: dict):
        self.steps = {}
        for config in configs:
            self.steps[config['name']] = Step(**config)
        self.schema = schema_config['schema']
        self.first_step = schema_config['first_step']

    def run(self, datapool: Datapool):
        step_name = self.first_step
        while step_name:
            current_step = self.steps[step_name]
            self.steps[step_name].run(datapool)
            step_name = self.schema[current_step.name][current_step.status]


