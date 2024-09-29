from .merge_sort import MergeSortQuestion
from .insertion_sort import InsertionSortQuestion

# Define the nested dictionary for topic-subtopic mapping
SORT_TOPIC_SUBTOPIC_MAPPING = {
    "Sort": {
        "Insertion Sort": InsertionSortQuestion,
        "Merge Sort": MergeSortQuestion,
        "Bubble Sort": None,
        "Quick Sort": None,
        # Add more subtopics here
    },
    # Add more topics here
}