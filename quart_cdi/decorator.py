from functools import wraps
from quart_cdi.context import context


class DumpArguments:

    def __init__(self, **serializers):
        self.serializers = serializers

    def __call__(self, fun):
        @wraps(fun)
        def wrapper(*args, **kwargs):
            parameters = {}
            for parameter_name, parameter_value in kwargs.items():
                if parameter_name in self.serializers.keys():
                    dump_args = {}
                    if isinstance(parameter_value, dict):
                        dump_args['many'] = True
                    parameters[parameter_name] = context.get_service(self.serializers[parameter_name]).dump(parameter_value, **dump_args)
                else:
                    parameters[parameter_name] = parameter_value
            return fun(*args, **kwargs)
        return wrapper


class LoadArguments:

    def __init__(self, **serializers):
        self.serializers = serializers

    def __call__(self, fun):
        @wraps(fun)
        def wrapper(*args, **kwargs):
            parameters = {}
            for parameter_name, parameter_value in kwargs.items():
                if parameter_name in self.serializers.keys():
                    dump_args = {}
                    if isinstance(parameter_value, dict):
                        dump_args['many'] = True
                    parameters[parameter_name] = context.get_service(self.serializers[parameter_name]).load(parameter_value, **dump_args)
                else:
                    parameters[parameter_name] = parameter_value
            return fun(*args, **kwargs)
        return wrapper
