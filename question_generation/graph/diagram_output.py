class DiagramOutput:

    def to_graph(self) -> str:
        """
        Generate a Graphviz representation of the graph .

                Returns:
            str: The Graphviz representation in SVG format.
        """
        raise NotImplementedError

    def to_table(self) -> str:
        """
        Generate a table representation of the graph.

        Returns:
            str: The table representation.
        """
        raise NotImplementedError