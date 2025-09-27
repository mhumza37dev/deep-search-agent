"""
Evaluation Framework for Deep Search Agent

Tests the agent's ability to uncover hidden facts, identify risks,
map connections, and validate sources against known test cases.
"""

from typing import List, Dict, Any
import json


def create_test_cases() -> List[Dict[str, Any]]:
    """Create evaluation subjects with known hidden facts for testing"""

    test_cases = [
        {
            "name": "Elon Musk",
            "description": "Tech entrepreneur with complex business network",
            "hidden_facts": [
                "Co-founded Zip2 with his brother Kimbal in 1995",
                "Was briefly CEO of PayPal after X.com merger",
                "Born in Pretoria, South Africa in 1971",
                "Has Neuralink brain-computer interface company",
                "Owns significant Bitcoin holdings",
                "Has multiple children with different partners",
                "Studied at University of Pennsylvania",
                "Moved to Canada at age 17",
                "Founded Boring Company for tunnel construction",
                "Has Asperger's syndrome (disclosed on SNL)",
            ],
            "expected_risks": [
                "SEC securities violations and settlements",
                "Twitter acquisition controversies and legal issues",
                "Tesla production and delivery challenges",
                "Cryptocurrency market manipulation accusations",
                "Labor disputes at Tesla factories",
                "Personal behavior on social media",
            ],
            "expected_connections": {
                "people": ["Kimbal Musk", "Grimes", "Peter Thiel", "Sam Altman"],
                "organizations": [
                    "Tesla",
                    "SpaceX",
                    "Neuralink",
                    "OpenAI",
                    "PayPal",
                    "X (Twitter)",
                ],
                "events": ["PayPal sale to eBay", "Tesla IPO", "Twitter acquisition"],
                "locations": ["Austin Texas", "Fremont California", "Boca Chica Texas"],
            },
            "verification_sources": [
                "SEC filings",
                "Tesla annual reports",
                "PayPal acquisition documents",
                "University records",
                "Court filings",
            ],
        },
        {
            "name": "Jensen Huang",
            "description": "NVIDIA CEO with semiconductor industry connections",
            "hidden_facts": [
                "Co-founded NVIDIA in 1993 at age 30",
                "Born in Taiwan, moved to US as child",
                "Graduated from Stanford with electrical engineering degree",
                "Worked at LSI Logic and AMD before NVIDIA",
                "Known for wearing leather jackets at presentations",
                "NVIDIA started in a Denny's restaurant meeting",
                "Has engineering background in chip design",
                "Led NVIDIA through multiple market transformations",
                "Significant AI industry influence through GPU development",
                "Net worth over $70 billion due to AI boom",
            ],
            "expected_risks": [
                "China trade restrictions impacting business",
                "Semiconductor supply chain vulnerabilities",
                "AI bubble concerns affecting stock valuation",
                "Geopolitical tensions affecting international sales",
                "Competition from Intel, AMD, and custom chips",
            ],
            "expected_connections": {
                "people": [
                    "Lisa Su (AMD)",
                    "Pat Gelsinger (Intel)",
                    "Tim Cook (Apple)",
                ],
                "organizations": ["NVIDIA", "Stanford University", "AMD", "LSI Logic"],
                "events": ["CUDA launch", "AI boom 2023", "Crypto mining boom/bust"],
                "locations": ["Santa Clara California", "Taiwan", "Silicon Valley"],
            },
            "verification_sources": [
                "NVIDIA SEC filings",
                "Stanford alumni records",
                "Industry conference presentations",
                "Patent filings",
                "Financial earnings calls",
            ],
        },
        {
            "name": "Sam Altman",
            "description": "OpenAI CEO with venture capital and startup connections",
            "hidden_facts": [
                "Dropped out of Stanford after two years",
                "Founded Loopt location-sharing app in 2005",
                "Was president of Y Combinator accelerator",
                "Co-founded OpenAI as non-profit in 2015",
                "Briefly fired and rehired as OpenAI CEO in November 2023",
                "Has significant investments in nuclear energy companies",
                "Founded Worldcoin cryptocurrency project",
                "Advocate for universal basic income",
                "Has connections to effective altruism movement",
                "Testified before US Congress on AI risks",
            ],
            "expected_risks": [
                "OpenAI governance crisis and board conflicts",
                "AI safety and existential risk concerns",
                "Regulatory scrutiny of AI development",
                "Worldcoin privacy and cryptocurrency issues",
                "Conflicts of interest with investments",
                "Competition from Google, Microsoft, Anthropic",
            ],
            "expected_connections": {
                "people": ["Elon Musk", "Peter Thiel", "Reid Hoffman", "Greg Brockman"],
                "organizations": ["OpenAI", "Y Combinator", "Microsoft", "Worldcoin"],
                "events": [
                    "ChatGPT launch",
                    "OpenAI board crisis",
                    "Congressional testimony",
                ],
                "locations": ["San Francisco", "Silicon Valley", "Washington DC"],
            },
            "verification_sources": [
                "Y Combinator records",
                "OpenAI announcements",
                "Congressional hearing transcripts",
                "Venture capital filings",
                "Stanford records",
            ],
        },
    ]

    return test_cases


