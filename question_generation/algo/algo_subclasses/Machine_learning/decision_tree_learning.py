import math
from typing import Counter

from question_generation.algo.algo import Algo
from question_generation.graph.decision_tree_graph import DecisionTreeGraph
from question_generation.input.input_subclasses.custom.decision_tree.decision_tree import DecisionTreeInput
from question_generation.input.input_subclasses.custom.decision_tree.tree_node import DecisionTreeNode
from question_generation.queryable.queryable_subclasses.evaluate import Evaluate
from question_generation.queryable.queryable_subclasses.output import Output
from question_generation.queryable.queryable_subclasses.step import Step
from question_generation.question.question import Question

class DecisionTreeLearningClass(Algo, Question, Step, Output, Evaluate):
    def algo(self, problem: DecisionTreeInput) -> None:
        # Dynamically determine the class attribute
        class_attribute = list(problem.value()[0].keys())[-1]
        def ID3(examples, default, root_attr=None):
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
            if root_attr:
                best_attribute = root_attr
                root_attr = None  # Only use the root attribute for the root node
            else:
                best_attribute = self.choose_attribute(examples, class_attribute)
            tree = DecisionTreeNode(best_attribute)
            tree.attribute = best_attribute

            # Split the examples by the best attribute
            attribute_values = set(example[best_attribute] for example in examples)
            tree.attribute_values = list(attribute_values)
            for value in attribute_values:
                subtree_examples = [
                    {key: val for key, val in example.items() if key != best_attribute}
                    for example in examples if example[best_attribute] == value
                ]
                subtree = ID3(subtree_examples, max(set(classifications), key=classifications.count))
                subtree.examples_labeled = subtree_examples
                subtree.parent_attribute = best_attribute
                subtree.parent_attribute_value = value
                tree.children[value] = subtree

            return tree

        # Build the decision tree and assign it to the problem's root
        try:
            examples = problem.value()
            classifications = [example[class_attribute] for example in examples]
            decision_tree_root = ID3(examples, max(classifications, key=classifications.count))
            if self.generate_graph:
                self.output_graph(decision_tree_root, DecisionTreeGraph())
            self.evaluate(decision_tree_root, self.evaluation, problem.generate_input)
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

    def evaluation(self, node, example):
        '''
        Takes in a tree and one example.
        Returns the Class value that the tree assigns to the example.
        '''
        if len(node.children) == 0:
            return node.label
        else:
            attribute_value = example[node.attribute]
            if attribute_value in node.children and node.children[attribute_value].pruned == False:
                return self.evaluation(node.children[attribute_value], example)
            # in case the attribute value was pruned or not belong to any existing branch
            # return the mode label of examples with other attribute values for the current attribute
            else:
                try:
                    examples = []
                    for value in node.attribute_values:
                        examples += node.children[value].examples_labeled
                    return self.mode_label(examples)
                except Exception as e:
                    print(f"Error evaluating decision tree: {e}")
                    return 0

    def mode_label(self, examples):
        classes = []
        class_attribute = list(examples[0].keys())[-1]
        for example in examples:
            classes.append(example[class_attribute])
        return Counter(classes).most_common(1)[0][0]
