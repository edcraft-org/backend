from typing import List
from question_generation.input.input_subclasses.custom.adversarial_problem.adversarial_problem import AdversarialProblem

class TicTacToe(AdversarialProblem):
    def __init__(self, board: List[List[str]] = None):
        self.board = board if board else [[' ' for _ in range(3)] for _ in range(3)]

    def get_legal_actions(self, state: List[List[str]]) -> List[tuple]:
        actions = []
        for row in range(3):
            for col in range(3):
                if state[row][col] == ' ':
                    actions.append((row, col))
        return actions

    def apply_action(self, state: List[List[str]], action: tuple, maximising: bool) -> List[List[str]]:
        """
        Apply the action to the board, marking the current player's move.
        If `maximising` is True, it's player 'X' making the move, otherwise player 'O'.
        """
        new_state = [row[:] for row in state]  # Create a copy of the state
        row, col = action
        current_player = 'X' if maximising else 'O'
        new_state[row][col] = current_player
        return new_state

    def is_terminal(self, state: List[List[str]]) -> bool:
        for row in state:
            if row[0] == row[1] == row[2] != ' ':
                return True
        for col in range(3):
            if state[0][col] == state[1][col] == state[2][col] != ' ':
                return True
        if state[0][0] == state[1][1] == state[2][2] != ' ':
            return True
        if state[0][2] == state[1][1] == state[2][0] != ' ':
            return True
        if all(cell != ' ' for row in state for cell in row):
            return True
        return False

    def evaluate(self, state: List[List[str]], maximising: bool) -> float:
            """
            Evaluate the board based on whether it's the maximizing or minimizing player's turn.
            - 1 if the maximizing player wins
            - -1 if the minimizing player wins
            - 0 for a draw or ongoing game
            """
            if self.is_terminal(state):
                # Check rows, columns, and diagonals for a winner
                for row in state:
                    if row[0] == row[1] == row[2] != ' ':
                        return 1 if (row[0] == 'X' and maximising) or (row[0] == 'O' and not maximising) else -1
                for col in range(3):
                    if state[0][col] == state[1][col] == state[2][col] != ' ':
                        return 1 if (state[0][col] == 'X' and maximising) or (state[0][col] == 'O' and not maximising) else -1
                if state[0][0] == state[1][1] == state[2][2] != ' ':
                    return 1 if (state[0][0] == 'X' and maximising) or (state[0][0] == 'O' and not maximising) else -1
                if state[0][2] == state[1][1] == state[2][0] != ' ':
                    return 1 if (state[0][2] == 'X' and maximising) or (state[0][2] == 'O' and not maximising) else -1
                return 0  # It's a draw if no winner
            return 0  # Game is ongoing, return a neutral value

    def get_state(self) -> List[List[str]]:
        return self.board
