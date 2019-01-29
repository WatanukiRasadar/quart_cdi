from importlib import import_module


def require(code_path: str):
    module_path, var_name = code_path.split(':')
    return getattr(import_module(module_path), var_name)
