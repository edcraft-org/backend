from typing import Any, Optional

def load_user_class(userAlgoCode: str, userQueryableCode: Optional[str] = None) -> Any:
    namespace = {}
    try:
        if userQueryableCode:
            exec(userQueryableCode, namespace)
        exec(userAlgoCode, namespace)

        user_classes = {k: v for k, v in namespace.items() if isinstance(v, type)}
        if not user_classes:
            raise ValueError("No valid class found in user-defined code")

        return next(reversed(user_classes.values()))
    except Exception as e:
        raise ValueError(f"Error loading user-defined class: {e}")