def evaluate_investigation(
    investigation_results: Dict, test_case: Dict
) -> Dict[str, float]:
    """Evaluate investigation results against known test case facts"""

    if not investigation_results:
        return {
            "facts_accuracy": 0.0,
            "risk_detection": 0.0,
            "connection_coverage": 0.0,
            "overall_score": 0.0,
        }

    # Extract investigation data
    found_facts = investigation_results.get("facts", {})
    found_risks = investigation_results.get("risks", [])
    found_connections = investigation_results.get("connections", {})

    # Evaluate fact accuracy
    facts_accuracy = evaluate_fact_extraction(found_facts, test_case["hidden_facts"])

    # Evaluate risk detection
    risk_detection = evaluate_risk_identification(
        found_risks, test_case["expected_risks"]
    )

    # Evaluate connection coverage
    connection_coverage = evaluate_connection_mapping(
        found_connections, test_case["expected_connections"]
    )

    # Calculate overall score
    overall_score = (facts_accuracy + risk_detection + connection_coverage) / 3

    evaluation = {
        "facts_accuracy": facts_accuracy,
        "risk_detection": risk_detection,
        "connection_coverage": connection_coverage,
        "overall_score": overall_score,
        "target": test_case["name"],
        "details": {
            "expected_facts": len(test_case["hidden_facts"]),
            "found_facts": sum(len(facts) for facts in found_facts.values()),
            "expected_risks": len(test_case["expected_risks"]),
            "found_risks": len(found_risks),
            "expected_connections": sum(
                len(conns) for conns in test_case["expected_connections"].values()
            ),
            "found_connections": sum(
                len(conns) for conns in found_connections.values()
            ),
        },
    }

    return evaluation


def evaluate_fact_extraction(found_facts: Dict, expected_facts: List[str]) -> float:
    """Evaluate how many expected facts were discovered"""
    if not expected_facts:
        return 1.0

    # Combine all found facts into a single text for matching
    all_found_text = ""
    for fact_category, facts_list in found_facts.items():
        for fact_item in facts_list:
            if isinstance(fact_item, dict):
                all_found_text += fact_item.get("fact", "") + " "
            else:
                all_found_text += str(fact_item) + " "

    all_found_text = all_found_text.lower()

    # Count how many expected facts were found (partial matching)
    found_count = 0
    for expected_fact in expected_facts:
        if fact_partially_matches(expected_fact, all_found_text):
            found_count += 1

    return found_count / len(expected_facts)


def evaluate_risk_identification(found_risks: List, expected_risks: List[str]) -> float:
    """Evaluate risk detection accuracy"""
    if not expected_risks:
        return 1.0 if not found_risks else 0.5  # No false positives

    # Combine all found risks into text
    all_found_risks_text = ""
    for risk_item in found_risks:
        if isinstance(risk_item, dict):
            all_found_risks_text += risk_item.get("risk", "") + " "
        else:
            all_found_risks_text += str(risk_item) + " "

    all_found_risks_text = all_found_risks_text.lower()

    # Count matching risks
    found_count = 0
    for expected_risk in expected_risks:
        if fact_partially_matches(expected_risk, all_found_risks_text):
            found_count += 1

    return found_count / len(expected_risks)


