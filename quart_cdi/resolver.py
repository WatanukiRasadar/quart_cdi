from dataclasses import dataclass

from quart_cdi.interface import ServiceContainerInterface
from quart_cdi.utils import require


@dataclass
class ParameterResolver:

    service_container: ServiceContainerInterface

    def resolve(self, parameter_value):
        if isinstance(parameter_value, str):
            if parameter_value.startswith('@') and ':' in parameter_value:
                resolver_name, _parameter_value = parameter_value[1:].split(':', 1)
                if hasattr(self, f'_resolve_{resolver_name}'):
                    resolver = getattr(self, f'_resolve_{resolver_name}')
                    return self.resolve(resolver(_parameter_value))
        if isinstance(parameter_value, dict):
            return {k: self.resolve(v) for k, v in parameter_value.items()}
        if isinstance(parameter_value, list):
            return [self.resolve(v) for v in parameter_value]
        return parameter_value

    def _resolve_service(self, service_name):
        return self.service_container.get_service(service_name)

    def _resolve_parameter(self, parameter_name):
        return self.service_container.get_parameter(parameter_name)

    def _resolve_class(self, class_path):
        return require(class_path)
