# trace

A lightweight terminal-based AI agent prototype that interacts with local files to inspect codebases, execute scripts, fix bugs, and verify changes autonomously using multi-turn tool calling.

## File Structure

```text
.
├── main.py                # Main agent execution loop & API setup
├── call_function.py       # Function calling router & dispatcher
├── cli.py                 # CLI argument parsing
├── config.py              # Configuration settings & iteration limits
├── prompts.py             # System prompt
├── functions/             # Tool execution modules
│   ├── get_file_content.py
│   ├── get_files_info.py
│   ├── run_code.py
│   └── write_to_file.py
└── calculator/            # Sample target codebase for testing

```

## Prerequisites

* **Python 3.12+**
* **[`uv`](https://docs.astral.sh/uv/)** (recommended) or standard `pip`
* An **OpenRouter API Key**


## Setup & Environment

1. **Clone the repository:**
```bash
git clone https://github.com/nnamusoboko/trace
cd trace

```


2. **Configure API Key:**
Create a `.env` file in the root directory:
```bash
echo "OPENROUTER_API_KEY=your_api_key_here" > .env

```


3. **Set up the virtual environment:**
* **Using `uv` (Automatic):**
```bash
uv sync

```

* **Using `pip` (Manual):**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install .

```

## How to Run

Pass any request to `main.py`:

```bash
# With uv (auto-activates environment)
uv run main.py "help me find a bug in calculator and fix it"

# With activated venv
python main.py "how does the calculator render results?"

```

*Add `--verbose` to see live token counts and tool call logs.*

## How It Works

```text
User Request ──> LLM Loop ──> Tool Call (read/write/run) ──> Subprocess ──> LLM Final Answer

```

1. **Task Request:** The user provides an instruction via CLI.
2. **Tool Selection:** The LLM decides which tools (`get_files_info`, `get_file_content`, `write_file`, `run_python_file`) to invoke.
3. **Local Execution:** Functions run locally via safe subprocesses with execution timeouts to prevent infinite loops.
4. **Verification Loop:** Results return to the LLM to inspect, fix bugs, or verify script outputs until the task finishes.
