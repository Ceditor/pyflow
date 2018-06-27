from utils.style import StepConfig
from celery_worker.celery_tasks import run_workflow

read_step = StepConfig(name="read_csv", module_name="pandas",
                       func_name="read_csv",
                       param_list=[],
                       param_map={
                           "filepath_or_buffer": "source_file"},
                       result_name="data",
                       assertion={"left": "True", "operator": "=",
                                  "right": "True"})

prepare_data = '''def prepare_data(data, settings):
    ignored_cols = settings['ignored_cols']
    ignored_cols.append(settings['target'])
    cols = [c for c in data.columns if c not in ignored_cols]

    X = data.ix[:, cols]
    y = data[settings['target']]
    return {"X": X, "y": y}'''

prepare_step = StepConfig(name="prepare_data",
                          module_name='utils.func_wrapper',
                          func_name="wrap_self_define_func",
                          param_list=[],
                          param_map={"func": "prepare_data",
                                     "data": "data",
                                     "settings": "settings"},
                          result_name="raw_data",
                          assertion={"left": "True", "operator": "=",
                                     "right": "True"})

split_step = StepConfig(name="split_data",
                        module_name="sklearn.model_selection",
                        func_name="train_test_split",
                        param_list=["raw_data['X']", "raw_data['y']"],
                        param_map={},
                        result_name="splited_data",
                        assertion={"left": "True", "operator": "=",
                                   "right": "True"})

init_clf_step = StepConfig(name="init_clf", module_name="sklearn.ensemble",
                           func_name="RandomForestClassifier", param_list=[],
                           param_map={
                               "max_depth": "max_depth",
                               "random_state": "random_state"
                           },
                           result_name="clf",
                           assertion={"left": "True", "operator": "=",
                                      "right": "True"})

fit_and_predict = '''
def fit_clf(clf, X_train, y_train, X_test):
    clf.fit(X_train, y_train)
    prob_y = clf.predict_proba(X_test)
    return prob_y[:, 1]
    '''

fit_clf_step = StepConfig(name="fit_clf", module_name='utils.func_wrapper',
                          func_name="wrap_self_define_func", param_list=[],
                          param_map={"func": "fit_and_predict",
                                     "clf": "clf",
                                     "X_train": "splited_data[0]",
                                     "y_train": "splited_data[2]",
                                     "X_test": "splited_data[1]"},
                          result_name="prob_y",
                          assertion={"left": "True", "operator": "=",
                                     "right": "True"})

evaluation_step = StepConfig(name="evaluation", module_name="sklearn.metrics",
                             func_name="roc_auc_score", param_list=[],
                             param_map={
                                 "y_true": "splited_data[3]",
                                 "y_score": "prob_y"},
                             result_name="auc_score",
                             assertion={"left": "True", "operator": "=",
                                        "right": "True"})
steps = [read_step.serialize(), prepare_step.serialize(),
         split_step.serialize(), init_clf_step.serialize(),
         fit_clf_step.serialize(),
         evaluation_step.serialize()]

config = {
    "steps": steps,
    "first_step": read_step.name,
    "schema": {
        read_step.name: {
            True: prepare_step.name
        },

        prepare_step.name: {
            True: split_step.name
        },

        split_step.name: {
            True: init_clf_step.name
        },

        init_clf_step.name: {
            True: fit_clf_step.name
        },

        fit_clf_step.name: {
            True: evaluation_step.name
        },
        evaluation_step.name: {
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
res = run_workflow(config, init_data)
print(res['auc_score'])
