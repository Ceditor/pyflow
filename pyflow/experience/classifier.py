from workflow import celery_task
from utils.toolbox import build_step

read_step = build_step(name="read_csv", module_name="pandas",
                       func_name="read_csv",
                       param_list=[],
                       param_map={
                           "filepath_or_buffer": {"name": "source_file"}},
                       result_name="data",
                       condition={"params": [], "func": "True"})

prepare_data = '''def prepare_data(data, settings):
    ignored_cols = settings['ignored_cols']
    ignored_cols.append(settings['target'])
    cols = [c for c in data.columns if c not in ignored_cols]

    X = data.ix[:, cols]
    y = data[settings['target']]
    return {"X": X, "y": y}'''

prepare_step = build_step(name="prepare_data",
                          module_name='utils.func_wrapper',
                          func_name="wrap_self_define_func",
                          param_list=[],
                          param_map={"func": {"name": "prepare_data"},
                                     "data": {"name": "data"},
                                     "settings": {"name": "settings"}},
                          result_name="raw_data",
                          condition={"params": [], "func": "True"})

split_step = build_step(name="split_data",
                        module_name="sklearn.model_selection",
                        func_name="train_test_split",
                        param_list=[{"name": "raw_data", "key": "X"},
                                    {"name": "raw_data", "key": "y"}],
                        param_map={},
                        result_name="splited_data",
                        condition={"params": [], "func": "True"})

init_clf_step = build_step(name="init_clf", module_name="sklearn.ensemble",
                           func_name="RandomForestClassifier", param_list=[],
                           param_map={
                               "max_depth": {"name": "max_depth"},
                               "random_state": {"name": "random_state"}
                           },
                           result_name="clf",
                           condition={"params": [], "func": "True"})

fit_and_predict = '''
def fit_clf(clf, X_train, y_train, X_test):
    clf.fit(X_train, y_train)
    prob_y = clf.predict_proba(X_test)
    return prob_y[:, 1]
    '''

fit_clf_step = build_step(name="fit_clf", module_name='utils.func_wrapper',
                          func_name="wrap_self_define_func", param_list=[],
                          param_map={"func": {"name": "fit_and_predict"},
                                     "clf": {"name": "clf"},
                                     "X_train": {"name": "splited_data",
                                                 "key": 0},
                                     "y_train": {"name": "splited_data",
                                                 "key": 2},
                                     "X_test": {"name": "splited_data",
                                                "key": 1}},
                          result_name="prob_y",
                          condition={"params": [], "func": "True"})

evaluation_step = build_step(name="evaluation", module_name="sklearn.metrics",
                             func_name="roc_auc_score", param_list=[],
                             param_map={
                                 "y_true": {"name": "splited_data", "key": 3},
                                 "y_score": {"name": "prob_y"}},
                             result_name="auc_score",
                             condition={"params": [], "func": "True"})
configs = [read_step, prepare_step, split_step, init_clf_step, fit_clf_step,
           evaluation_step]

schema = {
    "first_step": read_step["name"],
    "schema": {
        read_step["name"]: {
            True: prepare_step["name"]
        },

        prepare_step["name"]: {
            True: split_step["name"]
        },

        split_step["name"]: {
            True: init_clf_step["name"]
        },

        init_clf_step["name"]: {
            True: fit_clf_step["name"]
        },

        fit_clf_step["name"]: {
            True: evaluation_step["name"]
        },
        evaluation_step["name"]: {
            True: None
        },
    }
}

init_data = {
    "source_file": "/home/chenyunfeng/classifier/higgs_train_10k.csv",
    "settings": {"target": "response", "ignored_cols": []}, "max_depth": 2,
    "random_state": 0,
    "prepare_data": prepare_data, "fit_and_predict": fit_and_predict}

# workflow = Workflow(configs, schema)
# datapool = Datapool(init_data)
# workflow.execute(datapool)
# print(datapool.get("auc_score"))
res = celery_task.apply_async((configs, schema, init_data))
print(res)