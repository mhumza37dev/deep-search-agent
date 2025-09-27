from src.agent.graph.base_node import BaseResearchNode
from src.agent.graph.state import ResearchState
from src.agent.services.model_services import ModelService


class RiskAnalysisNode(BaseResearchNode):
    """Handles risk pattern recognition"""

    def __init__(self, model_service: ModelService):
        super().__init__("Risk Analysis Node")
        self.model_service = model_service

    def execute(self, state: ResearchState) -> ResearchState:
        """Risk pattern recognition (Functional Spec 2)"""
        self.log("Starting risk analysis")

        risks = self.model_service.analyze_risks(state["facts"])
        state["risks"] = risks

        self._log_risk_summary(risks)
        return state

    def _log_risk_summary(self, risks: list) -> None:
        """Log summary of identified risks"""
        self.log(f"Identified {len(risks)} potential risks")

        for risk in risks[:3]:  # Show first 3 risks
            severity = risk.get("severity", "UNKNOWN")
            description = risk.get("risk", "No description")[:50]
            self.log(f"- {severity}: {description}...")
