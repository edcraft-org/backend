"""
This is a pure Python implementation of the merge sort algorithm with a callback for debugging.

For doctests run following command:
python -m doctest -v merge_sort.py
or
python3 -m doctest -v merge_sort.py
For manual testing run:
python merge_sort.py
"""

from typing import Callable, List, Optional, Tuple

def merge_sort(collection: List[int], callback: Optional[Callable[[List[int], List[int], List[int], int, int], None]] = None, depth: int = 0, iteration: int = 0) -> List[int]:
    """
    Sorts a list using the merge sort algorithm with a callback for debugging.

    :param collection: A mutable ordered collection with comparable items.
    :param callback: A callback function that takes the current state of the list, the depth of recursion, and the iteration number.
    :param depth: The current depth of the recursion (used for debugging).
    :param iteration: The current iteration number (used for debugging).
    :return: The same collection ordered in ascending order.

    Time Complexity: O(n log n)

    Examples:
    >>> merge_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> merge_sort([])
    []
    >>> merge_sort([-2, -5, -45])
    [-45, -5, -2]
    """

    def merge(left: List[int], right: List[int], depth: int, iteration: int) -> Tuple[List[int], int]:
        """
        Merge two sorted lists into a single sorted list with a callback for debugging.

        :param left: Left collection
        :param right: Right collection
        :param depth: The current depth of the recursion (used for debugging).
        :param iteration: The current iteration number (used for debugging).
        :return: Merged result and updated iteration number.
        """
        result = []
        while left and right:
            if left[0] <= right[0]:
                result.append(left.pop(0))
            else:
                result.append(right.pop(0))
            iteration += 1
            if callback:
                callback(result + left + right, left, right, depth, iteration)
        result.extend(left)
        result.extend(right)
        iteration += 1
        if callback:
            callback(result, left, right, depth, iteration)
        return result, iteration

    if len(collection) <= 1:
        return collection

    mid_index = len(collection) // 2
    left_half = merge_sort(collection[:mid_index], callback, depth + 1, iteration)
    right_half = merge_sort(collection[mid_index:], callback, depth + 1, iteration)
    if callback:
        callback(left_half + right_half, left_half, right_half, depth, iteration)
    merged, iteration = merge(left_half, right_half, depth, iteration)
    return merged

def collect_states(state: List[int], left: List[int], right: List[int], depth: int, iteration: int, states: List[Tuple[List[int], List[int], List[int], int, int]]):
    """
    A sample callback function for debugging that collects the state of the list.

    :param state: The current state of the list.
    :param left: The current left sublist.
    :param right: The current right sublist.
    :param depth: The current depth of the recursion.
    :param iteration: The current iteration number.
    :param states: A list to collect the states.
    """
    states.append((state.copy(), left.copy(), right.copy(), depth, iteration))

def merge_sort_with_states(collection: List[int]) -> Tuple[List[int], List[Tuple[List[int], List[int], List[int], int, int]]]:
    """
    Sorts a list using the merge sort algorithm and collects the state at each iteration.

    :param collection: A mutable ordered collection with comparable items.
    :return: A tuple containing the sorted collection and a list of states at each iteration.
    """
    states = []
    sorted_collection = merge_sort(collection, callback=lambda state, left, right, depth, iteration: collect_states(state, left, right, depth, iteration, states))
    return sorted_collection, states

def state_at_iteration(collection: List[int], iteration: int) -> Optional[Tuple[List[int], List[int], List[int], int, int]]:
    """
    Returns the state of the list at a specific iteration.

    :param collection: A mutable ordered collection with comparable items.
    :param iteration: The iteration number.
    :return: The state of the list at the specified iteration, or None if the iteration is out of range.
    """
    _, states = merge_sort_with_states(collection)
    for state in states:
        if state[4] == iteration:
            return state
    return None

def state_at_depth(collection: List[int], depth: int) -> List[Tuple[List[int], List[int], List[int], int, int]]:
    """
    Returns the states of the list at a specific depth.

    :param collection: A mutable ordered collection with comparable items.
    :param depth: The depth of the recursion.
    :return: A list of states of the list at the specified depth.
    """
    _, states = merge_sort_with_states(collection)
    return [state for state in states if state[3] == depth]

if __name__ == "__main__":
    import doctest

    doctest.testmod()

    try:
        user_input = input("Enter numbers separated by a comma:\n").strip()
        unsorted = [int(item) for item in user_input.split(",")]
        print(f"Unsorted: {unsorted}")

        # Example usage
        sorted_list, states = merge_sort_with_states(unsorted)
        print(f"Sorted: {sorted_list}")
        print("States during sorting:")
        for state, left, right, depth, iteration in states:
            print(f"Iteration {iteration}, Depth {depth}: {state}, Left: {left}, Right: {right}")

        # Query state at a specific iteration
        iteration = 3
        state_at_iteration_result = state_at_iteration(unsorted, iteration)
        print(f"State at iteration {iteration}: {state_at_iteration_result}")

        # Query states at a specific depth
        depth = 2
        states_at_depth = state_at_depth(unsorted, depth)
        print(f"States at depth {depth}: {states_at_depth}")

    except ValueError:
        print("Invalid input. Please enter valid integers separated by commas.")