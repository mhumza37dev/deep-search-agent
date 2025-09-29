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

    @staticmethod
    def should_enhance_search(state: ResearchState) -> str:
        """Determine if search needs enhancement based on relevance evaluation"""
        needs_enhancement = state.get("needs_enhanced_search", False)
        
        if needs_enhancement:
            print("Search results not relevant enough, enhancing search")
            return "search"
        else:
            print("Search results are relevant, continuing to analysis")
            return "continue"
