from functools import singledispatchmethod
from typing import List, Dict, Tuple, Any
import heapq
from question.processor_class import ProcessorClass
from question.queryable_class import QueryableClass
from question.queryable_subclasses.output import OutputQueryableClass
from question.queryable_subclasses.step import StepQueryableClass

class AStarClass(ProcessorClass):
    @singledispatchmethod
    @classmethod
    def process_method(cls, queryable: QueryableClass, input: Any) -> Any:
        return super().process_method(queryable, input)

    @process_method.register
    @classmethod
    def _(cls, queryable: StepQueryableClass, graph: Dict[int, List[Tuple[int, int]]], start: int, goal: int, step: int) -> List[int]:
        states: List[List[int]] = cls.algorithm(graph, start, goal)

        if step - 1 < len(states):
            return states[step - 1]
        return []

    @process_method.register
    @classmethod
    def _(cls, queryable: OutputQueryableClass, graph: Dict[int, List[Tuple[int, int]]], start: int, goal: int) -> List[int]:
        states: List[List[int]] = cls.algorithm(graph, start, goal)
        return states[-1]

    @classmethod
    def heuristic(cls, a: int, b: int) -> int:
        return abs(a - b)

    @classmethod
    def algorithm(cls, graph: Dict[int, List[Tuple[int, int]]], start: int, goal: int) -> List[List[int]]:
        queue = [(0, start)]
        came_from = {start: None}
        cost_so_far = {start: 0}
        states = []

        while queue:
            current_priority, current_node = heapq.heappop(queue)

            if current_node == goal:
                break

            for neighbor, weight in graph[current_node]:
                new_cost = cost_so_far[current_node] + weight

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + cls.heuristic(goal, neighbor)
                    heapq.heappush(queue, (priority, neighbor))
                    came_from[neighbor] = current_node
                    states.append(cost_so_far.copy())

        return states