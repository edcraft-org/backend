from functools import singledispatchmethod
from typing import List, Dict, Tuple, Any
import heapq
from question.processor_class import ProcessorClass
from question.queryable_class import QueryableClass
from question.queryable_subclasses.output import OutputQueryableClass
from question.queryable_subclasses.step import StepQueryableClass

class DijkstraClass(ProcessorClass):
    @singledispatchmethod
    @classmethod
    def process_method(cls, queryable: QueryableClass, input: Any) -> Any:
        return super().process_method(queryable, input)

    @process_method.register
    @classmethod
    def _(cls, queryable: StepQueryableClass, graph: Dict[int, List[Tuple[int, int]]], start: int, step: int) -> List[int]:
        states: List[List[int]] = cls.algorithm(graph, start)

        if step - 1 < len(states):
            return states[step - 1]
        return []

    @process_method.register
    @classmethod
    def _(cls, queryable: OutputQueryableClass, graph: Dict[int, List[Tuple[int, int]]], start: int) -> List[int]:
        states: List[List[int]] = cls.algorithm(graph, start)
        return states[-1]

    @classmethod
    def algorithm(cls, graph: Dict[int, List[Tuple[int, int]]], start: int) -> List[List[int]]:
        queue = [(0, start)]
        distances = {node: float('inf') for node in graph}
        distances[start] = 0
        states = []

        while queue:
            current_distance, current_node = heapq.heappop(queue)

            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in graph[current_node]:
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(queue, (distance, neighbor))
                    states.append(distances.copy())

        return states