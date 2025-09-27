# Deep Search Agent Assessment

An autonomous research agent built with LangGraph for comprehensive investigations, featuring multi-step analysis, risk assessment, and connection mapping capabilities.

## 🚀 Overview

The Deep Search Agent is a sophisticated AI-powered research tool that performs comprehensive investigations on topics or entities. It uses LangGraph to orchestrate multiple analysis stages including fact extraction, risk assessment, connection mapping, and source validation.

## 📋 Prerequisites

- **Python**: 3.10.4 or higher
- **UV Package Manager**: For dependency management
- **API Keys**: Azure OpenAI and Tavily API access

### Required API Keys

- Azure OpenAI (GPT models)
- Azure Grok (Alternative LLM)
- Tavily (Web search API)

## 🛠️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/mhumza37dev/deep-search-agent.git
cd deep_search_agent_assessment
```

### 2. Install UV Package Manager

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 3. Install Dependencies

```bash
# Install all dependencies using UV
uv sync

# Activate the virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=your_gpt_deployment_name
AZURE_OPENAI_MODEL=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Azure Grok Configuration  
AZURE_GROK_API_KEY=your_azure_grok_api_key
AZURE_GROK_ENDPOINT=https://your-grok-resource.openai.azure.com/
AZURE_GROK_DEPLOYMENT=your_grok_deployment_name
AZURE_GROK_MODEL=grok-beta
AZURE_GROK_API_VERSION=2024-02-15-preview

# Web Search API
TAVILY_API_KEY=your_tavily_api_key
```

### 5. Run the Application

```bash
# Start the FastAPI server
python main.py

# Or using uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 1122 --reload
```

The application will be available at:
- **Web Interface**: http://localhost:1122/deep-search
- **API Documentation**: http://localhost:1122/docs
- **Health Check**: http://localhost:1122/

## 📁 Project Structure

```
deep_search_agent_assessment/
├── main.py                     # FastAPI application entry point
├── pyproject.toml             # Project dependencies and metadata
├── uv.lock                    # Dependency lock file
├── index.html                 # Web interface frontend
├── research_graph.png         # LangGraph workflow visualization
├── .env                       # Environment variables (create this)
├── .gitignore                 # Git ignore patterns
│
├── src/                       # Source code directory
│   ├── config/
│   │   └── app_config.py      # Application configuration management
│   │
│   ├── agent/                 # Core agent implementation
│   │   ├── graph/             # LangGraph workflow components
│   │   │   ├── base_node.py   # Base node class for all workflow nodes
│   │   │   ├── research_graph.py  # Main LangGraph workflow definition
│   │   │   ├── router.py      # Workflow routing logic
│   │   │   ├── state.py       # Shared state management
│   │   │   └── nodes/         # Individual workflow nodes
│   │   │       ├── planning_node.py         # Research planning and strategy
│   │   │       ├── search_node.py           # Web search and data collection
│   │   │       ├── extraction_node.py       # Fact extraction and parsing
│   │   │       ├── risk_analysis_node.py    # Risk identification and assessment
│   │   │       ├── connection_mapping_node.py # Entity relationship mapping
│   │   │       ├── validation_node.py       # Source credibility validation
│   │   │       └── report_node.py           # Final report generation
│   │   │
│   │   ├── services/          # Business logic services
│   │   │   ├── search_service.py       # Web search integration
│   │   │   ├── analysis_service.py     # Content analysis and processing
│   │   │   └── model_services.py       # LLM interaction services
│   │   │
│   │   └── llm_services/      # LLM strategy implementations
│   │       ├── llm_strategy.py         # Abstract LLM strategy interface
│   │       └── strategies/             # Concrete LLM implementations
│   │           ├── gpt_strategy.py     # Azure OpenAI GPT strategy
│   │           └── grok_strategy.py    # Azure Grok strategy
│   │
│   ├── api/                   # FastAPI REST API
│   │   ├── controller/
│   │   │   └── search_controller.py    # Search endpoint controllers
│   │   └── manager/
│   │       └── search_manager.py       # Search orchestration logic
│   │
│   └── evaluators/           # Testing and evaluation
│       └── evaluation.py     # Evaluation framework with test cases
```

### Component Responsibilities

#### Core Components

- **`main.py`**: FastAPI application setup, middleware configuration, and server startup
- **`index.html`**: Single-page web application for interactive research interface

#### Configuration

- **`src/config/app_config.py`**: Centralized configuration management with environment variable validation

#### Agent Architecture

- **`src/agent/graph/`**: LangGraph workflow implementation
  - **`research_graph.py`**: Main workflow orchestration with node connections
  - **`state.py`**: Shared state object for passing data between nodes
  - **`router.py`**: Conditional routing logic for workflow branching
  - **`base_node.py`**: Abstract base class for all workflow nodes

#### Workflow Nodes

- **`planning_node.py`**: Analyzes query and creates research strategy
- **`search_node.py`**: Performs web searches using Tavily API
- **`extraction_node.py`**: Extracts structured facts from search results
- **`risk_analysis_node.py`**: Identifies potential risks and assigns severity levels
- **`connection_mapping_node.py`**: Maps relationships between entities
- **`validation_node.py`**: Validates source credibility and cross-references information
- **`report_node.py`**: Generates comprehensive investigation reports

#### Services Layer

- **`src/agent/services/`**: Business logic abstraction
  - **`search_service.py`**: Web search API integration and result processing
  - **`analysis_service.py`**: Content analysis, parsing, and structuring
  - **`model_services.py`**: LLM interaction and response processing

#### LLM Integration

- **`src/agent/llm_services/`**: Strategy pattern for multiple LLM providers
  - **`llm_strategy.py`**: Abstract interface for LLM implementations
  - **`gpt_strategy.py`**: Azure OpenAI GPT integration
  - **`grok_strategy.py`**: Azure Grok integration

#### API Layer

- **`src/api/controller/search_controller.py`**: REST endpoints for search operations
- **`src/api/manager/search_manager.py`**: High-level search orchestration and streaming

#### Evaluation Framework

- **`src/evaluators/evaluation.py`**: Comprehensive testing framework with predefined test cases for prominent figures (Elon Musk, Jensen Huang, Sam Altman)

## 🔧 Usage

### Web Interface

1. Open http://localhost:1122/deep-search
2. Enter your research query
3. View real-time streaming results as the agent processes information
4. Download comprehensive reports in JSON format

### API Usage

```python
import requests

