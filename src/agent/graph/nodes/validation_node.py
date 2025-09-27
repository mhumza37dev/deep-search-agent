from src.agent.graph.base_node import BaseResearchNode
from src.agent.graph.state import ResearchState
from src.agent.services.model_services import ModelService


class ValidationNode(BaseResearchNode):
    """Handles source validation and confidence scoring"""

    def __init__(self, model_service: ModelService):
        super().__init__("Source Validation Node")
        self.model_service = model_service

    def execute(self, state: ResearchState) -> ResearchState:
        """Source validation (Functional Spec 4)"""
        self.log("Starting source validation")

        confidence_scores = self.model_service.validate_sources(
            state["facts"], state["search_results"]
        )
        state["confidence_scores"] = confidence_scores

        self._log_validation_summary(confidence_scores)
        return state

    def _log_validation_summary(self, confidence_scores: dict) -> None:
        """Log validation results summary"""
        fact_confidence = confidence_scores.get("fact_confidence", {})

        if fact_confidence:
            avg_confidence = sum(fact_confidence.values()) / len(fact_confidence)
            self.log(f"Average fact confidence: {avg_confidence:.2f}")

        inconsistencies = confidence_scores.get("inconsistencies", [])
        self.log(f"Found {len(inconsistencies)} inconsistencies")
