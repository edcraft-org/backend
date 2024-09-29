"""
A pure Python implementation of the insertion sort algorithm

This algorithm sorts a collection by comparing adjacent elements.
When it finds that order is not respected, it moves the element compared
backward until the order is correct.  It then goes back directly to the
element's initial position resuming forward comparison.

For doctests run following command:
python3 -m doctest -v insertion_sort.py

For manual testing run:
python3 insertion_sort.py
"""

from collections.abc import MutableSequence
from typing import Any, Protocol, Tuple, TypeVar, Callable, List, Optional


class Comparable(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


T = TypeVar("T", bound=Comparable)


def insertion_sort(collection: MutableSequence[T], callback: Optional[Callable[[MutableSequence[T], int], None]] = None) -> MutableSequence[T]:
    """A pure Python implementation of the insertion sort algorithm

    :param collection: some mutable ordered collection with heterogeneous
    comparable items inside
    :param callback: a callback function that takes the current state of the list and the iteration number.
    :return: the same collection ordered by ascending

    Examples:
    >>> insertion_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> insertion_sort([]) == sorted([])
    True
    >>> insertion_sort([-2, -5, -45]) == sorted([-2, -5, -45])
    True
    >>> insertion_sort(['d', 'a', 'b', 'e', 'c']) == sorted(['d', 'a', 'b', 'e', 'c'])
    True
    >>> import random
    >>> collection = random.sample(range(-50, 50), 100)
    >>> insertion_sort(collection) == sorted(collection)
    True
    >>> import string
    >>> collection = random.choices(string.ascii_letters + string.digits, k=100)
    >>> insertion_sort(collection) == sorted(collection)
    True
    """
    iteration = 0
    if callback:
        callback(collection, iteration)

    iteration = 0
    for insert_index in range(1, len(collection)):
        insert_value = collection[insert_index]
        while insert_index > 0 and insert_value < collection[insert_index - 1]:
            collection[insert_index] = collection[insert_index - 1]
            insert_index -= 1
        collection[insert_index] = insert_value
        iteration += 1
        if callback:
            callback(collection, iteration)
    return collection


def collect_states(state: MutableSequence[T], iteration: int, states: List[Tuple[MutableSequence[T], int]]):
    """
    A sample callback function for debugging that collects the state of the list.

    :param state: The current state of the list.
    :param iteration: The current iteration number.
    :param states: A list to collect the states.
    """
    states.append((state.copy(), iteration))


def insertion_sort_with_states(collection: MutableSequence[T]) -> Tuple[MutableSequence[T], List[Tuple[MutableSequence[T], int]]]:
    """
    Sorts a list using the insertion sort algorithm and collects the state at each iteration.

    :param collection: A mutable ordered collection with comparable items.
    :return: A tuple containing the sorted collection and a list of states at each iteration.
    """
    states = []
    sorted_collection = insertion_sort(collection, callback=lambda state, iteration: collect_states(state, iteration, states))
    return sorted_collection, states

def get_state_at_iteration(states: List[Tuple[MutableSequence[T], int]], iteration: int) -> Optional[MutableSequence[T]]:
    """
    Returns the state of the list at a specific iteration from the given states.

    :param states: A list of tuples containing the state of the list and the iteration number.
    :param iteration: The iteration number.
    :return: The state of the list at the specified iteration, or None if the iteration is out of range.
    """
    for state, iter_num in states:
        if iter_num == iteration:
            return state
    return None

def state_at_iteration(collection: MutableSequence[T], iteration: int) -> Optional[MutableSequence[T]]:
    """
    Returns the state of the list at a specific iteration.

    :param collection: A mutable ordered collection with comparable items.
    :param iteration: The iteration number.
    :return: The state of the list at the specified iteration, or None if the iteration is out of range.
    """
    _, states = insertion_sort_with_states(collection)
    for state, iter_num in states:
        if iter_num == iteration:
            return state
    return None


if __name__ == "__main__":
    from doctest import testmod

    testmod()

    user_input = input("Enter numbers separated by a comma:\n").strip()
    unsorted = [int(item) for item in user_input.split(",")]
    sorted_list, states = insertion_sort_with_states(unsorted)
    print(f"Sorted: {sorted_list}")
    print("States during sorting:")
    for state, iteration in states:
        print(f"Iteration {iteration}: {state}")

    # Query state at a specific iteration
    iteration = 3
    state_at_iteration_result = state_at_iteration(unsorted, iteration)
    print(f"State at iteration {iteration}: {state_at_iteration_result}")