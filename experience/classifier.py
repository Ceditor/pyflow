import pandas

from utils.toolbox import build_step

read_step = build_step(name="read_csv", module_name="pandas",
                       func_name="read_csv",
                       param_map={"filepath_or_buffer": "source_file"},
                       result_name="data",
                       condition={"params": [], "func": "True"})

prepare_data = '''def prepare_data(data, settings):
    ignored_cols = settings['ignored_cols']
    ignored_cols.append(settings['target'])
    cols = [c for c in data.columns if c not in ignored_cols]

    X = data.ix[:, cols]
    y = data[settings['target']]
    return {"X": X, "y": y}'''

prepare_step = build_step(name="prepare_data", module_name='',
                          func_name="prepare_data",
                          param_list=[],
                          param_map={"data": {"name": "data"},
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
                        condition={"params": [], "func": "True"}
                        )
