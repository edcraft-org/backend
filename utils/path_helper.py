from pathlib import Path
from typing import List
from utils.exceptions import handle_exceptions

@handle_exceptions
def get_topics(base_path: str) -> List[str]:
    """Get all topics (folder names) inside the base path."""
    return [p.name for p in Path(base_path).iterdir() if p.is_dir() and not p.name.startswith('__')]

@handle_exceptions
def get_subtopics(topic_path: str) -> List[str]:
    """Get all subtopics (file names) inside the topic path."""
    return [p.name for p in Path(topic_path).glob('*.py') if p.name != '__init__.py']
