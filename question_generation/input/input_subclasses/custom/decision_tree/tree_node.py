from question_generation.input.input_class import Input
from question_generation.input.input_subclasses.primitive.int_type import IntInput

class DecisionTreeNode(Input):
    internal = True

    def __init__(self, label):
        self.label = str(label)
        self.children = {}
        self.attribute = None
        self.attribute_values = []

        self.pruned = False
        self.examples_labeled = []

        self.parent_attribute = None
        self.parent_attribute_value = None

    def __str__(self):
        return self.label