from src.agent.graph.base_node import BaseResearchNode
from src.agent.graph.state import ResearchState
from src.agent.services.search_service import SearchService


class SearchNode(BaseResearchNode):
    """Handles comprehensive and targeted search operations"""

    def __init__(self, search_service: SearchService):
        super().__init__("Search Node")
        self.search_service = search_service

    def execute(self, state: ResearchState) -> ResearchState:
        """Comprehensive search phase"""
        self.log(f"Iteration {state.get('iteration', 0)}")

        if not state.get("search_results"):
            self._perform_initial_search(state)
        else:
            self._perform_targeted_search(state)

        self.log(f"Found {len(state['search_results'])} total results")
        return state

    def _perform_initial_search(self, state: ResearchState) -> None:
        """Perform initial broad search"""
        self.log(f"Initial search for: {state['target']}")
        results = self.search_service.comprehensive_search(state["target"])
        state["search_results"] = results
        state["iteration"] = 1

    def _perform_targeted_search(self, state: ResearchState) -> None:
        """Perform targeted follow-up searches"""
        self.log(f"Targeted search with {len(state['next_queries'])} queries")
        results = self.search_service.targeted_search(state["next_queries"])
        state["search_results"].extend(results)
        state["iteration"] = state.get("iteration", 1) + 1
