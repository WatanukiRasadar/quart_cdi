from dataclasses import dataclass, field
from quart import g, current_app, Quart

from quart_cdi.resolver import ParameterResolver
from quart_cdi.service_container_loader import ServiceContainerLoader
from quart_cdi.wrapper import Wrapper
from .container import container, Container
from .interface import ServiceContainerInterface


current_app: Quart


@dataclass
class Context(ServiceContainerInterface):

    container: Container = field(default_factory=lambda: current_app.config.get(
        'SERVICE_CONTAINER_LOADER_CLASS', ServiceContainerLoader).__call__(container).load_file(
            current_app.config.get('SERVICES_FILE', 'services.yml')
        ).get_container()
    )

    instances: dict = field(default_factory=dict)
    services: dict = field(default_factory=dict)
    parameters: dict = field(default_factory=dict)

    def has_service(self, service_name: str):
        return service_name in self.instances.keys() or service_name in self.services.keys() or self.container.has_service(service_name)

    def get_service(self, service_name: str):
        if service_name in self.instances.keys():
            return self.instances.get(service_name)
        if service_name in self.services.keys():
            self.instances[service_name] = self.services[service_name](self)
        elif self.container.has_service(service_name):
            self.instances[service_name] = self.container.get_service(service_name)(self)
        return self.instances.get(service_name)

    def get_parameter(self, parameter_name: str):
        value = self.parameters.get(parameter_name) or self.container.get_parameter(parameter_name)
        if isinstance(value, str):
            return self.resolve(value)
        return value

    def resolve(self, value):
        resolver_class = current_app.config.get('PARAMETER_RESOLVER_CLASS', ParameterResolver)
        resolver = resolver_class(self)
        return resolver.resolve(value)

    def has_parameter(self, parameter_name: str):
        return parameter_name in self.parameters.keys() or self.container.has_parameter(parameter_name)


context: Context = Wrapper(Context, g)
