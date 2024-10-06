from abc import ABC, abstractmethod
from typing import Any, List

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

    @classmethod
    @abstractmethod
    def format_question_description(cls, queryable: str, question_description: str, variables_data: List[Any]) -> str:
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

    @classmethod
    def format_question_description(cls, queryable: str, question_description: str, variables_data: List[Any]) -> str:
        # Find the topic item that matches the queryable
        topic_item = next((item for item in cls.topic if item['queryable'] == queryable), None)
        if not topic_item:
            raise ValueError(f"Queryable {queryable} not found in Insertion Sort topic")

        # Format the question description with variable names and values
        formatted_description = question_description
        for index, variable_name in enumerate(topic_item['variables']):
            formatted_description = formatted_description.replace(f"{{{variable_name}}}", f"{variable_name}: {variables_data[index]}")

        return formatted_description