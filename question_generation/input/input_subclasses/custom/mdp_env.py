from .env import Env
from typing import Any, Tuple, Dict

class MDPEnv(Env):
    """
    Abstract base class for a Markov Decision Process (MDP) environment.
    """

    def step(self, state: Any, action: Any) -> Tuple[Any, Dict, float]:
        """
        Perform an action in the environment and return the next state, additional info, and reward.

        Args:
            state (Any): The current state of the environment.
            action (Any): The action to be performed.

        Returns:
            Tuple[Any, bool, Dict, float]: A tuple containing the next state, a boolean indicating if the episode is done, additional info, and the reward.
        """
        next_state = self.transition(state, action)
        reward = self.reward(state, action, next_state)
        return next_state, {}, reward

    def reward(self, state: Any, action: Any, next_state: Any) -> float:
        """
        Calculate the reward for a given state transition.

        Args:
            state (Any): The current state of the environment.
            action (Any): The action performed.
            next_state (Any): The resulting state after the action.

        Returns:
            float: The reward for the state transition.
        """
        raise NotImplementedError
