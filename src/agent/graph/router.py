from src.agent.graph.state import ResearchState


class ConditionalRouter:
    """Handles conditional routing logic for the research graph"""

    @staticmethod
    def should_continue_searching(state: ResearchState) -> str:
        """Determine next workflow step based on state"""
        has_queries = bool(state.get("next_queries"))

        if has_queries:
            print("Continuing to search")
            return "search"
        else:
            print("Moving to report generation")
            return "report"
