from typing import Any, List, Optional

def load_user_class(userAlgoCode: str, userQueryableCode: Optional[str] = None, userEnvCode: Optional[List[str]] = None) -> Any:
    namespace = {}
    try:
        if userEnvCode:
            for env_code in userEnvCode:
                exec(env_code, namespace)
        if userQueryableCode:
            exec(userQueryableCode, namespace)
        exec(userAlgoCode, namespace)

        user_classes = {k: v for k, v in namespace.items() if isinstance(v, type)}
        if not user_classes:
            raise ValueError("No valid class found in user-defined code")
        return next(reversed(user_classes.values()))
    except Exception as e:
        raise ValueError(f"Error loading user-defined class: {e}")

def load_input_class(userEnvCode: str) -> Any:
    namespace = {}
    try:
        exec(userEnvCode, namespace)
        input_classes = {k: v for k, v in namespace.items() if isinstance(v, type)}
        if not input_classes:
            raise ValueError("No valid class found in user-defined code")

        return next(reversed(input_classes.values()))
    except Exception as e:
        raise ValueError(f"Error loading user-defined class: {e}")
