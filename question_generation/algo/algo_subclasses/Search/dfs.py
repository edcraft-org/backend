from copy import deepcopy
from question_generation.algo.algo import Algo
from question_generation.input.input_subclasses.custom.graph_type import GraphInput
from question_generation.quantifiable.quantifiable_class import Quantifiable
from question_generation.queryable.queryable_subclasses.output import Output
from question_generation.queryable.queryable_subclasses.step import Step
from question_generation.question.question import Question


class DFSClass(Algo, Question, Output, Step):
    def __init__(self):
        super().__init__()

    def algo(self, input: GraphInput[Quantifiable], start: Quantifiable):
        print(input, start)
        """Depth First Search on Graph
        :param graph: directed graph in dictionary format
        :param start: starting vertex as a string
        :returns: the trace of the search
        >>> input_G = { "A": ["B", "C", "D"], "B": ["A", "D", "E"],
        ... "C": ["A", "F"], "D": ["B", "D"], "E": ["B", "F"],
        ... "F": ["C", "E", "G"], "G": ["F"] }
        >>> output_G = list({'A', 'B', 'C', 'D', 'E', 'F', 'G'})
        >>> all(x in output_G for x in list(depth_first_search(input_G, "A")))
        True
        >>> all(x in output_G for x in list(depth_first_search(input_G, "G")))
        True
        """
        initial = start.value()
        graph = input.value()
        explored, stack = {initial}, [initial]
        while stack:
            v = stack.pop()
            explored.add(v)
            # Differences from BFS:
            # 1) pop last element instead of first one
            # 2) add adjacent elements to stack without exploring them
            for adj in reversed(graph[v]):
                if adj not in explored:
                    stack.append(adj)
                self.step(deepcopy(explored))
        self.output(deepcopy(explored))