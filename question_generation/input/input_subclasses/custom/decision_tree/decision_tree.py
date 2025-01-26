import random
from typing import List, Dict, Any, Type
from graphviz import Digraph
import pandas as pd
import plotly.graph_objects as go

from question_generation.input.input_class import Input
from question_generation.input.input_subclasses.custom.decision_tree.tree_node import DecisionTreeNode
from question_generation.input.input_subclasses.primitive.int_type import IntInput

class DecisionTreeInput(Input):
    _exposed_args = ['columns', 'values', 'probs', 'num_samples']

    def __init__(self, data: List[Dict[str, Any]] = None, columns: List[str] = None, values: Dict[str, List[Any]] = None, probs: Dict[str, List[float]] = None, num_samples: int = 5):
        self.data = data if data is not None else []
        self.columns = columns if columns is not None else []
        self.values = values if values is not None else {}
        self.probs = probs if probs is not None else {}
        self.num_samples = num_samples
        self._value = self.data if self.data else self.generate_data()
        self.root = None

    def generate_data(self) -> List[Dict[str, Any]]:
        generated_data = []
        seen_samples = set()
        max_attempts = self.num_samples * 10  # Limit the number of attempts to avoid infinite loops

        for _ in range(max_attempts):
            if len(generated_data) >= self.num_samples:
                break
            sample = self.generate_sample()
            sample_tuple = tuple(sample.items())
            if sample_tuple not in seen_samples:
                seen_samples.add(sample_tuple)
                generated_data.append(sample)
        self.data = generated_data
        return generated_data

    def generate_sample(self) -> Dict[str, Any]:
        sample = {}
        for column in self.columns:
            sample[column] = str(random.choices(self.values[column], self.probs[column])[0])
        return sample

    def generate_input(self) -> Dict[str, Any]:
        input = self.generate_sample()
        columns_excluding_last = self.columns[:-1]
        input_excluding_last = {k: input[k] for k in columns_excluding_last}
        return {"example": input_excluding_last}

    def value(self) -> Any:
        return self._value

    def to_table(self) -> str:
        """
        Generate an SVG representation of the data in a tabular format using plotly.

        Returns:
            str: The SVG content representing the table.
        """
        data = self.value()
        if not data:
            return ""

        # Create a DataFrame from the data
        df = pd.DataFrame(data)

        # Create a plotly table
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(df.columns),
                        align='left'),
            cells=dict(values=[df[col] for col in df.columns],
                       align='left'))
        ])

        # Export the plotly figure to SVG
        svg_bytes = fig.to_image(format="svg")
        svg_content = svg_bytes.decode("utf-8")
        return svg_content

    def generate_options(self) -> 'DecisionTreeInput':
        """
        Generate options for generating input data.
        """
        new_data = []
        for sample in self._value:
            new_sample = sample.copy()
            for column in self.columns:
                if random.random() < 0.5:
                    new_sample[column] = random.choices(self.values[column], weights=self.probs[column])[0]
            new_data.append(new_sample)
        return self.__class__(data=new_data, columns=self.columns, values=self.values, probs=self.probs, num_samples=self.num_samples)

    def __str__(self) -> str:
        return f"{self._value}"