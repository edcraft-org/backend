import math

from question_generation.algo.algo import Algo
from question_generation.input.input_subclasses.custom.decision_tree.decision_tree import DecisionTreeInput
from question_generation.input.input_subclasses.custom.decision_tree.tree_node import DecisionTreeNode
from question_generation.queryable.queryable_subclasses.step import Step
from question_generation.question.question import Question

class DecisionTreeLearningClass(Algo, Question, Step):
    def algo(self, problem: DecisionTreeInput) -> None:
        # Dynamically determine the class attribute
        class_attribute = list(problem.value()[0].keys())[-1]

        def ID3(examples, default):
            # If examples are empty, return a leaf with the default label
            if not examples:
                return DecisionTreeNode(default)

            # If all examples have the same classification, return a leaf with that classification
            classifications = [example[class_attribute] for example in examples]
            if len(set(classifications)) == 1:
                return DecisionTreeNode(classifications[0])

            # If no non-trivial splits are possible, return a leaf with the most common classification
            if len(examples[0]) == 1:  # Only the class attribute remains
                return DecisionTreeNode(max(set(classifications), key=classifications.count))

            # Choose the best attribute for splitting
            best_attribute = self.choose_attribute(examples, class_attribute)
            tree = DecisionTreeNode(best_attribute)
            tree.attribute = best_attribute

            # Split the examples by the best attribute
            attribute_values = set(example[best_attribute] for example in examples)
            for value in attribute_values:
                subtree_examples = [
                    {key: val for key, val in example.items() if key != best_attribute}
                    for example in examples if example[best_attribute] == value
                ]
                subtree = ID3(subtree_examples, max(set(classifications), key=classifications.count))
                subtree.parent_attribute = best_attribute
                subtree.parent_attribute_value = value
                tree.children[value] = subtree

            return tree

        # Build the decision tree and assign it to the problem's root
        try:
            print('Building decision tree...')
            examples = problem.value()
            classifications = [example[class_attribute] for example in examples]
            decision_tree_root = ID3(examples, max(classifications, key=classifications.count))
            problem.set_root(decision_tree_root)
            print('Decision tree built successfully.')
        except Exception as e:
            print(f"Error generating decision tree: {e}")
            return

    def choose_attribute(self, examples, class_attribute):
        """
        Select the attribute with the highest information gain for splitting.
        """
        def entropy(data):
            labels = [row[class_attribute] for row in data]
            label_counts = {label: labels.count(label) for label in set(labels)}
            total = len(labels)
            return -sum((count / total) * (math.log2(count / total)) for count in label_counts.values())

        def information_gain(attribute):
            total_entropy = entropy(examples)
            values = set(example[attribute] for example in examples)
            weighted_entropy = sum(
                (len(subset) / len(examples)) * entropy(subset)
                for value in values
                for subset in [[example for example in examples if example[attribute] == value]]
            )
            return total_entropy - weighted_entropy

        best_attribute = max([attr for attr in examples[0] if attr != class_attribute], key=information_gain)
        info_gain = information_gain(best_attribute)
        self.step({'attribute': best_attribute, 'information_gain': info_gain})
        return best_attribute
