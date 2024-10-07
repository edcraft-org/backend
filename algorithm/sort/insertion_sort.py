from collections.abc import MutableSequence
from typing import Any, Protocol, Tuple, TypeVar, Callable, List, Optional

class Comparable(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...

T = TypeVar("T", bound=Comparable)

class InsertionSortClass:
    def __init__(self, collection: MutableSequence[T]):
        self.collection = collection
        self.states: List[Tuple[MutableSequence[T], int]] = []

    def sort(self, callback: Optional[Callable[[MutableSequence[T], int], None]] = None) -> MutableSequence[T]:
        """Sorts the collection using the insertion sort algorithm."""
        iteration = 0
        if callback:
            callback(self.collection, iteration)

        for insert_index in range(1, len(self.collection)):
            insert_value = self.collection[insert_index]
            while insert_index > 0 and insert_value < self.collection[insert_index - 1]:
                self.collection[insert_index] = self.collection[insert_index - 1]
                insert_index -= 1
            self.collection[insert_index] = insert_value
            iteration += 1
            if callback:
                callback(self.collection, iteration)
        return self.collection

    def collect_states(self, state: MutableSequence[T], iteration: int):
        """A callback function for debugging that collects the state of the list."""
        self.states.append((state.copy(), iteration))

    def sort_with_states(self) -> Tuple[MutableSequence[T], List[Tuple[MutableSequence[T], int]]]:
        """Sorts the collection and collects the state at each iteration."""
        self.states = []
        sorted_collection = self.sort(callback=self.collect_states)
        return sorted_collection, self.states

    def get_state_at_iteration(self, iteration: int) -> Optional[MutableSequence[T]]:
        """Returns the state of the list at a specific iteration."""
        for state, iter_num in self.states:
            if iter_num == iteration:
                return state
        return None

# Example usage
if __name__ == "__main__":
    user_input = input("Enter numbers separated by a comma:\n").strip()
    unsorted = [int(item) for item in user_input.split(",")]

    sorter = InsertionSortClass(unsorted)
    sorted_list, states = sorter.sort_with_states()

    print(f"Sorted: {sorted_list}")
    print("States during sorting:")
    for state, iteration in states:
        print(f"Iteration {iteration}: {state}")

    # Query state at a specific iteration
    iteration = 3
    state_at_iteration_result = sorter.get_state_at_iteration(iteration)
    print(f"State at iteration {iteration}: {state_at_iteration_result}")