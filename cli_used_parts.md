# Parts of the OpenHands Repository Used in CLI Mode

This document outlines the key parts of the OpenHands repository that are actively used when running the application via the CLI (e.g., `.venv/bin/openhands`). This is based on tracing the execution flow from the entry point. Note that this focuses on runtime components; development tools, tests, documentation, and frontend/UI are not involved in CLI execution.

## Entry Point
- **.venv/bin/openhands**: The CLI executable script. It imports and calls `main()` from `openhands/cli/entry.py`.

## CLI Handling
- **openhands/cli/entry.py**: Parses arguments and routes to CLI or GUI modes. For CLI, it calls `run_cli_command` from `openhands/cli/main.py`.
- **openhands/cli/main.py**: Core CLI logic, including session setup, event handling, agent execution, and user interaction (e.g., prompts, confirmations).
- **openhands/cli/commands.py**: Handles special CLI commands (e.g., /help, /exit).
- **openhands/cli/settings.py**: Manages LLM settings modifications.
- **openhands/cli/shell_config.py**: Shell configuration and alias management.
- **openhands/cli/tui.py**: Terminal UI utilities for displaying messages, prompts, and events.
- **openhands/cli/utils.py**: Utility functions like usage metrics updates.
- **openhands/cli/vscode_extension.py**: Optional VSCode extension installation attempt.
- **openhands/cli/suppress_warnings.py**: Suppresses unnecessary warnings.
- **openhands/cli/gui_launcher.py**: Not used in pure CLI mode (it's for 'serve' subcommand).

## Core Configuration
- **openhands/core/config/**: All configuration files, including `OpenHandsConfig`, argument parsing (`arg_utils.py`, `get_cli_parser`), and utilities (`utils.py`, `finalize_config`).
- **openhands/core/config/condenser_config.py**: Condenser configurations (e.g., `NoOpCondenserConfig`).
- **openhands/core/config/mcp_config.py**: MCP (Microagent Control Plane) configuration if enabled.

## Agent Setup and Execution
- **openhands/core/setup.py**: Functions for creating agents, controllers, memory, runtimes (e.g., `create_agent`, `create_controller`, `create_runtime`).
- **openhands/agenthub/**: Agent registrations and implementations (imported to register available agents like CodeActAgent).
- **openhands/controller/agent.py**: Base Agent class.
- **openhands/controller/**: AgentController for managing agent lifecycle and state.
- **openhands/core/loop.py**: Main agent execution loop (`run_agent_until_done`).
- **openhands/core/schema/**: Schemas for agent states, exit reasons, etc.

## Runtime Environment
- **openhands/runtime/**: Runtime classes and utilities (e.g., `base.py`, `get_runtime_cls`, specific runtimes like local or Docker).
- **openhands/runtime/builder/**: Runtime builder if needed (e.g., for Docker images).

## Events and Observations
- **openhands/events/**: Event system, including `event.py`, `action/**` (e.g., `ChangeAgentStateAction`, `MessageAction`), `observation/**` (e.g., `AgentStateChangedObservation`), and `EventSource`, `EventStreamSubscriber`.

## Memory Management
- **openhands/memory/**: Agent memory handling, including condensers (e.g., `llm_summarizing_condenser.py`).
- **openhands/memory/condenser/impl/**: Specific condenser implementations.

## Microagents and MCP (if enabled)
- **openhands/microagent/microagent.py**: Base microagent class.
- **openhands/mcp/**: Microagent Control Plane, including tool additions (`add_mcp_tools_to_agent`), error collection.
- **microagents/**: Public microagent definitions (loaded if applicable).
- **.openhands/microagents/**: Repository-specific microagents (loaded if selected repo is set).

## Utilities and Logging
- **openhands/core/logger.py**: Logging setup.
- **openhands/utils/utils.py**: General utilities (e.g., `create_registry_and_conversation_stats`).
- **openhands/storage/settings/file_settings_store.py**: Settings storage.
- **openhands/io.py**: Input/output utilities (e.g., `read_task`).

## Other Imported Components
- **openhands/core/schema/exit_reason.py**: Exit reasons for sessions.
- **openhands/events/action/action_security_risk.py**: Security risk enums.
- Various standard library imports (e.g., asyncio, logging, os, sys) and third-party (e.g., prompt_toolkit).

## Unused in CLI Mode
- **frontend/**: React frontend (used in GUI mode).
- **openhands-ui/**: UI components.
- **evaluation/**: Evaluation scripts and benchmarks.
- **tests/**: Unit and integration tests.
- **docs/**: Documentation files.
- **scripts/**: Miscellaneous scripts (unless explicitly called).
- Build tools (e.g., Makefile, build.sh) are not runtime components.

This list is derived from tracing imports and function calls starting from the CLI entry point. It may not be exhaustive for conditional paths (e.g., specific agents or runtimes), but covers the primary flow. If MCP or specific agents are disabled, related directories are skipped.

For a more detailed trace, you can run the CLI with debug logging enabled.