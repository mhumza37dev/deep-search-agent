from src.agent.graph.base_node import BaseResearchNode
from src.agent.graph.state import ResearchState
from src.agent.services.model_services import ModelService


class ReportNode(BaseResearchNode):
    """Handles final report generation"""

    def __init__(self, model_service: ModelService):
        super().__init__("Report Generation Node")
        self.model_service = model_service

    def execute(self, state: ResearchState) -> ResearchState:
        """Generate final report"""
        self.log("Generating final report")

        investigation_data = self._prepare_investigation_data(state)
        report = self.model_service.generate_report(investigation_data)
        if "```html" in report:
            report = report.split("```html")[1].split("```")[0].strip()
        if "```json" in report:
            report = report.split("```json")[1].split("```")[0].strip()
        state["report"] = report

        self.log("Final report generated successfully")
        return state

    def _prepare_investigation_data(self, state: ResearchState) -> dict:
        """Prepare data for report generation"""
        return {
            "target": state["target"],
            "facts": state["facts"],
            "risks": state["risks"],
            "connections": state["connections"],
            "confidence": state["confidence_scores"],
            "total_sources": len(state["search_results"]),
            "search_iterations": state.get("iteration", 0),
        }
