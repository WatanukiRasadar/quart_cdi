from abc import ABC, abstractmethod


class ServiceContainerInterface(ABC):

    parameters: dict
    services: dict

    @abstractmethod
    def has_service(self, service_name: str):
        raise NotImplementedError('implement it')

    @abstractmethod
    def get_service(self, service_name: str):
        raise NotImplementedError('implement it')

    @abstractmethod
    def has_parameter(self, parameter_name: str):
        raise NotImplementedError('implement it')

    @abstractmethod
    def get_parameter(self, parameter_name: str):
        raise NotImplementedError('implement it')
