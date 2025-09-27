from abc import ABC, abstractmethod
from typing import Dict, Any
from src.agent.graph.state import ResearchState


class BaseResearchNode(ABC):
    """Base class for all research graph nodes"""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def execute(self, state: ResearchState) -> ResearchState:
        """Execute the node's logic"""
        pass

    def log(self, message: str, level: str = "INFO"):
        """Centralized logging"""
        print(f"{self.name} - {level}: {message}")
