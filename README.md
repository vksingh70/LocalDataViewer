# Localized Infrastructure Audit Agent 🤖

An **Agentic RAG** system built with **LangGraph** and **Google Gemini 3.1 Pro**, designed to audit and remediate infrastructure code locally using the **Model Context Protocol (MCP)**.

## 🚀 Overview
Unlike traditional RAG, this agent uses a reasoning loop to dynamically discover, read, and audit local infrastructure files. By leveraging MCP, the agent maintains **Data Sovereignty**—sensitive configuration data never leaves the local environment for indexing.

### Key Features
- **Autonomous Reasoning:** Uses LangGraph to iterate between observation, tool-calling, and analysis.
- **MCP Integration:** Uses a custom Model Context Protocol server to bridge the LLM with the local filesystem.
- **Security Auditing:** Specifically tuned to identify risks in Terraform (`.tf`) and Kubernetes manifests.
- **Local Execution:** Capable of running local diagnostic scripts and capturing output for real-time analysis.

---

## 🏗 Architecture


1. **The Brain:** Google Gemini 3.1 Pro (via LangChain).
2. **The Orchestrator:** LangGraph state machine managing the `agent -> tools -> agent` loop.
3. **The Gateway:** A Python-based MCP Server (`my_local_data.py`) providing secure tool access to `/configs` and `/scripts`.

---

## 🛠 Setup & Installation

### Prerequisites
- Python 3.11+
- Google Gemini API Key ([Get one here](https://aistudio.google.com/))

### Installation
1. **Clone the repo:**
   ```bash
   git clone [https://github.com/your-username/LocalDataViewer.git](https://github.com/your-username/LocalDataViewer.git)
   cd LocalDataViewer

## 🛠 Developer Playbook: From Checkout to Enhancement

Follow these steps when moving to a new machine or starting a new development session.

### 1. Fresh Environment Setup
```bash
# Clone and enter
git clone <your-repo-url>
cd LocalDataViewer

# Initialize Environment
python -m venv venv
source venv/bin/activate

# Install Dependencies
pip install -r requirements.txt

# Setup Secrets
echo "GOOGLE_API_KEY=your_key_here" > .env

# This uses the MCP Inspector to test your server in isolation
npx @modelcontextprotocol/inspector python my_local_data.py