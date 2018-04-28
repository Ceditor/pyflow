from datapool import Datapool
from step import Step
import logging
from celery import Celery

app = Celery(broker='redis://127.0.0.1:6379')
app.config_from_object('celeryconfig')


class Workflow:
    def __init__(self, configs: list, schema_config: dict):
        self.steps = {}
        for config in configs:
            self.steps[config['name']] = Step(**config)
        self.schema = schema_config['schema']
        self.first_step = schema_config['first_step']

    def execute(self, datapool: Datapool):
        step_name = self.first_step
        while step_name:
            current_step = self.steps[step_name]
            self.steps[step_name].run(datapool)
            step_name = self.schema[current_step.name][current_step.status]


@app.task(serializer='msgpack')
def celery_task(workflow_config, schema_config, init_data):
    schema = schema_config["schema"]
    logging.info(type(list(schema["step1"].keys())[0]))
    logging.info(schema_config)
    logging.info(type(schema_config))
    workflow = Workflow(workflow_config, schema_config)
    datapool = Datapool(init_data)
    workflow.execute(datapool)
    return datapool.pool
