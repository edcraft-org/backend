from question.tree import BinarySearchTreeQuestion

# Define the nested dictionary for topic-subtopic mapping
TOPIC_SUBTOPIC_MAPPING = {
    "Tree": {
        "Binary Search Tree": BinarySearchTreeQuestion,
        # Add more subtopics here
    },
    # Add more topics here
}

def get_question_class(topic, subtopic):
    try:
        return TOPIC_SUBTOPIC_MAPPING[topic][subtopic]
    except KeyError:
        raise ValueError(f"Invalid topic '{topic}' or subtopic '{subtopic}'")

def get_topics():
    return list(TOPIC_SUBTOPIC_MAPPING.keys())

def get_subtopics(topic):
    try:
        return list(TOPIC_SUBTOPIC_MAPPING[topic].keys())
    except KeyError:
        raise ValueError(f"Invalid topic '{topic}'")