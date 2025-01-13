from question_generation.algo.algo import Algo
from question_generation.input.input_subclasses.custom.graph.graph_env import GraphEnv
from question_generation.queryable.queryable_subclasses.output import Output
from question_generation.queryable.queryable_subclasses.step import Step
from question_generation.question.question import Question


class DFSClass(Algo, Question, Output, Step):
    def algo(self, input: GraphEnv) -> None:
        explored, steps, stack = set(), [], [input.initial_state()]
        while stack:
            v = stack.pop()
            explored.add(v)
            steps.append(v)
            self.step(steps)
            for adj in reversed(input.get_neighbours(v)):
                if adj not in explored:
                    stack.append(adj)
        self.output(steps)
