from abc import ABC, abstractmethod


class InputClass(ABC):
    @abstractmethod
    def input_type(self):
        pass
    
    @abstractmethod
    def obtain_input(self, input_data):
        pass


class ProcessorClass(ABC):
    @abstractmethod
    def process_method(self):
        pass


class QueryableClass(ABC):
    @abstractmethod
    def query_options(self):
        pass


class Question(InputClass, ProcessorClass, QueryableClass):
    @abstractmethod
    def input_type(self):
        pass

    @abstractmethod
    def obtain_input(self, input_data):
        pass

    @abstractmethod
    def process_method(self):
        pass

    @abstractmethod
    def query_options(self):
        pass