from abc import ABC, abstractmethod

class InputClass(ABC):
    @classmethod
    @abstractmethod
    def input_type(cls):
        pass

    @abstractmethod
    def obtain_input(self, input_data):
        pass

    # @classmethod
    # @abstractmethod
    # def variables(cls, method_name):
    #     pass

class ProcessorClass(ABC):
    @abstractmethod
    def process_method(self):
        pass

    @classmethod
    @abstractmethod
    def output_type(cls, method_name):
        pass

class QueryableClass(ABC):
    @classmethod
    @abstractmethod
    def query_options(cls):
        pass

class Question(InputClass, ProcessorClass, QueryableClass):
    topic = None

    @classmethod
    @abstractmethod
    def input_type(cls):
        pass

    @abstractmethod
    def obtain_input(self, input_data):
        pass

    @abstractmethod
    def process_method(self):
        pass

    @classmethod
    @abstractmethod
    def query_options(cls):
        pass

    @classmethod
    @abstractmethod
    def output_type(cls, method_name):
        pass