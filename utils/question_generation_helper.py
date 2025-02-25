import ast
from copy import deepcopy
import inspect
import random
from typing import Any, Dict, Optional, Type

from models.question_generation import ContextRequest, GenerateQuestionRequest, SubQuestion
from question_generation.queryable.queryable_class import Queryable
from utils.conversion_helper import deserialize_init_args
from utils.faker_helper import generate_data_for_type
from utils.types_helper import GeneratedQuestionClassType
from utils.classes_helper import get_all_subclasses, get_matching_class, get_subtopic_class
from utils.exceptions import handle_exceptions
from utils.user__code_helper import load_user_class
from utils.variable_helper import get_algo_variables, get_query_variables

@handle_exceptions
def generate_input(input_path: Dict[str, Any], variable_options: Dict[str, Any], input_classes: Dict[str, Dict[str, Any]], input_init: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Generate a variable for a given class."""

    def traverse_path(path: Dict[str, Any], classes: Dict[str, Any]) -> Any:
        """Recursively traverse the input path to find the corresponding class."""
        for key, subpath in path.items():
            if key in classes:
                if isinstance(subpath, dict):
                    return traverse_path(subpath, classes[key])
                else:
                    return classes[key].get(subpath)
        return None
    try:
        cls = traverse_path(input_path, input_classes)
        if input_init:
            input_generated_data = cls(**input_init[cls.__name__]) if input_init.get(cls.__name__) else cls()
        else:
            input_generated_data = cls(**(variable_options[cls.__name__])) if variable_options.get(cls.__name__) else cls()
        input_generated_data_init = input_generated_data.get_init_args()
        return {
            'context': { cls.__name__: input_generated_data },
            'context_init': { cls.__name__: input_generated_data_init },
            'cls': cls ,
            'cls_instance': input_generated_data,
        }
    except Exception as e:
        print(f"Error generating variable: {e}")
        return {}

@handle_exceptions
def generate_variable(
    autoloaded_classes: Dict[str, Dict[str, GeneratedQuestionClassType]],
    topic: str,
    subtopic: str,
    arguments: Dict[str, Any],
    element_type: Dict[str, str],
    subclasses: Dict[str, str],
    question_description: str,
    arguments_init: Optional[Dict[str, Any]] = None,
    userAlgoCode: Optional[str] = None,
    userEnvCode: Optional[str] = None,
    userQueryableCode: Optional[str] = None
) -> Dict[str, Any]:
    if userAlgoCode:
        cls = load_user_class(userAlgoCode, userQueryableCode)
    else:
        cls = get_subtopic_class(autoloaded_classes, topic, subtopic)
    cls_instance = cls()
    algo_variables = get_algo_variables(cls)
    for var in algo_variables:
        if var["name"] in subclasses:
            subclass_type = get_matching_class(get_all_subclasses(var["type"]), subclasses[var["name"]])
            if subclass_type:
                var['type'] = subclass_type
    try:
        algo_generated_data = {}
        filtered_variables = [var for var in algo_variables if not arguments_init or var["name"] not in arguments_init]
        algo_generated_data = generate_data(filtered_variables, element_type, arguments)
        if arguments_init:
            for key, value in arguments_init.items():
                var_type = next((v["type"] for v in algo_variables if v["name"] == key), None)
                if var_type:
                    algo_generated_data[key] = var_type(**deserialize_init_args(value)) if isinstance(value, dict) else var_type(value)
                else:
                    algo_generated_data[key] = value
        algo_generated_data_init = {
            key: value.get_init_args() if hasattr(value, 'get_init_args') else value
            for key, value in algo_generated_data.items()
        }
        for key, value in algo_generated_data_init.items():
            if key in arguments:
                for innerKey, innerValue in value.items():
                    if innerKey in arguments[key] and callable(innerValue):
                        algo_generated_data_init[key][innerKey] = arguments[key][innerKey]
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
    input_classes: Dict[str, Dict[str, Type]]
) -> Dict[str, Any]:
    try:
        result = {}
        outerContext = deepcopy(request.context)
        outer = {}
        if request.context.selectedTopic and request.context.selectedSubtopic:
            outer = generate_variable(
                autoloaded_classes,
                request.context.selectedTopic,
                request.context.selectedSubtopic,
                request.context.arguments,
                request.context.selectedQuantifiables,
                request.context.selectedSubclasses,
                request.description,
                arguments_init=request.context.argumentsInit,
                userAlgoCode=request.context.userAlgoCode
            )

        outerInput = {}
        if request.context.inputPath:
            outerInput = generate_input(request.context.inputPath, request.context.inputArguments, input_classes, input_init=request.context.inputInit)

        result['description'] = outer['description'] if outer['description'] else ''
        if outer['context']:
            # Generate SVG for main question
            svg_content = generate_svg(outer['context'])
            if svg_content:
                result['svg'] = svg_content
        if request.sub_questions:
            result['subquestions'] = [
                generate_subquestion(autoloaded_classes, outer, outerContext, subquestion, outerInput, input_classes)
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
    subquestion: SubQuestion,
    outerInput: Dict[str, Any],
    input_classes: Dict[str, Dict[str, Type]]
):
    if subquestion.queryable:
        return generate_subquestion_queryable(
            autoloaded_classes,
            outer,
            outerContext,
            subquestion
        )
    elif subquestion.inputQueryable:
        return generate_subquestion_input_queryable(
            input_classes,
            subquestion,
            outerInput,
        )

def generate_subquestion_input_queryable(
    input_classes: Dict[str, Dict[str, Type]],
    subquestion: SubQuestion,
    outerInput: Dict[str, Any]
) -> Dict[str, Any]:
    try:
        if subquestion.context.inputPath:
            inner = generate_input(
                subquestion.context.inputPath,
                subquestion.context.inputArguments,
                input_classes,
                subquestion.context.inputInit
            )
            sub_input_variable = inner['context']
            cls_instance = inner['cls_instance']
            cls = inner['cls']
        else:
            sub_input_variable = outerInput['context']
            cls_instance = outerInput['cls_instance']
            cls = outerInput['cls']
        query_variables = get_query_variables(cls, subquestion.inputQueryable)
        sub = {}
        try:
            sub['answer'], query_generated_data, answer_svg_content = process_input_query_result(
                cls_instance,
                subquestion.inputQueryable,
                query_variables,
                subquestion.context.inputArguments
            )
        except Exception as e:
            print(f"Error processing query result: {e}")
            return {}
        sub['description'] = cls_instance.format_question_description(
            subquestion.description,
            {**query_generated_data}
        )
        options = [sub['answer']]
        for _ in range(subquestion.questionDetails.number_of_options - 1):
            try:
                option = generate_input_query_options(
                    cls_instance,
                    subquestion.inputQueryable,
                    {},
                    query_variables,
                    sub['answer'],
                    subquestion.context.inputArguments
                )
                options.append(option)
            except Exception as e:
                print(f"Error generating option: {e}")
                continue
        sub['options'] = options
        sub['marks'] = subquestion.questionDetails.marks
        return sub
    except Exception as e:
        print(f"Error generating subquestion input queryable: {e}")
        return {}

def generate_subquestion_queryable(
    autoloaded_classes: Dict[str, Dict[str, Any]],
    outer: Dict[str, Any],
    outerContext: ContextRequest,
    subquestion: SubQuestion,
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
                arguments_init=subquestion.context.argumentsInit if subquestion.context.argumentsInit else outerContext.argumentsInit,
                userAlgoCode=subquestion.context.userAlgoCode,
                userEnvCode=subquestion.context.userEnvCode,
                userQueryableCode=subquestion.userQueryableCode
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
        svg_content = generate_svg(copy_algo_generated_data, subquestion.queryable)
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
        return '', {}, {}, {}

def process_input_query_result(cls_instance, queryable_type, query_variables, arguments):
    try:
        query_result = cls_instance.query_all()
        for base, query_method, generate_input in query_result:
            if base.__name__ == queryable_type and issubclass(base, Queryable):
                query_base, query_method = base, query_method
                base_instance = query_base()
                copy_attributes(cls_instance, base_instance)
                if generate_input:
                    generated_input = generate_input(base_instance)
                    query_generated_data = { query_variables[0]['name']: generated_input }
                else:
                    query_generated_data = generate_data(query_variables, {}, arguments)
                query_output = query_method(base_instance, **deepcopy(query_generated_data))
                value, graph = query_output['value'], query_output['svg']
                return str(value), query_generated_data, graph
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

def generate_input_query_options(cls_instance, queryable_type, element_type, query_variables, query_answer, arguments):
    query_result_option, _, _ = process_input_query_result(cls_instance, queryable_type, query_variables, arguments)
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


def generate_svg(algo_generated_data, queryable_type=None) -> Dict[str, Optional[str]]:
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
            to_graph_method = getattr(instance, 'to_graph')
            to_graph_signature = inspect.signature(to_graph_method)
            if 'label_edges' in to_graph_signature.parameters:
                label_edges = queryable_type == 'Pruned'
                svg_content['graph'] = to_graph_method(label_edges=label_edges)
            else:
                svg_content['graph'] = to_graph_method()
        if hasattr(instance, 'to_table') and callable(getattr(instance, 'to_table')):
            svg_content['table'] = instance.to_table()

    return svg_content if svg_content else None
