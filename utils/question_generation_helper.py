import ast
from copy import deepcopy
import random
from typing import Any, Dict, List, Optional

from models.question_generation import ContextRequest, GenerateQuestionRequest, SubQuestion
from question_generation.queryable.queryable_class import Queryable
from utils.faker_helper import generate_data_for_type
from utils.types_helper import GeneratedQuestionClassType
from utils.classes_helper import get_all_subclasses, get_matching_class, get_subtopic_class
from utils.exceptions import handle_exceptions
from utils.variable_helper import get_algo_variables, get_query_variables

@handle_exceptions
def generate_variable(
    autoloaded_classes: Dict[str, Dict[str, GeneratedQuestionClassType]],
    topic: str,
    subtopic: str,
    arguments: Dict[str, Any],
    element_type: Dict[str, str],
    subclasses: Dict[str, str],
    question_description: str,
    arguments_init: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    cls = get_subtopic_class(autoloaded_classes, topic, subtopic)
    cls_instance = cls()
    algo_variables = get_algo_variables(cls)
    for var in algo_variables:
        if var["name"] in subclasses:
            var["type"] = get_matching_class(get_all_subclasses(var["type"]), subclasses[var["name"]])
    try:
        algo_generated_data = {}
        if arguments_init:
            for key, value in arguments_init.items():
                var_type = next((v["type"] for v in algo_variables if v["name"] == key), None)
                if var_type:
                    algo_generated_data[key] = var_type(**value) if isinstance(value, dict) else var_type(value)
                else:
                    algo_generated_data[key] = value
        # if arguments_init:
        #     algo_generated_data = {
        #         key: algo_variables[key]["type"](**value) if isinstance(value, dict) else value
        #         for key, value in arguments_init.items()
        #     }
        else:
            algo_generated_data = generate_data(algo_variables, element_type, arguments)
        algo_generated_data_init = {
            key: value.get_init_args() if hasattr(value, 'get_init_args') else value
            for key, value in algo_generated_data.items()
        }
    except Exception as e:
        print(f"Error generating variable: {e}")
        algo_generated_data = {}
    result = {}
    result['context'] = algo_generated_data
    result['context_init'] = algo_generated_data_init
    result['description'] = cls_instance.format_question_description(question_description, {**algo_generated_data})
    result['cls'] = cls
    result['cls_instance'] = cls_instance
    return result

@handle_exceptions
def generate_question(
    request: GenerateQuestionRequest,
    autoloaded_classes: Dict[str, Dict[str, GeneratedQuestionClassType]],
) -> Dict[str, Any]:
    try:
        result = {}
        outerContext = deepcopy(request.context)
        outer = generate_variable(
            autoloaded_classes,
            request.context.selectedTopic,
            request.context.selectedSubtopic,
            request.context.arguments,
            request.context.selectedQuantifiables,
            request.context.selectedSubclasses,
            request.description,
            arguments_init=request.context.argumentsInit
        )
        result['description'] = outer['description']
        # Generate SVG for main question
        svg_content = generate_svg(outer['context'])
        if svg_content:
            result['svg'] = svg_content

        if request.sub_questions:
            result['subquestions'] = [
                generate_subquestion(autoloaded_classes, outer, outerContext, subquestion)
                for subquestion in request.sub_questions
            ]

        return result

    except Exception as e:
        print(f"Error generating variable: {e}")
        return {}

def generate_subquestion(
    autoloaded_classes: Dict[str, Dict[str, Any]],
    outer: Dict[str, Any],
    outerContext: ContextRequest,
    subquestion: SubQuestion
) -> Dict[str, Any]:
    try:
        if subquestion.context.selectedSubtopic:
            inner = generate_variable(
                autoloaded_classes,
                subquestion.context.selectedTopic,
                subquestion.context.selectedSubtopic,
                subquestion.context.arguments,
                subquestion.context.selectedQuantifiables if subquestion.context.selectedQuantifiables else outerContext.selectedQuantifiables,
                subquestion.context.selectedSubclasses if subquestion.context.selectedSubclasses else outerContext.selectedSubclasses,
                subquestion.description,
                arguments_init=subquestion.context.argumentsInit if subquestion.context.argumentsInit else outerContext.argumentsInit
            )
            sub_algo_variables = inner['context']
            cls_instance = inner['cls_instance']
            cls = inner['cls']
        else:
            sub_algo_variables = outer['context']
            cls_instance = outer['cls_instance']
            cls = outer['cls']
        query_variables = get_query_variables(cls, subquestion.queryable)
        sub = {}
        try:
            sub['answer'], copy_algo_generated_data, query_generated_data, answer_svg_content = process_query_result(
                cls_instance,
                sub_algo_variables,
                subquestion.queryable,
                subquestion.context.selectedQuantifiables,
                query_variables,
                subquestion.context.arguments
            )
        except Exception as e:
            print(f"Error processing query result: {e}")
            return {}
        sub['description'] = cls_instance.format_question_description(
            subquestion.description,
            {**copy_algo_generated_data, **query_generated_data}
        )

        # Generate options for subquestion
        options = [sub['answer']]
        for _ in range(subquestion.questionDetails.number_of_options - 1):
            try:
                option = generate_options(
                    cls,
                    copy_algo_generated_data,
                    subquestion.queryable,
                    subquestion.context.selectedQuantifiables,
                    query_variables,
                    sub['answer'],
                    subquestion.context.arguments
                )
                options.append(option)
            except Exception as e:
                print(f"Error generating option: {e}")
                continue
        sub['options'] = options
        sub['marks'] = subquestion.questionDetails.marks
        # Generate SVG for subquestion
        svg_content = generate_svg(copy_algo_generated_data)
        if svg_content:
            sub['svg'] = svg_content
        if answer_svg_content:
            sub['answer_svg'] = answer_svg_content
        return sub

    except Exception as e:
        print(f"Error generating subquestion: {e}")
        return {}

def process_query_result(cls_instance, algo_generated_data, queryable_type, element_type, query_variables, arguments):
    try:
        copy_algo_generated_data = deepcopy(algo_generated_data)
        cls_instance.algo(**copy_algo_generated_data)
        query_result = cls_instance.query_all()
        for base, query_method, generate_input in query_result:
            if base.__name__ == queryable_type and issubclass(base, Queryable):
                query_base, query_method = base, query_method
                base_instance = query_base()
                copy_attributes(cls_instance, base_instance)
                if generate_input:
                    query_generated_data = generate_input(base_instance)
                else:
                    query_generated_data = generate_data(query_variables, element_type, arguments)
                query_output = query_method(base_instance, **deepcopy(query_generated_data))
                value, graph = query_output['value'], query_output['svg']
                return str(value), copy_algo_generated_data, query_generated_data, graph
    except Exception as e:
        print(f"Error processing query result: {e}")
        return '', {}, {}

def generate_data(variables: list, element_type: Dict[str, str], arguments: Dict[str, Any]) -> Dict[str, Any]:
    return {
        var["name"]: generate_data_for_type(
            var['type'],
            element_type.get(var["name"]),
            arguments.get(var["name"], {})
        )
        for var in variables
    }

def copy_attributes(source_instance: Any, target_instance: Any) -> None:
    for attr in dir(source_instance):
        if not attr.startswith('__') and hasattr(target_instance, attr) and attr != 'variable':
            setattr(target_instance, attr, getattr(source_instance, attr))

def generate_options(cls, algo_generated_data, queryable_type, element_type, query_variables, query_answer, arguments):
    option_data = deepcopy(algo_generated_data)
    cls_instance = cls(generate_graph=False)  # Create a new instance of the class
    for var_name, var_value in option_data.items():
        if hasattr(var_value, 'generate_options') and callable(getattr(var_value, 'generate_options')):
            option_instance = var_value.generate_options()
            option_data[var_name] = option_instance
    query_result_option, _, _, _ = process_query_result(cls_instance, option_data, queryable_type, element_type, query_variables, arguments)
    try:
        if str(query_result_option) == query_answer:
            try:
                opt = ast.literal_eval(query_answer)
                if isinstance(opt, list):
                    random.shuffle(opt)
                    return str(opt)
            except (ValueError, SyntaxError) as e:
                print(f"Error in ast.literal_eval: {e}")
                return query_result_option
    except Exception as e:
        print(f"Error during comparison: {e}")

    return query_result_option

def generate_svg(algo_generated_data) -> Dict[str, Optional[str]]:
    """
    Generate Graphviz and table representations in SVG format if the instance has to_graph and to_table methods.

    Args:
        algo_generated_data (Dict[str, Any]): The generated data.

    Returns:
        Dict[str, Optional[str]]: The SVG content for graph and table if available, otherwise None.
    """
    instance = algo_generated_data.get('input') or algo_generated_data.get('problem')
    svg_content = {}
    if instance:
        if hasattr(instance, 'to_graph') and callable(getattr(instance, 'to_graph')):
            svg_content['graph'] = instance.to_graph()
        if hasattr(instance, 'to_table') and callable(getattr(instance, 'to_table')):
            svg_content['table'] = instance.to_table()

    return svg_content if svg_content else None
