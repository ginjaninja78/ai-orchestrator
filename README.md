# 🤖 AI Orchestrator

This tool is a standalone AI orchestration system designed to coordinate multiple AI agents (Claude, Codex, etc.) for high-performance software development.

## 🚀 Features

- **Multi-Agent Coordination:** Manages specialized agents for research, coding, and quality assurance.
- **Claude Integration:** Leverages Anthropic's Claude for deep research and semantic understanding.
- **Codex Simulation:** Simulates a coding agent (Codex) for code generation and syntax checking.
- **Parallel Execution:** Capable of running tasks concurrently (planned feature).

## 🛠️ Setup

1.  Ensure Python 3.8+ is installed.
2.  Install dependencies (if any).
3.  Run the orchestrator:
    ```bash
    python main.py
    ```

## 🏗️ Architecture

- **AgentManager:** Central controller that dispatches tasks.
- **ResearcherAgent (Claude):** Handles information retrieval and complex reasoning.
- **CoderAgent (Codex):** Handles code generation and local validation.

## 📝 Usage

Currently, the system runs a predefined workflow in `main.py`. Future versions will support dynamic task ingestion.
