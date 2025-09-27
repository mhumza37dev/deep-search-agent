from typing import List, Dict
from abc import ABC, abstractmethod


class LLMStrategy(ABC):
    """Abstract base class for LLM strategies"""

    @abstractmethod
    def invoke(self, messages: List[Dict]) -> str:
        pass
