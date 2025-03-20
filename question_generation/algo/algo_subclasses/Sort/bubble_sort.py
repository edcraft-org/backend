from copy import deepcopy
from question_generation.algo.algo import Algo
from question_generation.input.input_subclasses.composite.list_type import ListInput
from question_generation.quantifiable.quantifiable_class import Quantifiable
from question_generation.queryable.queryable_subclasses.output import Output
from question_generation.queryable.queryable_subclasses.step import Step
from question_generation.question.question import Question

class BubbleSortClass(Algo, Question, Output, Step):
    def algo(self, input: ListInput[Quantifiable]):
        n = len(input)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if input[j] > input[j + 1]:
                    input[j], input[j + 1] = input[j + 1], input[j]
                    swapped = True
            self.step(input)
            if not swapped:
                break
        self.output(input)
        return input