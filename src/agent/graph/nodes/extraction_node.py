from src.agent.graph.base_node import BaseResearchNode
from src.agent.graph.state import ResearchState
from src.agent.services.model_services import ModelService


class ExtractionNode(BaseResearchNode):
    """Handles fact extraction from search results"""

    FACT_TYPES = ["biographical", "professional", "financial", "behavioral"]

    def __init__(self, model_service: ModelService):
        super().__init__("Fact Extraction Node")
        self.model_service = model_service

    def execute(self, state: ResearchState) -> ResearchState:
        """Extract all fact types (Functional Spec 1)"""
        self.log("Starting fact extraction")

        facts = {}
        for fact_type in self.FACT_TYPES:
            facts[fact_type] = self._extract_facts_by_type(
                state["search_results"], fact_type
            )

        state["facts"] = facts
        return state

    def _extract_facts_by_type(self, search_results: list, fact_type: str) -> list:
        """Extract facts for a specific type"""
        self.log(f"Extracting {fact_type} facts...")
        extracted_facts = self.model_service.extract_facts(search_results, fact_type)
        self.log(f"Found {len(extracted_facts)} {fact_type} facts")
        return extracted_facts