def evaluate_connection_mapping(
    found_connections: Dict, expected_connections: Dict
) -> float:
    """Evaluate connection discovery accuracy"""
    if not expected_connections:
        return 1.0

    total_expected = sum(len(conn_list) for conn_list in expected_connections.values())
    if total_expected == 0:
        return 1.0

    total_found = 0

    for conn_type, expected_list in expected_connections.items():
        found_list = found_connections.get(conn_type, [])

        # Convert found connections to text for matching
        found_text = ""
        for conn_item in found_list:
            if isinstance(conn_item, dict):
                found_text += " ".join(str(v) for v in conn_item.values()) + " "
            else:
                found_text += str(conn_item) + " "

        found_text = found_text.lower()

        # Count matches in this connection type
        for expected_item in expected_list:
            if fact_partially_matches(str(expected_item), found_text):
                total_found += 1

    return total_found / total_expected


def fact_partially_matches(expected_fact: str, found_text: str) -> bool:
    """Check if an expected fact is partially found in the discovered text"""
    expected_fact = expected_fact.lower()
    found_text = found_text.lower()

    # Extract key terms from expected fact (ignore common words)
    stop_words = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "but",
        "in",
        "on",
        "at",
        "to",
        "for",
        "of",
        "with",
        "by",
        "is",
        "was",
        "are",
        "were",
    }
    key_terms = [
        word
        for word in expected_fact.split()
        if word not in stop_words and len(word) > 2
    ]

    # Check if majority of key terms are found
    if not key_terms:
        return False

    found_terms = sum(1 for term in key_terms if term in found_text)
    return found_terms / len(key_terms) >= 0.5  # At least 50% of key terms found


def generate_evaluation_report(evaluations: List[Dict]) -> str:
    """Generate a comprehensive evaluation report"""
    if not evaluations:
        return "No evaluation data available."

    report = "DEEP SEARCH AGENT - EVALUATION REPORT\n"
    report += "=" * 50 + "\n\n"

    # Individual test case results
    for i, eval_result in enumerate(evaluations, 1):
        report += f"Test Case {i}: {eval_result['target']}\n"
        report += "-" * 30 + "\n"
        report += f"Facts Accuracy:      {eval_result['facts_accuracy']:.1%}\n"
        report += f"Risk Detection:      {eval_result['risk_detection']:.1%}\n"
        report += f"Connection Coverage: {eval_result['connection_coverage']:.1%}\n"
        report += f"Overall Score:       {eval_result['overall_score']:.1%}\n\n"

        details = eval_result.get("details", {})
        report += f"Details:\n"
        report += f"  Expected Facts: {details.get('expected_facts', 0)}, Found: {details.get('found_facts', 0)}\n"
        report += f"  Expected Risks: {details.get('expected_risks', 0)}, Found: {details.get('found_risks', 0)}\n"
        report += f"  Expected Connections: {details.get('expected_connections', 0)}, Found: {details.get('found_connections', 0)}\n\n"

    # Overall statistics
    avg_facts = sum(e["facts_accuracy"] for e in evaluations) / len(evaluations)
    avg_risks = sum(e["risk_detection"] for e in evaluations) / len(evaluations)
    avg_connections = sum(e["connection_coverage"] for e in evaluations) / len(
        evaluations
    )
    avg_overall = sum(e["overall_score"] for e in evaluations) / len(evaluations)

    report += "OVERALL PERFORMANCE\n"
    report += "=" * 20 + "\n"
    report += f"Average Facts Accuracy:      {avg_facts:.1%}\n"
    report += f"Average Risk Detection:      {avg_risks:.1%}\n"
    report += f"Average Connection Coverage: {avg_connections:.1%}\n"
    report += f"Average Overall Score:       {avg_overall:.1%}\n"

    return report


def save_evaluation_results(
    evaluations: List[Dict], filename: str = "evaluation_results.json"
):
    """Save evaluation results to file"""
    try:
        evaluation_data = {
            "timestamp": json.dumps(evaluations, indent=2),
            "summary": {
                "total_test_cases": len(evaluations),
                "average_scores": {
                    "facts_accuracy": sum(e["facts_accuracy"] for e in evaluations)
                    / len(evaluations),
                    "risk_detection": sum(e["risk_detection"] for e in evaluations)
                    / len(evaluations),
                    "connection_coverage": sum(
                        e["connection_coverage"] for e in evaluations
                    )
                    / len(evaluations),
                    "overall_score": sum(e["overall_score"] for e in evaluations)
                    / len(evaluations),
                },
            },
            "individual_results": evaluations,
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(evaluation_data, f, indent=2, ensure_ascii=False)

        print(f"Evaluation results saved to: {filename}")
        return filename

    except Exception as e:
        print(f"Error saving evaluation results: {e}")
        return None
