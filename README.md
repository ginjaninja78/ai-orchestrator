# AI Orchestrator

A highly advanced agentic system designed to orchestrate development tasks using Claude Code and other AI tools.

## Features

- **Multi-Agent Architecture**: Specialized agents for research, coding, and management.
- **Configuration Driven**: Easily configurable via `config.yaml`.
- **Extensible**: Designed to integrate with various AI models and tools.
- **Task Orchestration**: Manages complex workflows and dependencies.

## Setup

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2.  Configure agents in `config.yaml`.

3.  Run the orchestrator:
    ```bash
    python main.py
    ```

## Architecture

The system consists of an `AgentManager` that coordinates multiple `Agent` instances. Each agent has a specific role and utilizes different AI models (e.g., Claude 3 Opus, Sonnet, Haiku) best suited for their tasks.

## Future Roadmap

- Integration with ChromaDB for long-term memory.
- Real-time feedback loops with the Claude CLI.
- Web interface for monitoring and control.
