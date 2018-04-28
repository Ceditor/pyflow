from celery import Celery
from workflow import Workflow
from datapool import Datapool

app = Celery(broker='redis://127.0.0.1:6379')
app.config_from_object('celery_worker.celery_config')


@app.task(serializer='msgpack')
def run_workflow(workflow_config, schema_config, init_data):
    workflow = Workflow(workflow_config, schema_config)
    datapool = Datapool(init_data)
    workflow.run(datapool)
    return datapool.pool
