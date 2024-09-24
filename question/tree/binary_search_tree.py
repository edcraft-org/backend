from question.question import Question
from question.data_types import DataStructureTypes


class BinarySearchTreeQuestion(Question):
    def input_type(self):
        return DataStructureTypes.LIST.value

    def obtain_input(self, input_data):
        if not isinstance(input_data, list):
            raise ValueError("Input data must be a list")
        self.input_data = input_data

    def process_method(self):
        pass

    def query_options(self):
        pass