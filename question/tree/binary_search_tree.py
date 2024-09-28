from question.question import Question
from question.data_types import DataStructureTypes

class BinarySearchTreeQuestion(Question):
    # Define the structure as a class attribute
    topic = [
        {
            'queryable': 'Preorder',
            'variables': ['Binary Search Tree'],
            'outputType': 'Array',
        },
        {
            'queryable': 'Postorder',
            'variables': ['Binary Search Tree'],
            'outputType': 'Array',
        },
        {
            'queryable': 'Inorder',
            'variables': ['Binary Search Tree'],
            'outputType': 'Array',
        },
        {
            'queryable': 'Kth smallest element',
            'variables': ['Binary Search Tree', 'Kth smallest element'],
            'outputType': 'Number',
        },
    ]

    @classmethod
    def input_type(cls):
        return DataStructureTypes.LIST.value

    @classmethod
    def obtain_input(cls, input_data):
        if not isinstance(input_data, list):
            raise ValueError("Input data must be a list")
        cls.input_data = input_data

    @classmethod
    def process_method(cls):
        pass

    @classmethod
    def query_options(cls):
        return cls.topic

    @classmethod
    def output_type(cls, queryable):
        for item in cls.topic:
            if item['queryable'] == queryable:
                return item['outputType']
        raise ValueError(f"Queryable {queryable} not found in Binary Search Tree topic")

    # @classmethod
    # def variables(cls, queryable):
    #     for item in cls.topic:
    #         if item['queryable'] == queryable:
    #             return item['variables']
    #     raise ValueError(f"Queryable {queryable} not found in Binary Search Tree topic")
