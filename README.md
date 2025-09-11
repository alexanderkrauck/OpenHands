# OpenHands CLI

OpenHands is an autonomous AI software engineer capable of executing complex engineering tasks through a command-line interface.

## Installation

### Prerequisites
- Python 3.11+ 
- Poetry or pip
- Docker (optional, for sandboxed execution)

### Install from source

```bash
# Clone the repository
git clone https://github.com/All-Hands-AI/OpenHands.git
cd OpenHands

# Using Poetry (recommended)
poetry config virtualenvs.in-project true
poetry install

# Or using pip
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Quick Install with uv

```bash
# Install and run CLI directly
uvx --python 3.12 --from openhands-ai openhands
```

## Usage

### Basic CLI Usage

```bash
# Run with a task
openhands "Write a Python function that calculates factorial"

# Use a specific model
openhands --llm-model claude-3-5-sonnet-20241022 "Create a web scraper"

# Set API keys
export ANTHROPIC_API_KEY=your_key_here
export OPENAI_API_KEY=your_key_here
```

### Configuration

Create a `config.toml` file based on `config.template.toml`:

```toml
[llm]
model = "claude-3-5-sonnet-20241022"
api_key = "your-api-key"

[runtime]
type = "local"  # or "docker"
```

### CLI Commands

While in a session, you can use these commands:
- `/help` - Show available commands
- `/exit` - Exit the session
- `/finish` - Mark task as complete
- `/settings` - Modify LLM settings

## Core Components

### Essential Directories
- `openhands/cli/` - CLI interface and commands
- `openhands/core/` - Core configuration and setup
- `openhands/controller/` - Agent control and execution
- `openhands/agenthub/` - Available agents
- `openhands/runtime/` - Execution environments
- `openhands/events/` - Event system
- `openhands/memory/` - Agent memory management
- `microagents/` - Microagent definitions
- `.openhands/` - Local configuration and microagents

## Available LLM Models

OpenHands supports various LLM providers:
- **Anthropic**: Claude models (recommended)
- **OpenAI**: GPT-4, GPT-3.5
- **Local models**: Via Ollama or other providers

See the [LLM configuration guide](https://docs.all-hands.dev/usage/llms) for details.

## Runtime Environments

- **Local**: Direct execution on your machine
- **Docker**: Sandboxed execution in containers (safer for untrusted code)

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## Support

- [GitHub Issues](https://github.com/All-Hands-AI/OpenHands/issues)
- [Documentation](https://docs.all-hands.dev)
- [Slack Community](https://dub.sh/openhands)
- [Discord](https://discord.gg/ESHStjSjD4)

## Citation

```
@inproceedings{
  wang2025openhands,
  title={OpenHands: An Open Platform for {AI} Software Developers as Generalist Agents},
  author={Xingyao Wang and Boxuan Li and Yufan Song and Frank F. Xu and Xiangru Tang and Mingchen Zhuge and Jiayi Pan and Yueqi Song and Bowen Li and Jaskirat Singh and Hoang H. Tran and Fuqiang Li and Ren Ma and Mingzhang Zheng and Bill Qian and Yanjun Shao and Niklas Muennighoff and Yizhe Zhang and Binyuan Hui and Junyang Lin and Robert Brennan and Hao Peng and Heng Ji and Graham Neubig},
  booktitle={The Thirteenth International Conference on Learning Representations},
  year={2025},
  url={https://openreview.net/forum?id=OJd3ayDDoF}
}
```