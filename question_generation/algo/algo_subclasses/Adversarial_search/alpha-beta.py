from question_generation.algo.algo import Algo
from question_generation.graph.game_tree_graph import GameTreeGraph
from question_generation.input.input_subclasses.custom.adversarial_problem.adversarial_env import AdversarialEnv
from question_generation.queryable.queryable_subclasses.output import Output
from question_generation.queryable.queryable_subclasses.pruned import Pruned
from question_generation.question.question import Question

class AlphaBetaClass(Algo, Question, Output, Pruned):
    def algo(self, problem: AdversarialEnv, maximising: bool, left_to_right: bool = True) -> float:
        def minimax(problem: AdversarialEnv, state, alpha: float, beta: float, maximising: bool) -> float:
            if problem.terminal(state):
                return problem.evaluate(state, maximising)

            legal_actions = problem.get_possible_actions(state)
            if not left_to_right:
                legal_actions = list(reversed(legal_actions))

            if maximising:
                max_eval = float('-inf')
                for i, action in enumerate(legal_actions):
                    new_state, _, _ = problem.transition(state, action, maximising)
                    eval = minimax(problem, new_state, alpha, beta, False)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, max_eval)
                    if beta <= alpha:
                        # Prune remaining actions
                        for remaining_action in legal_actions[i+1:]:
                            self.prune(state, remaining_action)
                        break
                return max_eval
            else:
                min_eval = float('inf')
                for i, action in enumerate(legal_actions):
                    new_state, _, _ = problem.transition(state, action, maximising)
                    eval = minimax(problem, new_state, alpha, beta, True)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, min_eval)
                    if beta <= alpha:
                        # Prune remaining actions
                        for remaining_action in legal_actions[i+1:]:
                            self.prune(state, remaining_action)
                        break
                return min_eval
        result = minimax(problem, problem.initial_state(), alpha=float('-inf'), beta=float('inf'), maximising=maximising)
        self.output(result)
        self.prune_graph(problem.initial_state(), GameTreeGraph())
