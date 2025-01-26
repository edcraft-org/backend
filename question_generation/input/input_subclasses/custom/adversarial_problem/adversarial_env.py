from question_generation.input.input_subclasses.custom.adversarial_problem.adversarial_element import AdversarialElement
from typing import Any, List, Tuple, Dict

from question_generation.input.input_subclasses.custom.env import Env

class AdversarialEnv(Env):
    """
    Base class for an adversarial environment.
    """
    def __init__(self, initial: Any):
        """
        Args:
            # initial: The initial state.
        """
        super().__init__()
        self.initial = initial

    def transition(self, state: AdversarialElement, action: Any, turn: bool) -> Tuple[Any, Dict, float]:
        """
        Perform an action in the environment and return the next state, info and score.
        """
        return action, {}, 0.0

    def initial_state(self) -> Any:
        return self.initial

    def terminal(self, state: AdversarialElement) -> bool:
        """
        Check if the state is a terminal state.
        """
        return state.is_terminal()

    def get_possible_actions(self, state: AdversarialElement) -> List[Any]:
        return state.get_actions()

    def __str__(self):
        return "AdversarialEnv"

    def evaluate(self, state: AdversarialElement, turn: bool) -> float:
        """Compute the score (can be customized depending on the game)."""
        if self.terminal(state):
            return state.value()
        raise ValueError("Evaluation called on a non-terminal node.")
