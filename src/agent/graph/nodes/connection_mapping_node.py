from src.agent.graph.base_node import BaseResearchNode
from src.agent.graph.state import ResearchState
from src.agent.services.model_services import ModelService


class ConnectionMappingNode(BaseResearchNode):
    """Handles connection mapping between entities"""

    CONNECTION_TYPES = ["people", "organizations", "events", "locations"]

    def __init__(self, model_service: ModelService):
        super().__init__("Connection Mapping Node")
        self.model_service = model_service

    def execute(self, state: ResearchState) -> ResearchState:
        """Map connections (Functional Spec 3)"""
        self.log("Starting connection mapping")

        connections = self.model_service.map_connections(state["facts"])
        state["connections"] = connections

        self._log_connection_summary(connections)
        return state

    def _log_connection_summary(self, connections: dict) -> None:
        """Log summary of mapped connections"""
        total_connections = sum(
            [len(connections.get(conn_type, [])) for conn_type in self.CONNECTION_TYPES]
        )

        self.log(f"Mapped {total_connections} total connections")
        for conn_type in self.CONNECTION_TYPES:
            count = len(connections.get(conn_type, []))
            self.log(f"- {conn_type.title()}: {count}")
