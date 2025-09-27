import json
from enum import Enum
from typing import List, Dict
from src.agent.llm_services.strategies.gpt_strategy import GPT4Strategy
from src.agent.llm_services.strategies.grok_strategy import GrokStrategy


class MODEL(Enum):
    GROK = "grok"
    GPT4 = "gpt"


class ModelService:
    """Handle both Grok and GPT-4 for different tasks"""

    model_assignments = {
        "extract_facts": MODEL.GPT4,
        "analyze_risks": MODEL.GROK,
        "map_connections": MODEL.GROK,
        "validate_sources": MODEL.GPT4,
        "generate_report": MODEL.GPT4,
    }

    def __init__(self):
        self.grok = GrokStrategy()
        self.gpt4 = GPT4Strategy()

    def extract_facts(self, search_results: List[Dict], fact_type: str) -> List[Dict]:
        """Extract facts from search results by type"""

        combined_text = "\n".join(
            [
                f"Source: {result.get('url', 'Unknown')}\n{result.get('content', '')}"
                for result in search_results
            ]
        )

        prompts = {
            "biographical": """
            Extract biographical facts from this search data about the target person:
            - Full name and known aliases
            - Birth date and place
            - Education history (schools, degrees, years)
            - Family information (spouse, children, parents)
            - Personal background and early life
            
            Return as JSON list with format: [{"fact": "description", "source": "url", "confidence": 0.0-1.0}]
            """,
            "professional": """
            Extract professional history from this search data:
            - Current and previous job positions
            - Companies worked for and dates
            - Board positions and directorships
            - Professional achievements and awards
            - Career progression and timeline
            
            Return as JSON list with format: [{"fact": "description", "source": "url", "confidence": 0.0-1.0}]
            """,
            "financial": """
            Extract financial information from this search data:
            - Investment activities and portfolio
            - Company ownership and stakes
            - Financial partnerships and deals
            - Assets and properties mentioned
            - Revenue/wealth estimates
            
            Return as JSON list with format: [{"fact": "description", "source": "url", "confidence": 0.0-1.0}]
            """,
            "behavioral": """
            Extract behavioral patterns from this search data:
            - Leadership style and management approach
            - Public statements and positions
            - Decision-making patterns
            - Communication style
            - Consistency in actions/statements
            
            Return as JSON list with format: [{"fact": "description", "source": "url", "confidence": 0.0-1.0}]
            """,
        }

        prompt = prompts.get(fact_type, prompts["biographical"])
        full_prompt = f"{prompt}\n\nSearch Data:\n{combined_text[:15000]}"

        try:
            if self.model_assignments["extract_facts"] == MODEL.GPT4:
                response = self.gpt4.invoke([{"role": "user", "content": full_prompt}])
            else:
                response = self.grok.invoke([{"role": "user", "content": full_prompt}])
            result = response

            # Try to parse JSON response
            try:
                facts = json.loads(result)
                return facts if isinstance(facts, list) else []
            except json.JSONDecodeError:
                # Fallback: extract facts from text
                return self._parse_facts_from_text(result)

        except Exception as e:
            print(f"Error in fact extraction: {e}")
            return []

    def analyze_risks(self, facts: Dict) -> List[Dict]:
        """Risk pattern recognition using Grok"""

        facts_text = json.dumps(facts, indent=2)

        prompt = f"""
        Analyze these facts about a person for potential risks and red flags:
        
        Look for:
        1. Legal issues (lawsuits, violations, investigations)
        2. Financial irregularities (bankruptcies, failed ventures, debt issues)  
        3. Reputational problems (scandals, controversies, negative press)
        4. Inconsistencies (conflicting information across sources)
        5. Concerning associations (links to problematic entities/people)
        
        Return JSON list: [{{"risk": "description", "severity": "LOW/MEDIUM/HIGH/CRITICAL", "evidence": "supporting facts", "confidence": "0.0-1.0"}}]
        
        Facts to analyze:
        {facts_text}
        """

        try:
            if self.model_assignments["analyze_risks"] == MODEL.GPT4:
                response = self.gpt4.invoke([{"role": "user", "content": prompt}])
            else:
                response = self.grok.invoke([{"role": "user", "content": prompt}])
            if "```json" in response:
                result = response.split("```json")[1].split("```")[0].strip()
            else:
                result = response
            try:
                risks = json.loads(result)
                return risks if isinstance(risks, list) else []
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in risk analysis: {e}")
                return self._parse_risks_from_text(result)

        except Exception as e:
            print(f"Error in risk analysis: {e}")
            return []

    def map_connections(self, facts: Dict) -> Dict:
        """Map relationships and connections using Grok"""

        facts_text = json.dumps(facts, indent=2)

        prompt = f"""
        Map connections and relationships from these facts:
        
        Identify:
        1. People mentioned (colleagues, partners, family, associates)
        2. Organizations (companies, institutions, boards)
        3. Events (meetings, deals, incidents, shared experiences)
        4. Locations (offices, properties, frequent places)
        
        Return JSON: {{
            "people": [{{"name": "person", "relationship": "type", "context": "how connected"}}],
            "organizations": [{{"name": "org", "role": "relationship type", "timeframe": "when"}}],
            "events": [{{"event": "description", "participants": ["people involved"], "significance": "why important"}}],
            "locations": [{{"place": "location", "connection_type": "how related", "timeframe": "when"}}]
        }}
        
        Facts:
        {facts_text}
        """

        try:
            if self.model_assignments["map_connections"] == MODEL.GPT4:
                response = self.gpt4.invoke([{"role": "user", "content": prompt}])
            else:
                response = self.grok.invoke([{"role": "user", "content": prompt}])
                if "```json" in response:
                    result = response.split("```json")[1].split("```")[0].strip()
                else:
                    result = response
            try:
                connections = json.loads(result)
                return connections if isinstance(connections, dict) else {}
            except json.JSONDecodeError:
                return self._parse_connections_from_text(result)

        except Exception as e:
            print(f"Error in connection mapping: {e}")
            return {}

    def validate_sources(self, facts: Dict, search_results: List[Dict]) -> Dict:
        """Source validation with confidence scoring using Grok"""

        # Create source quality mapping
        source_quality = {}
        for result in search_results:
            url = result.get("url", "")
            source_quality[url] = self._assess_source_quality(url)

        facts_text = json.dumps(facts, indent=2)
        sources_text = json.dumps(source_quality, indent=2)

        prompt = f"""
        Validate these facts and assign confidence scores based on source quality and cross-referencing:
        
        Consider:
        1. Source reliability (primary vs secondary, credibility)
        2. Cross-referencing (multiple sources saying same thing)
        3. Recency (how recent is the information)
        4. Consistency (conflicting vs supporting information)
        
        Return JSON: {{
            "fact_confidence": {{"fact_id": confidence_score_0_to_1}},
            "source_reliability": {{"source_url": reliability_score_0_to_1}},
            "cross_references": {{"fact": ["supporting_sources"]}},
            "inconsistencies": [{{"fact": "conflicting fact", "sources": ["conflicting sources"], "severity": "LOW/MEDIUM/HIGH"}}]
        }}
        
        Facts: {facts_text}
        
        Source Quality: {sources_text}
        """

        try:
            if self.model_assignments["validate_sources"] == MODEL.GPT4:
                response = self.gpt4.invoke([{"role": "user", "content": prompt}])
            else:
                response = self.grok.invoke([{"role": "user", "content": prompt}])
            result = response

            try:
                validation = json.loads(result)
                return validation if isinstance(validation, dict) else {}
            except json.JSONDecodeError:
                return {
                    "fact_confidence": {},
                    "source_reliability": {},
                    "cross_references": {},
                    "inconsistencies": [],
                }

        except Exception as e:
            print(f"Error in source validation: {e}")
            return {}

    def generate_report(self, investigation_data: Dict) -> str:
        """Generate final intelligence report"""

        data_text = json.dumps(investigation_data, indent=2)

        prompt = f"""
        Generate a comprehensive intelligence report based on this investigation data:

        Structure the report with:
        1. EXECUTIVE SUMMARY (key findings, risk level, recommendations)
        2. BIOGRAPHICAL PROFILE (verified personal/professional details)
        3. RISK ASSESSMENT (identified risks by severity, supporting evidence)
        4. NETWORK ANALYSIS (key relationships and connections)
        5. SOURCE RELIABILITY (confidence levels and verification status)
        6. INTELLIGENCE GAPS (what couldn't be verified or found)
        7. RECOMMENDATIONS (suggested actions based on findings)

        Make it professional, fact-based, and clearly formatted in valid HTML so that it can be directly appended as element without any issues and without any modifications
        Use:
        - <h4>, <h5> tags for section headings and sub-headings
        - <ul>/<li> for bullet points
        - <table> for structured data
        - <strong> for emphasis
        - Inline CSS styles for basic styling (fonts, colors, spacing, background=transparent etc)
        - No footer/prepared by section
        - No date in header

        Investigation Data:
        {data_text}
        """

        try:
            if self.model_assignments["generate_report"] == MODEL.GPT4:
                response = self.gpt4.invoke([{"role": "user", "content": prompt}])
            else:
                response = self.grok.invoke([{"role": "user", "content": prompt}])
            return response
        except Exception as e:
            return f"Error generating report: {e}"

    def _parse_facts_from_text(self, text: str) -> List[Dict]:
        """Fallback parser for non-JSON responses"""
        facts = []
        lines = text.split("\n")
        for line in lines:
            if line.strip() and not line.startswith("#"):
                facts.append(
                    {
                        "fact": line.strip(),
                        "source": "parsed_from_response",
                        "confidence": 0.5,
                    }
                )
        return facts[:10]  # Limit to 10 facts

    def _parse_risks_from_text(self, text: str) -> List[Dict]:
        """Fallback parser for risk analysis"""
        risks = []
        lines = text.split("\n")
        for line in lines:
            if any(
                word in line.lower() for word in ["risk", "concern", "issue", "problem"]
            ):
                risks.append(
                    {
                        "risk": line.strip(),
                        "severity": "MEDIUM",
                        "evidence": "from_analysis",
                        "confidence": 0.5,
                    }
                )
        return risks[:5]

    def _parse_connections_from_text(self, text: str) -> Dict:
        """Fallback parser for connections"""
        return {"people": [], "organizations": [], "events": [], "locations": []}

    def _assess_source_quality(self, url: str) -> float:
        """Simple source quality assessment"""
        high_quality = [
            "wikipedia.org",
            "bloomberg.com",
            "reuters.com",
            "wsj.com",
            "ft.com",
            "forbes.com",
        ]
        medium_quality = ["linkedin.com", "crunchbase.com", "sec.gov", ".edu", ".gov"]

        url_lower = url.lower()

        if any(domain in url_lower for domain in high_quality):
            return 0.9
        elif any(domain in url_lower for domain in medium_quality):
            return 0.7
        else:
            return 0.5
