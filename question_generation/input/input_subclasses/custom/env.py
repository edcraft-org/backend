from typing import Any, List, Tuple, Dict

class Env:
    """
    Base class for an environment.
    """

    def transition(self, state: Any, action: Any) -> Tuple[Any, Dict]:
        """
        Perform an action in the environment.

        Args:
            state (Any): The current state of the environment.
            action (Any): The action to be performed.

        Returns:
            Tuple[Any, Dict]: A tuple containing the next state, and additional info.
        """
        raise NotImplementedError

    def initial_state(self) -> Any:
        """
        Get the initial state of the environment.

        Returns:
            Any: The initial state of the environment.
        """
        raise NotImplementedError

    def terminal(self, state: Any) -> bool:
        """
        Check if the given state is a terminal state.

        Args:
            state (Any): The state to be checked.

        Returns:
            bool: True if the state is terminal, False otherwise.
        """
        raise NotImplementedError

    def get_possible_actions(self, state: Any) -> List[Any]:
        """
        Get the possible actions that can be performed from the given state.

        Args:
            state (Any): The current state of the environment.

        Returns:
            List[Any]: A list of possible actions.
        """
        raise NotImplementedError

    def __str__(self):
        """
        Get a string representation of the environment.

        Returns:
            str: A string representation of the environment.
        """
        raise NotImplementedError
