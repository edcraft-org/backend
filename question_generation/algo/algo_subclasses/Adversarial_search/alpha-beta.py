from question_generation.algo.algo import Algo
from question_generation.input.input_subclasses.custom.adversarial_problem.adversarial_problem import AdversarialProblem
from question_generation.queryable.queryable_subclasses.output import Output
from question_generation.question.question import Question

class AlphaBetaClass(Algo, Question, Output):
    def algo(self, problem: AdversarialProblem, maximising: bool, left_to_right: bool = True) -> float:
        def minimax(problem: AdversarialProblem, state, alpha: float, beta: float, maximising: bool) -> float:
            if problem.is_terminal(state):
                return problem.evaluate(state, maximising)

            legal_actions = problem.get_legal_actions(state)
            if not left_to_right:
                legal_actions = reversed(legal_actions)

            if maximising:
                max_eval = float('-inf')
                for action in legal_actions:
                    new_state = problem.apply_action(state, action, maximising)
                    eval = minimax(problem, new_state, alpha, beta, False)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                return max_eval
            else:
                min_eval = float('inf')
                for action in legal_actions:
                    new_state = problem.apply_action(state, action, maximising)
                    eval = minimax(problem, new_state, alpha, beta, True)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
                return min_eval

        result = minimax(problem, problem.get_state(), alpha=float('-inf'), beta=float('inf'), maximising=maximising)
        self.output(result)
