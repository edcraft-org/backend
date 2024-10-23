from functools import singledispatchmethod
from typing import List, Any, Dict
from question.processor_class import ProcessorClass
from question.queryable_class import QueryableClass
from question.queryable_subclasses.output import OutputQueryableClass
from question.queryable_subclasses.step import StepQueryableClass


class DFSClass(ProcessorClass):
    @singledispatchmethod
    @classmethod
    def process_method(cls, queryable: QueryableClass, input: Any) -> Any:
        return super().process_method(queryable, input)

    @process_method.register
    @classmethod
    def _(cls, queryable: StepQueryableClass, graph: Dict[int, List[int]], start: int, step: int) -> List[int]:
        states: List[List[int]] = cls.algorithm(graph, start)

        if step - 1 < len(states):
            return states[step - 1]
        return []

    @process_method.register
    @classmethod
    def _(cls, queryable: OutputQueryableClass, graph: Dict[int, List[int]], start: int) -> List[int]:
        states: List[List[int]] = cls.algorithm(graph, start)
        return states[-1]

    @classmethod
    def algorithm(cls, graph: Dict[int, List[int]], start: int) -> List[List[int]]:
        visited = []
        stack = [start]
        states = []

        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.append(vertex)
                stack.extend([node for node in graph[vertex] if node not in visited])
                states.append(visited.copy())

        return states
