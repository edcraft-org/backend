from abc import ABC, abstractmethod
from typing import List, Any

class AdversarialProblem(ABC):
    @abstractmethod
    def get_legal_actions(self, state: Any) -> List[Any]:
        """
        Return a list of all legal actions for the current state.
        :param state: The current state of the game or problem.
        """
        pass

    @abstractmethod
    def apply_action(self, state: Any, action: Any, maximising: bool) -> Any:
        """
        Apply an action to the current state and return the resulting state.
        :param state: The current state of the game or problem.
        :param action: The action to apply.
        :param maximising: True if the player is the maximizing player, False otherwise
        """
        pass

    @abstractmethod
    def is_terminal(self, state: Any) -> bool:
        """
        Check if the given state is a terminal state (e.g., game over).
        :param state: The state to check.
        """
        pass

    @abstractmethod
    def evaluate(self, state: Any, maximising: bool) -> float:
        """
        Evaluate the given state from the perspective of a specific player.
        :param state: The current state of the game or problem.
        :param maximising: True if the player is the maximizing player, False otherwise.
        """
        pass

    @abstractmethod
    def get_state(self) -> Any:
        """
        Return the current state of the game or problem.
        """
        pass
