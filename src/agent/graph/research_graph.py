from langgraph.graph import StateGraph, END
from src.agent.services.model_services import ModelService
from src.agent.services.search_service import SearchService
from src.agent.services.analysis_service import AnalysisService

from src.agent.graph.state import ResearchState, initialize_research_state
from src.agent.graph.nodes.search_node import SearchNode
from src.agent.graph.nodes.extraction_node import ExtractionNode
from src.agent.graph.nodes.risk_analysis_node import RiskAnalysisNode
from src.agent.graph.nodes.connection_mapping_node import ConnectionMappingNode
from src.agent.graph.nodes.validation_node import ValidationNode
from src.agent.graph.nodes.planning_node import PlanningNode
from src.agent.graph.nodes.report_node import ReportNode
from src.agent.graph.router import ConditionalRouter


class ResearchGraphBuilder:
    """Builder class for creating the research workflow graph"""

    def __init__(self):
        self.model_service = ModelService()
        self.search_service = SearchService()
        self.analysis_service = AnalysisService()
        self._initialize_nodes()

    def _initialize_nodes(self):
        """Initialize all workflow nodes"""
        self.search_node = SearchNode(self.search_service)
        self.extraction_node = ExtractionNode(self.model_service)
        self.risk_analysis_node = RiskAnalysisNode(self.model_service)
        self.connection_mapping_node = ConnectionMappingNode(self.model_service)
        self.validation_node = ValidationNode(self.model_service)
        self.planning_node = PlanningNode(self.analysis_service)
        self.report_node = ReportNode(self.model_service)

    def build(self) -> StateGraph:
        """Build and return the compiled workflow graph"""
        workflow = StateGraph(ResearchState)

        self._add_nodes(workflow)
        self._configure_edges(workflow)
        app = workflow.compile()
        return app

    def _add_nodes(self, workflow: StateGraph):
        """Add all nodes to the workflow"""
        workflow.add_node("search", self.search_node.execute)
        workflow.add_node("extract", self.extraction_node.execute)
        workflow.add_node("analyze_risks", self.risk_analysis_node.execute)
        workflow.add_node("map_connections", self.connection_mapping_node.execute)
        workflow.add_node("validate", self.validation_node.execute)
        workflow.add_node("plan_next", self.planning_node.execute)
        workflow.add_node("generate_report", self.report_node.execute)

    def _configure_edges(self, workflow: StateGraph):
        """Configure workflow edges and routing"""
        workflow.set_entry_point("search")

        # Linear flow through analysis nodes
        workflow.add_edge("search", "extract")
        workflow.add_edge("extract", "analyze_risks")
        workflow.add_edge("analyze_risks", "map_connections")
        workflow.add_edge("map_connections", "validate")
        workflow.add_edge("validate", "plan_next")

        # Conditional routing from planning
        workflow.add_conditional_edges(
            "plan_next",
            ConditionalRouter.should_continue_searching,
            {"search": "search", "report": "generate_report"},
        )

        workflow.add_edge("generate_report", END)


def create_research_graph():
    """Create the LangGraph workflow for research investigation"""
    builder = ResearchGraphBuilder()
    return builder.build()
