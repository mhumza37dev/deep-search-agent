from src.agent.llm_services.strategies.gpt_strategy import GPT4Strategy
from src.agent.graph.base_node import BaseResearchNode
from src.agent.graph.state import ResearchState
from src.agent.services.model_services import ModelService
from typing import List, Dict, Any


class RelevanceEvaluationNode(BaseResearchNode):
    """Evaluates search results relevance and enhances query if needed"""

    def __init__(self, model_service: ModelService):
        super().__init__("Relevance Evaluation Node")
        self.gpt4 = GPT4Strategy()

    def execute(self, state: ResearchState) -> ResearchState:
        """Evaluate search results relevance and determine if re-search is needed"""
        self.log(f"Evaluating relevance of {len(state['search_results'])} search results")
        
        # Track relevance evaluation attempts for POC
        if "relevance_attempts" not in state:
            state["relevance_attempts"] = 0
        state["relevance_attempts"] += 1
        
        # Evaluate relevance of current search results
        relevance_score = self._evaluate_relevance(state)
        
        # Store relevance score in state
        if "relevance_scores" not in state:
            state["relevance_scores"] = []
        state["relevance_scores"].append(relevance_score)
        
        self.log(f"Relevance score: {relevance_score['overall_score']:.2f} (Attempt {state['relevance_attempts']})")
        
        # POC: Pass on second attempt regardless of score
        if state["relevance_attempts"] >= 2:
            self.log("POC: Passing after second attempt regardless of relevance score")
            state["needs_enhanced_search"] = False
        elif relevance_score["overall_score"] < 0.6:  # Threshold for relevance
            self.log("Low relevance detected, enhancing search query")
            enhanced_queries = self._enhance_search_query(state, relevance_score)
            state["next_queries"] = enhanced_queries
            state["needs_enhanced_search"] = True
        else:
            self.log("Search results are sufficiently relevant")
            state["needs_enhanced_search"] = False
            
        return state

    def _evaluate_relevance(self, state: ResearchState) -> Dict[str, Any]:
        """Evaluate how relevant the search results are to the target query"""
        
        # Prepare search results summary for evaluation
        results_summary = self._prepare_results_summary(state["search_results"])
        
        evaluation_prompt = f"""
        Evaluate the relevance of the following search results to the target query.
        
        Target Query: "{state['target']}"
        
        Search Results Summary:
        {results_summary}
        
        Please evaluate:
        1. How well do these results match the specific person/entity mentioned in the query?
        2. How well do they match the context (job role, company.) mentioned in the query?
        3. Are there any irrelevant or off-topic results?
        4. What specific information is missing that would make the results more complete?
        
        Provide your evaluation in the following JSON format:
        {{
            "overall_score": <float between 0 and 1>,
            "person_match_score": <float between 0 and 1>,
            "context_match_score": <float between 0 and 1>,
            "completeness_score": <float between 0 and 1>,
            "irrelevant_results_count": <integer>,
            "missing_information": ["list", "of", "missing", "aspects"],
            "reasoning": "explanation of the scores"
        }}
        """
        
        try:
            response = self.gpt4.invoke([{"role": "user", "content": evaluation_prompt}])
            if "```json" in response.lower():
                response = response.split("```json")[1].split("```")[0].strip()
            # Parse the JSON response
            import json
            relevance_data = json.loads(response.strip())
            
            return relevance_data
            
        except Exception as e:
            self.log(f"Error evaluating relevance: {str(e)}", "ERROR")
            # Return default low relevance score on error
            return {
                "overall_score": 0.3,
                "person_match_score": 0.3,
                "context_match_score": 0.3,
                "completeness_score": 0.3,
                "irrelevant_results_count": 0,
                "missing_information": ["Unable to evaluate due to error"],
                "reasoning": f"Evaluation failed: {str(e)}"
            }

    def _prepare_results_summary(self, search_results: List[Dict]) -> str:
        """Prepare a concise summary of search results for evaluation"""
        if not search_results:
            return "No search results found."
            
        summary_parts = []
        for i, result in enumerate(search_results[:10]):  # Limit to first 10 results
            title = result.get('title', 'No title')
            snippet = result.get('snippet', result.get('description', 'No description'))
            # Truncate snippet if too long
            if len(snippet) > 200:
                snippet = snippet[:200] + "..."
            
            summary_parts.append(f"{i+1}. Title: {title}\n   Summary: {snippet}")
            
        if len(search_results) > 10:
            summary_parts.append(f"... and {len(search_results) - 10} more results")
            
        return "\n\n".join(summary_parts)

    def _enhance_search_query(self, state: ResearchState, relevance_score: Dict[str, Any]) -> List[str]:
        """Generate enhanced search queries based on relevance evaluation"""
        
        missing_info = relevance_score.get("missing_information", [])
        original_target = state["target"]
        
        enhancement_prompt = f"""
        Based on the relevance evaluation, the original search query needs enhancement.
        
        Original Query: "{original_target}"
        Missing Information: {missing_info}
        Relevance Issues: {relevance_score.get('reasoning', 'Low relevance detected')}
        
        Generate 3-5 enhanced search queries that would help find more relevant information.
        The queries should:
        1. Be more specific and targeted
        2. Include alternative search terms or synonyms
        3. Address the missing information identified
        4. Use different search strategies (exact phrases, related terms, etc.)
        
        Provide the enhanced queries as a JSON array of strings:
        ["query1", "query2", "query3", ...]
        
        Example for "Deep search on Ali Wahab who worked at Tapmad as software engineer":
        [
            "Ali Wahab software engineer Tapmad",
            "\"Ali Wahab\" Tapmad developer",
            "Ali Wahab programmer Tapmad Pakistan",
            "Tapmad engineering team Ali Wahab",
            "Ali Wahab software development Tapmad"
        ]
        """
        
        try:
            response = self.gpt4.invoke([{"role": "user", "content": enhancement_prompt}])
            if "```json" in response.lower():
                response = response.split("```json")[1].split("```")[0].strip()

            # Parse the JSON response
            import json
            enhanced_queries = json.loads(response.strip())
            
            # Ensure we have a list of strings
            if isinstance(enhanced_queries, list):
                return enhanced_queries
            else:
                self.log("Invalid response format for enhanced queries", "WARNING")
                return self._generate_fallback_queries(original_target)
                
        except Exception as e:
            self.log(f"Error generating enhanced queries: {str(e)}", "ERROR")
            return self._generate_fallback_queries(original_target)

    def _generate_fallback_queries(self, original_target: str) -> List[str]:
        """Generate fallback enhanced queries using simple heuristics"""
        # Simple fallback strategy - create variations of the original query
        base_terms = original_target.lower().split()
        
        fallback_queries = [
            f'"{original_target}"',  # Exact phrase search
            original_target + " profile",
            original_target + " background",
            original_target + " professional",
            original_target + " career"
        ]
        
        return fallback_queries[:3]  # Return top 3 fallback queries
