from dataclasses import dataclass, field
from .interface import ServiceContainerInterface
from quart import current_app

from quart_cdi.wrapper import Wrapper


@dataclass
class Container(ServiceContainerInterface):

    services: dict = field(default_factory=dict)
    parameters: dict = field(default_factory=dict)

    def has_service(self, service_name: str) -> bool:
        return service_name in self.services.keys()

    def get_service(self, service_name: str) -> dict:
        if self.has_service(service_name):
            return self.services[service_name]
        raise NotImplementedError(f'the service "{service_name}" not implemented')

    def has_parameter(self, parameter_name: str):
        return parameter_name in self.parameters.keys()

    def get_parameter(self, parameter_name: str):
        if self.has_parameter(parameter_name):
            return self.parameters[parameter_name]
        raise NotImplementedError(f'the parameter "{parameter_name}" not found')


container: Container = Wrapper(Container, current_app)
