from question_generation.algo.algo import Algo
from question_generation.input.input_subclasses.custom.adversarial_problem.adversarial_env import AdversarialEnv
from question_generation.queryable.queryable_subclasses.output import Output
from question_generation.question.question import Question

class MinimaxClass(Algo, Question, Output):
    def algo(self, problem: AdversarialEnv, maximising: bool) -> float:
        def minimax(problem:AdversarialEnv, state, maximising: bool) -> float:
            if problem.terminal(state):
                return problem.evaluate(state, maximising)

            if maximising:
                max_eval = float('-inf')
                for action in problem.get_possible_actions(state):
                    new_state, _, _ = problem.transition(state, action, maximising)
                    eval = minimax(problem, new_state, False)
                    max_eval = max(max_eval, eval)
                return max_eval
            else:
                min_eval = float('inf')
                for action in problem.get_possible_actions(state):
                    new_state, _, _ = problem.transition(state, action, maximising)
                    eval = minimax(problem, new_state, True)
                    min_eval = min(min_eval, eval)
                return min_eval
        result = minimax(problem, problem.initial_state(), maximising)
        self.output(result)
