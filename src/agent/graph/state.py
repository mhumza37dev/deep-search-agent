from typing import TypedDict, List, Dict, Any


class ResearchState(TypedDict):
    target: str
    facts: Dict[str, List[Dict]]
    risks: List[Dict]
    connections: Dict[str, List[Dict]]
    confidence_scores: Dict[str, Any]
    search_results: List[Dict]
    next_queries: List[str]
    iteration: int
    report: str


def initialize_research_state(target: str) -> ResearchState:
    """Initialize the research state for a new investigation"""
    return ResearchState(
        target=target,
        facts={},
        risks=[],
        connections={},
        confidence_scores={},
        search_results=[],
        next_queries=[],
        iteration=0,
        report="",
    )
