from pyflow.datapool import Datapool
from pyflow.workflow import Workflow

double2 = '''def double2(alist):
    blist = [i * 2 for i in alist]
    print(blist)
    return blist
    '''
print(double2)

configs = [
    {
        "name": "step1",
        "module_name": "utils.func_wrapper",
        "func_name": "wrap_self_define_func",
        "param_map": {
            "alist": {"name": "raw_list1"},
            "func": {"name": "double2"}
        },
        "param_list": [],
        "result_name": "raw_list1",
        "condition": {"params": [], "func": "True"}
    },
    {
        "name": "step2",
        "module_name": "",
        "func_name": "max",
        "param_map": {},
        "param_list": [{"name": "raw_list1"}],
        "result_name": "max1",
        "condition": {"params": ["max1", "max2"], "func": "max1 > max2"}
    },
    {
        "name": "step3",
        "module_name": "",
        "func_name": "max",
        "param_map": {},
        "param_list": [{"name": "raw_list2"}],
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
init_data = {"raw_list1": [1, 2, 3], "raw_list2": [8, 9, 10], "max": "max",
             "double2": double2}
datapool = Datapool(
    init_data)
# res = celery_task.apply_async((configs, schema, init_data))
print(workflow.execute(datapool))
print(datapool.pool)
