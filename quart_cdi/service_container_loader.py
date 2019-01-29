from quart import current_app
from dataclasses import dataclass
from yaml import load

from quart_cdi.utils import require
from quart_cdi.interface import ServiceContainerInterface


@dataclass
class ServiceContainerLoader:

    service_container: ServiceContainerInterface

    def load_file(self, filepath):
        with open(filepath) as file:
            configurations = load(file) or {}
            for type, type_configuration in configurations.items(): #type: dict
                for name, configuration in type_configuration.items():
                    if hasattr(self, f'load_{type}'):
                        loader = getattr(self, f'load_{type}')
                        if not isinstance(configuration, dict):
                            configuration = dict(value=configuration)
                        loader(name=name, **configuration)
        return self

    def load_parameters(self, name: str, value):
        self.service_container.parameters[name] = value
        return self

    def load_services(self, name: str, factory: str, parameters: dict):
        self.service_container.services[name] = lambda container: container.resolve(factory).__call__(**{
            p: container.get_parameter(v)
            for p, v in parameters.items()
        })
        return self

    def get_container(self):
        return self.service_container

