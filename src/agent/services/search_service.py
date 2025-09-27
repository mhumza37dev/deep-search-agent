from typing import List, Dict
from tavily import TavilyClient
from src.config.app_config import config


class SearchService:
    """Handle all search operations"""

    def __init__(self):
        self.tavily_client = TavilyClient(api_key=config.TAVILY_API_KEY)

    def comprehensive_search(self, target: str) -> List[Dict]:
        """Multi-source search for target"""
        all_results = []

        queries = self._generate_initial_queries(target)

        for query in queries:
            results = self._tavily_search(query)
            all_results.extend(results)

        return self._deduplicate_results(all_results)

    def targeted_search(self, queries: List[str]) -> List[Dict]:
        """Focused search based on specific queries"""
        all_results = []

        for query in queries[: config.MAX_SEARCH_RESULTS]:
            results = self._tavily_search(query)
            all_results.extend(results)

        return self._deduplicate_results(all_results)

    def _generate_initial_queries(self, target: str) -> List[str]:
        """Generate comprehensive search queries"""
        base_queries = [
            f'"{target}"',
            f"{target} biography",
            f"{target} career history",
            f"{target} company CEO",
            f"{target} investments",
            f"{target} board positions",
            f"{target} controversies",
            f"{target} linkedin",
            f"{target} net worth",
            f"{target} news",
            f"{target} financial connections",
            f"{target} behavioral patterns",
        ]
        return base_queries

    def _tavily_search(self, query: str) -> List[Dict]:
        """Search using Tavily API"""
        try:
            response = self.tavily_client.search(
                query=query,
                search_depth="advanced",
                max_results=config.MAX_SEARCH_RESULTS,
            )

            results = []
            for result in response.get("results", []):
                results.append(
                    {
                        "url": result.get("url", ""),
                        "title": result.get("title", ""),
                        "content": result.get("content", ""),
                        "query": query,
                        "score": result.get("score", 0.5),
                    }
                )

            return results

        except Exception as e:
            print(f"Error in Tavily search for '{query}': {e}")
            return []

    def _deduplicate_results(self, results: List[Dict]) -> List[Dict]:
        """Remove duplicate results"""
        seen_urls = set()
        unique_results = []

        for result in results:
            url = result.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)

        return unique_results