# Stream search results
response = requests.post(
    "http://localhost:1122/api/search/stream",
    json={"query": "Elon Musk business network analysis"},
    stream=True
)

for chunk in response.iter_content(chunk_size=1024):
    print(chunk.decode())
```

### Running Evaluations

```python
from src.evaluators.evaluation import create_test_cases, evaluate_investigation

# Load test cases
test_cases = create_test_cases()

# Run evaluation (implement your investigation logic)
for test_case in test_cases:
    results = your_investigation_function(test_case["name"])
    evaluation = evaluate_investigation(results, test_case)
    print(f"Score for {test_case['name']}: {evaluation['overall_score']:.1%}")
```

## 🧪 Testing

The project includes a comprehensive evaluation framework located in `src/evaluators/evaluation.py`. It tests the agent's ability to:

- **Fact Discovery**: Uncover hidden biographical and business facts
- **Risk Identification**: Detect potential legal, financial, and reputational risks  
- **Connection Mapping**: Map relationships between people, organizations, and events
- **Source Validation**: Verify information credibility

### Test Subjects

The evaluation includes predefined test cases for:
- **Elon Musk**: Tech entrepreneur with complex business network
- **Jensen Huang**: NVIDIA CEO with semiconductor industry connections
- **Sam Altman**: OpenAI CEO with venture capital and startup connections

## 🚨 Important Notes

- **API Keys**: Ensure all required API keys are properly configured in the `.env` file
- **Rate Limits**: Be mindful of API rate limits for Azure OpenAI and Tavily
- **Costs**: Monitor usage as LLM API calls can incur significant costs
- **Compliance**: Ensure research activities comply with applicable laws and regulations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is part of an assessment and is intended for evaluation purposes.

---

**Built with**: Python 3.10+, LangGraph, FastAPI, Azure OpenAI, Tavily API
