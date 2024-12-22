from collections import deque
from question_generation.algo.algo import Algo
from question_generation.input.input_subclasses.custom.traversable.traversable import Traversable
from question_generation.queryable.queryable_subclasses.output import Output
from question_generation.queryable.queryable_subclasses.step import Step
from question_generation.question.question import Question


class BFSClass(Algo, Question, Output, Step):
    def algo(self, input: Traversable):
        explored, steps, q = set(), [], deque([input.get_start()])
        while q:
            v = q.popleft()
            explored.add(v)
            steps.append(v)
            self.step(steps)
            for adj in input.get_neighbors(v):
                if adj not in explored:
                    q.append(adj)
        self.output(steps)

