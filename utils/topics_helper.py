from question.sort.sort_class import SortClass

TOPIC_CLASSES_MAPPING = {
    "Sort": SortClass
}

def get_topics():
    return list(TOPIC_CLASSES_MAPPING.keys())


def get_topic_class(topic: str):
    try:
        return TOPIC_CLASSES_MAPPING[topic]
    except KeyError:
        raise ValueError(f"Invalid topic '{topic}'")
