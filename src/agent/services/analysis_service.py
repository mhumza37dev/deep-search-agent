from typing import List, Dict


class AnalysisService:
    """Core analysis functions"""

    def process_search_results(self, results: List[Dict]) -> Dict:
        """Process and structure raw search data"""
        processed = {
            "total_results": len(results),
            "sources": list(set([r.get("url", "") for r in results])),
            "content_length": sum([len(r.get("content", "")) for r in results]),
            "high_relevance_results": [r for r in results if r.get("score", 0) > 0.7],
        }
        return processed

    def identify_information_gaps(self, current_facts: Dict) -> List[str]:
        """Determine what information is missing and generate new search queries"""
        gaps = []

        fact_categories = {
            "biographical": ["education", "family", "early life"],
            "professional": ["current role", "previous positions", "achievements"],
            "financial": ["investments", "assets", "financial history"],
            "behavioral": ["leadership style", "public positions", "controversies"],
        }

        for category, required_info in fact_categories.items():
            category_facts = current_facts.get(category, [])
            category_text = " ".join(
                [fact.get("fact", "") for fact in category_facts]
            ).lower()

            for info_type in required_info:
                if info_type not in category_text:

                    target_name = self._extract_target_name(current_facts)
                    gaps.append(f"{target_name} {info_type}")

        return gaps[:5]

    def _extract_target_name(self, facts: Dict) -> str:
        """Extract target person's name from facts"""

        biographical = facts.get("biographical", [])
        for fact in biographical:
            fact_text = fact.get("fact", "").lower()
            if "name" in fact_text:

                return fact_text.split("name")[1].strip().split()[0:2]

        return "target person"
