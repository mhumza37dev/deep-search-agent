from src.agent.graph.base_node import BaseResearchNode
from src.agent.graph.state import ResearchState
from src.agent.services.analysis_service import AnalysisService


class PlanningNode(BaseResearchNode):
    """Handles search planning and iteration decisions"""

    MAX_ITERATIONS = 3
    MAX_SEARCH_RESULTS = 50

    def __init__(self, analysis_service: AnalysisService):
        super().__init__("Planning Node")
        self.analysis_service = analysis_service

    def execute(self, state: ResearchState) -> ResearchState:
        """Determine if more searches are needed"""
        self.log("Analyzing search completeness")

        current_iteration = state.get("iteration", 0)

        if self._should_stop_searching(current_iteration, state):
            state["next_queries"] = []
            return state

        gaps = self.analysis_service.identify_information_gaps(state["facts"])

        if gaps:
            state["next_queries"] = gaps
            self._log_continuation_plan(gaps)
        else:
            state["next_queries"] = []
            self.log("No significant information gaps found")

        return state

    def _should_stop_searching(
        self, current_iteration: int, state: ResearchState
    ) -> bool:
        """Determine if searching should stop"""
        if current_iteration >= self.MAX_ITERATIONS:
            self.log(f"Reached maximum iterations ({self.MAX_ITERATIONS})")
            return True

        if len(state["search_results"]) >= self.MAX_SEARCH_RESULTS:
            self.log(f"Reached maximum search results ({self.MAX_SEARCH_RESULTS})")
            return True

        return False

    def _log_continuation_plan(self, gaps: list) -> None:
        """Log the continuation plan"""
        self.log(f"Identified {len(gaps)} information gaps")
        self.log(f"Next queries: {gaps[:3]}...")
