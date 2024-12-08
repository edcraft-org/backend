from abc import ABC


class Traversable(ABC):
    def get_neighbors(self, node):
        """
        Return the neighbors of a given node.
        :param node: The node whose neighbors are to be returned.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def get_start(self):
        """
        Return the starting node of the graph.
        """
        raise NotImplementedError("Subclasses must implement this method.")
