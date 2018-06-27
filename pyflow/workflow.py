from datapool import Datapool
from step import Step


class Workflow:
    def __init__(self, config: dict):
        self.steps = {}
        for step in config['steps']:
            self.steps[step['name']] = Step(**step)
        self.schema = config['schema']
        self.first_step = config['first_step']

    def run(self, datapool: Datapool):
        step_name = self.first_step
        while step_name:
            current_step = self.steps[step_name]
            self.steps[step_name].run(datapool)
            step_name = self.schema[current_step.name][current_step.status]
