import json
import asyncio
from typing import AsyncGenerator, Dict, Any
from src.agent.graph.research_graph import create_research_graph
from src.agent.graph.state import initialize_research_state, ResearchState
from src.agent.llm_services.strategies.gpt_strategy import GPT4Strategy


class SearchManager:
    """Manages deep search operations with streaming capabilities"""

    def __init__(self):
        try:
            self.research_graph = create_research_graph()
            self.gpt4 = GPT4Strategy()
            self.initialized = True
        except Exception as e:
            print(f"Warning: Failed to initialize research graph: {e}")
            self.research_graph = None
            self.gpt4 = None
            self.initialized = False

    async def stream_search_results(self, query: str) -> AsyncGenerator[str, None]:
        """Stream search results as they're generated"""
        try:
            # Check if properly initialized
            if not self.initialized or not self.research_graph:
                yield self._format_stream_data(
                    {
                        "type": "error",
                        "message": "Search service not properly initialized. Please check API keys configuration.",
                        "error": True,
                    }
                )
                return

            # Step 1: AI Thinking Phase
            yield self._format_stream_data(
                {
                    "type": "thinking_start",
                    "message": "AI is analyzing your query and planning the research approach...",
                    "progress": 5,
                    "step": "thinking",
                }
            )

            # Stream thinking process
            thinking_content = ""
            async for thinking_chunk in self._stream_thinking_process(query):
                thinking_content += thinking_chunk
                yield self._format_stream_data(
                    {
                        "type": "thinking_update",
                        "content": thinking_chunk,
                        "accumulated_thinking": thinking_content,
                        "progress": 10,
                        "step": "thinking",
                    }
                )

            yield self._format_stream_data(
                {
                    "type": "thinking_complete",
                    "message": "Analysis complete. Starting deep search...",
                    "thinking_summary": thinking_content,
                    "progress": 15,
                    "step": "thinking_complete",
                }
            )

            # Step 2: Initialize research state
            initial_state = initialize_research_state(query)

            # Yield initial status
            yield self._format_stream_data(
                {
                    "type": "status",
                    "message": f"Starting deep search for: {query}",
                    "progress": 20,
                    "step": "initialization",
                }
            )

            # Step 3: Execute graph with streaming
            async for update in self._execute_graph_with_streaming(initial_state):
                # Adjust progress to account for thinking phase (20% already used)
                if "progress" in update:
                    update["progress"] = 20 + (update["progress"] * 0.8)
                yield self._format_stream_data(update)

        except Exception as e:
            yield self._format_stream_data(
                {"type": "error", "message": f"Search failed: {str(e)}", "error": True}
            )

    async def _execute_graph_with_streaming(
        self, initial_state: ResearchState
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Execute the research graph with streaming updates"""
        current_state = initial_state
        step_count = 0
        max_steps = 15  # Prevent infinite loops - increased to accommodate relevance evaluation

        # Map node names to user-friendly descriptions
        node_descriptions = {
            "search": "Searching for information",
            "extract": "Extracting key facts",
            "evaluate_relevance": "Evaluating search relevance",
            "analyze_risks": "Analyzing potential risks",
            "map_connections": "Mapping entity connections",
            "validate": "Validating information sources",
            "plan_next": "Planning next search steps",
            "generate_report": "Generating final report",
        }

        try:
            # Run the graph and capture intermediate states
            for chunk in self.research_graph.stream(current_state):
                step_count += 1

                if step_count > max_steps:
                    yield {
                        "type": "warning",
                        "message": "Maximum steps reached, finalizing results",
                        "progress": 95,
                    }
                    break

                # Extract node name and state from chunk
                node_name = list(chunk.keys())[0] if chunk else "unknown"
                updated_state = chunk.get(node_name, current_state)
                current_state = updated_state

                # Calculate progress
                progress = min(90, (step_count / max_steps) * 90)

                # Yield progress update
                yield {
                    "type": "progress",
                    "step": node_name,
                    "description": node_descriptions.get(
                        node_name, f"Processing {node_name}"
                    ),
                    "progress": progress,
                    "iteration": current_state.get("iteration", 0),
                    "results_count": len(current_state.get("search_results", [])),
                    "facts_count": sum(
                        len(facts) for facts in current_state.get("facts", {}).values()
                    ),
                    "risks_count": len(current_state.get("risks", [])),
                    "connections_count": sum(
                        len(conn)
                        for conn in current_state.get("connections", {}).values()
                    ),
                }

                # Yield specific updates based on node type
                if node_name == "search":
                    yield {
                        "type": "search_update",
                        "message": f"Found {len(current_state.get('search_results', []))} search results",
                        "search_results": current_state.get("search_results", [])[
                            :3
                        ],  # Show first 3
                    }

                elif node_name == "extract":
                    yield {
                        "type": "extraction_update",
                        "message": "Extracted key facts from sources",
                        "facts": current_state.get("facts", {}),
                        "confidence_scores": current_state.get("confidence_scores", {}),
                    }

                elif node_name == "evaluate_relevance":
                    relevance_scores = current_state.get("relevance_scores", [])
                    latest_score = relevance_scores[-1] if relevance_scores else {}
                    needs_enhancement = current_state.get("needs_enhanced_search", False)
                    
                    yield {
                        "type": "relevance_update",
                        "message": f"Relevance evaluation: {latest_score.get('overall_score', 0):.2f} - {'Enhancing search' if needs_enhancement else 'Proceeding with analysis'}",
                        "relevance_score": latest_score.get('overall_score', 0),
                        "needs_enhancement": needs_enhancement,
                    }

                elif node_name == "analyze_risks":
                    yield {
                        "type": "risk_analysis_update",
                        "message": f"Identified {len(current_state.get('risks', []))} potential risks",
                        "risks": current_state.get("risks", []),
                    }

                elif node_name == "map_connections":
                    yield {
                        "type": "connection_update",
                        "message": "Mapped entity relationships",
                        "connections": current_state.get("connections", {}),
                    }

                elif node_name == "validate":
                    yield {
                        "type": "validation_update",
                        "message": "Validated information sources",
                        "validation_summary": "Source validation completed",
                    }

                elif node_name == "plan_next":
                    next_queries = current_state.get("next_queries", [])
                    if next_queries:
                        yield {
                            "type": "planning_update",
                            "message": f"Planning {len(next_queries)} additional searches",
                            "next_queries": next_queries,
                        }
                    else:
                        yield {
                            "type": "planning_update",
                            "message": "Search complete, generating final report",
                            "next_queries": [],
                        }

                elif node_name == "generate_report":
                    report_content = current_state.get("report", "")
                    yield {
                        "type": "report_ready",
                        "message": "Final report generated",
                        "report": report_content,
                        "progress": 100,
                    }

                # Small delay to make streaming visible
                await asyncio.sleep(0.1)

            # Final completion update
            yield {
                "type": "completion",
                "message": "Deep search completed successfully",
                "progress": 100,
                "final_state": {
                    "target": current_state.get("target"),
                    "total_results": len(current_state.get("search_results", [])),
                    "facts_found": sum(
                        len(facts) for facts in current_state.get("facts", {}).values()
                    ),
                    "risks_identified": len(current_state.get("risks", [])),
                    "connections_mapped": sum(
                        len(conn)
                        for conn in current_state.get("connections", {}).values()
                    ),
                    "iterations": current_state.get("iteration", 0),
                    "report": current_state.get("report", ""),
                },
            }

        except Exception as e:
            yield {
                "type": "error",
                "message": f"Graph execution failed: {str(e)}",
                "error": True,
            }

    async def _mock_streaming_demo(
        self, query: str
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Mock streaming demo for testing when API keys are not available"""
        steps = [
            (
                "search",
                "Searching for information",
                {
                    "search_results": [
                        {
                            "title": f"Mock result for {query}",
                            "url": "http://example.com",
                            "content": "Mock search content",
                        }
                    ]
                },
            ),
            (
                "extract",
                "Extracting key facts",
                {"facts": {"key_facts": ["Mock fact 1", "Mock fact 2"]}},
            ),
            (
                "analyze_risks",
                "Analyzing potential risks",
                {"risks": [{"type": "Low", "description": "Mock risk"}]},
            ),
            (
                "map_connections",
                "Mapping entity connections",
                {"connections": {"entities": ["Mock entity 1"]}},
            ),
            ("validate", "Validating information sources", {}),
            ("plan_next", "Planning next search steps", {"next_queries": []}),
            (
                "generate_report",
                "Generating final report",
                {"report": f"Mock research report for {query}"},
            ),
        ]

        for i, (step_name, description, mock_data) in enumerate(steps):
            progress = int((i + 1) / len(steps) * 100)

            yield {
                "type": "progress",
                "step": step_name,
                "description": description,
                "progress": progress,
                "iteration": 1,
                "results_count": len(mock_data.get("search_results", [])),
                "facts_count": len(mock_data.get("facts", {})),
                "risks_count": len(mock_data.get("risks", [])),
                "connections_count": len(mock_data.get("connections", {})),
            }

            if step_name == "search":
                yield {
                    "type": "search_update",
                    "message": "Found mock search results",
                    "search_results": mock_data.get("search_results", []),
                }
            elif step_name == "generate_report":
                yield {
                    "type": "report_ready",
                    "message": "Mock report generated",
                    "report": mock_data.get("report", ""),
                    "progress": 100,
                }

            await asyncio.sleep(0.5)  # Visible delay for demo

        yield {
            "type": "completion",
            "message": "Mock deep search completed successfully",
            "progress": 100,
            "final_state": {
                "target": query,
                "total_results": 1,
                "facts_found": 2,
                "risks_identified": 1,
                "connections_mapped": 1,
                "iterations": 1,
                "report": f"Mock research report for {query}",
            },
        }

    async def _stream_thinking_process(self, query: str) -> AsyncGenerator[str, None]:
        """Stream the AI thinking process about the query"""
        try:
            async for chunk in self._fallback_thinking_simulation(query):
                yield chunk

        except Exception as e:
            yield f"Thinking process error: {str(e)}\nProceeding with standard research approach...\n"

    async def _fallback_thinking_simulation(
        self, query: str
    ) -> AsyncGenerator[str, None]:
        """Fallback thinking simulation when GPT-4 is not available"""
        thinking_steps = [
            f"Let me analyze the query: '{query}'...\n\n",
            "I need to consider multiple research angles:\n",
            "• Direct factual information and primary sources\n",
            "• Related entities, connections, and relationships\n",
            "• Potential risks, concerns, or controversial aspects\n",
            "• Historical context and background information\n",
            "• Current developments and recent updates\n\n",
            "Planning optimal search strategy:\n",
            "1. Start with broad comprehensive search\n",
            "2. Extract and validate key facts\n",
            "3. Analyze risks and map connections\n",
            "4. Conduct targeted follow-up searches\n",
            "5. Generate comprehensive report\n\n",
            "Ready to begin deep research process...\n",
        ]

        for step in thinking_steps:
            yield step
            await asyncio.sleep(0.5)  # Slightly longer delay for readability

    def _format_stream_data(self, data: Dict[str, Any]) -> str:
        """Format data for SSE streaming"""
        return f"data: {json.dumps(data)}\n\n"
