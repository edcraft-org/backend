import ast
from copy import deepcopy
import random
from typing import Any, Dict, List, Optional

from question_generation.queryable.queryable_class import Queryable
from utils.faker_helper import generate_data_for_type
from utils.types_helper import GeneratedQuestionClassType
from utils.classes_helper import get_all_subclasses, get_matching_class, get_subtopic_class
from utils.exceptions import handle_exceptions
from utils.variable_helper import get_variable_annotations


@handle_exceptions
def generate_question(autoloaded_classes: Dict[str, Dict[str, GeneratedQuestionClassType]], topic: str, subtopic: str, queryable_type: str, element_type: Dict[str, str], subclasses: Dict[str, str], number_of_options: int, question_description: str) -> Dict[str, Any]:
    cls = get_subtopic_class(autoloaded_classes, topic, subtopic)
    cls_instance = cls()
    variable_annotations = get_variable_annotations(cls, queryable_type)
    algo_variables = variable_annotations["algo_variables"]
    query_variables = variable_annotations["query_variables"]
    # Modify algo_variables with subclass name and class
    for var in algo_variables:
        if var["name"] in subclasses:
            var["type"] = get_matching_class(get_all_subclasses(var["type"]), subclasses[var["name"]])
    algo_generated_data = generate_data(algo_variables, element_type)

    result = {}
    result['answer'], query_generated_data = process_query_result(cls_instance, algo_generated_data, queryable_type, element_type, query_variables)
    result['question'] = cls_instance.format_question_description(question_description, {**algo_generated_data, **query_generated_data})

    # Generate options for algo variables
    options = []
    options.append(result['answer'])
    for _ in range(number_of_options - 1):
        options.append(generate_options(cls_instance, algo_generated_data, queryable_type, element_type, query_variables, result['answer']))

    result['options'] = options

    # Check if the input or problem variable has a to_graph method and generate SVG if it does
    svg_content = generate_svg(algo_generated_data)
    if svg_content:
        result['svg'] = svg_content

    return result

def process_query_result(cls_instance, algo_generated_data, queryable_type, element_type, query_variables):
    cls_instance.algo(**deepcopy(algo_generated_data))
    query_result = cls_instance.query_all()
    for base, query_method in query_result:
        if base.__name__ == queryable_type and issubclass(base, Queryable):
            query_generated_data = generate_data(query_variables, element_type)
            query_base, query_method = base, query_method
            base_instance = query_base()
            copy_attributes(cls_instance, base_instance)
            query_output = query_method(base_instance, **deepcopy(query_generated_data))
            return str(query_output), query_generated_data

def generate_data(variables: list, element_type: Dict[str, str]) -> Dict[str, Any]:
    return {
        var["name"]: generate_data_for_type(
          var['type'],
          element_type.get(var["name"])
        )
        for var in variables
    }

def copy_attributes(source_instance: Any, target_instance: Any) -> None:
    for attr in dir(source_instance):
        if not attr.startswith('__') and hasattr(target_instance, attr) and attr != 'variable':
            setattr(target_instance, attr, getattr(source_instance, attr))

def generate_options(cls_instance, algo_generated_data, queryable_type, element_type, query_variables, query_answer):
    option_data = deepcopy(algo_generated_data)
    for var_name, var_value in option_data.items():
            if hasattr(var_value, 'generate_options') and callable(getattr(var_value, 'generate_options')):
                option_instance = var_value.generate_options()
                option_data[var_name] = option_instance
    query_result_option, _ = process_query_result(cls_instance, option_data, queryable_type, element_type, query_variables)
    if str(query_result_option) == query_answer:
        opt = ast.literal_eval(query_answer)
        random.shuffle(opt)
        if isinstance(opt, list):
            random.shuffle(opt)
            return str(opt)
    return query_result_option

def generate_svg(algo_generated_data) -> Optional[str]:
    """
    Generate a Graphviz representation in SVG format if the instance has a to_graph method.

    Args:
        instance (Any): The instance to generate the SVG for.

    Returns:
        Optional[str]: The SVG content if available, otherwise None.
    """
    instance = algo_generated_data.get('input') or algo_generated_data.get('problem')

    if instance and hasattr(instance, 'to_graph') and callable(getattr(instance, 'to_graph')):
        return instance.to_graph()
    return None
