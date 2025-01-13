from ..env import Env
from typing import Any, List, Tuple, Dict

class GraphEnv(Env):
    def __init__(self, graph: Dict, start_node: Any, goal_node: Any):
        """
        Args:
            # graph: A dictionary where keys are states (nodes) and values are lists of neighboring states (edges).
            # start_node: The initial state (node).
            # goal_node: The goal state (node).
        """
        super().__init__()
        self.graph = graph
        self.start_node = start_node
        self.goal_node = goal_node

    def transition(self, state: Any, action: Any) -> Tuple[Any, Dict]:
        next_state = action  # action here is the state we are transitioning to
        return next_state, {}

    def initial_state(self) -> Any:
        return self.start_node

    def get_possible_actions(self, state: Any) -> List[Any]:
        return self.graph[state]

    def terminal(self, state: Any) -> bool:
        return state == self.goal_node

    def __str__(self):
        return "GraphEnv"

    def get_neighbours(self, state: Any) -> List[Any]:
        return self.get_possible_actions(state)
