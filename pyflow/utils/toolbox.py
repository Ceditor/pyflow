def build_step(name, module_name, func_name, param_list, param_map,
               result_name,
               condition):
    return {"name": name,
            "module_name": module_name,
            "func_name": func_name,
            "param_list": param_list,
            "param_map": param_map,
            "result_name": result_name,
            "condition": condition}
