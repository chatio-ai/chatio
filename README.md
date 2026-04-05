# chatio

ultra-lightweight llm streaming swiss-knife

Python CLI and library for async streaming chat with 15+ LLM providers.

![](doc/chatio.gif)

## Features

- **15+ providers** via 3 native APIs (Anthropic, OpenAI, Google) plus an OpenAI-compatible layer
- **Async streaming** for all providers
- **Built-in tools** -- shell, calculator, web search, web browse, Wikipedia, image analysis, nested LLM
- **CLI modes** -- interactive chat, two-LLM loop, token counter
- **File attachments** -- images, text, PDFs
- **Extensible** -- add a new provider with a single TOML file
- **Docker ready**

## Quick Start

Requires Python 3.12+.

```bash
pip install .
```

Set your model and API key, then run:

```bash
export CHATIO_MODEL_NAME="claude/claude-sonnet-4-5"
export ANTHROPIC_API_KEY="sk-..."
chatio
```

As a library:

```python
import asyncio
from chatio.misc import build_chat
from chatio.core.events import ModelTextChunk

async def main():
    chat = build_chat()
    async with chat:
        chat.state.append_input_message("Hello!")
        async for event in chat.stream_content():
            match event:
                case ModelTextChunk(text):
                    print(text, end="", flush=True)
    print()

asyncio.run(main())
```

`build_chat()` reads `CHATIO_MODEL_NAME` and `CHATIO_TOOLS_NAME` / `CHATIO_TOOLS_LIST` from environment variables.

## Configuration

All configuration is done through environment variables.

| Variable | Description | Example |
|---|---|---|
| `CHATIO_MODEL_NAME` | Vendor/model (required) | `openai/gpt-4o` |
| `{VENDOR}_API_KEY` | API key (vendor name uppercased) | `ANTHROPIC_API_KEY=sk-...` |
| `{VENDOR}_BASE_URL` | Custom base URL | `OPENAI_BASE_URL=https://...` |
| `CHATIO_TOOLS_NAME` | Tool preset (`default`, `llmtool`, `imgtool`, `empty`) | `default` |
| `CHATIO_TOOLS_LIST` | Comma-separated tool keys | `web,wiki,sh` |
| `CHATIO_VENDORS_PATH` | Colon-separated custom vendor config dirs | `/path/to/vendors` |
| `CHATIO_VENDOR_CONFIG` | JSON config override (merged into vendor TOML) | `{"format":{"compat":true}}` |

Model name format is `vendor/model-name`. Some vendors override the API key env var via `env_ns` in their TOML config (e.g. `qwq` uses `DASHSCOPE_API_KEY`, `xiaomi` uses `MIMO_API_KEY`).

## Supported Providers

### API Backends

| Backend | Description |
|---|---|
| `claude` | Native Anthropic/Claude API |
| `google` | Native Google Gemini API |
| `openai` | Native OpenAI API + OpenAI-compatible endpoints |
| `compat` | Generic OpenAI-compatible layer |

### Vendors

| Vendor | Backend | Aliases |
|---|---|---|
| anthropic | `claude` | `claude` |
| hailuo (MiniMax) | `claude` | |
| google | `google` | `gemini` |
| openai | `openai` | `chatgpt` |
| deepseek | `openai` | `ds` |
| openrouter | `openai` | `router` |
| together | `openai` | |
| xai | `openai` | `grok`, `grokai` |
| moonshot | `openai` | `kimi` |
| qwq (DashScope) | `openai` | `alibaba`, `qwenai` |
| mistral | `compat` | |
| perplexity | `compat` | `pplx` |
| novita | `compat` | |
| zai | `compat` | |
| xiaomi | `compat` | |

The `compat/` directory also provides OpenAI-compatible variants for google and hailuo.

Add a new provider with a TOML file -- see `share/vendors/` for examples.

## Tools

Control tools with `CHATIO_TOOLS_NAME` (presets) or `CHATIO_TOOLS_LIST` (individual keys).

| Key | Tools | Description |
|---|---|---|
| `sh` | shell_exec, shell_calc | Run shell commands, evaluate expressions |
| `web` | DuckDuckGo search, web browse | Web search and page fetching |
| `wiki` | wiki_content, wiki_summary, wiki_section, wiki_search | Wikipedia lookup |
| `img` | image_dump | Image analysis |
| `llm` | llm_dialog | Nested LLM conversation (uses `CHATIO_NESTED_*` env vars) |
| `noop` | do_nothing | Placeholder tool |

**Presets:** `default` = sh + wiki + web + noop, `llmtool` = llm, `imgtool` = img, `empty` = none

## CLI Commands

| Command | Description |
|---|---|
| `chatio` | Interactive multi-turn chat with colored output and file attachments |
| `chatio-loop <dir>` | Two-LLM autonomous conversation using prompts from `<dir>` |
| `chatio-tcnt` | Count tokens from stdin for current model |

## Docker

Build:

```bash
docker build -t chatio/chatio .
```

Run:

```bash
docker run --rm -it \
  -e CHATIO_MODEL_NAME="claude/claude-sonnet-4-5" \
  -e ANTHROPIC_API_KEY \
  chatio/chatio -- "You are a helpful cooking assistant"
```
