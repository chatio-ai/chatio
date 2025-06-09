
import atexit
import readline

from contextlib import suppress

from .style import Style, Empty


class SetupHistory:
    _HISTORY_FILE = '.chatio_history'

    def __init__(self):
        self._done = False

    def __call__(self):
        self.do_setup()

    def do_setup(self):
        if self._done:
            return

        with suppress(FileNotFoundError):
            readline.read_history_file(self._HISTORY_FILE)

        atexit.register(readline.write_history_file, self._HISTORY_FILE)

        self._done = True


setup_history = SetupHistory()


def _mk_style(style=None):
    if style is None:
        return Empty

    if isinstance(style, str):
        return Style(prefix=style)

    return style


def run_text(text, style=None, file=None):
    with _mk_style(style).wrap_print(file=file):
        print(text, end="", flush=True, file=file)


def run_info(chat, style=None, file=None):
    info = chat.info()

    run_text(
        f"chatio: model: {info.vendor}/{info.model} "
        f"tools: {info.tools} system: {info.system} messages: {info.messages}",
        style=style, file=file)


def run_user(style=None, file=None):
    setup_history()
    with _mk_style(style).wrap_input(end="", file=file) as prompt:
        try:
            return input(prompt)
        except (EOFError, KeyboardInterrupt):
            return None


def _run_chat_event(event, style, file=None):

    etype = event['type']
    etext = ""

    match etype:

        case 'token_stats':
            etext = f"token_stats: {event['scope']}:"
            etext += f" in: {event['input_tokens']}"
            etext += f" (hist: {event['input_history_tokens']}"
            etext += f" curr: {event['input_current_tokens']})"
            etext += f" out: {event['output_tokens']}"
            etext += "  "
            etext += f" nc: {event['cache_missed']}"
            etext += f" cw: {event['cache_written']}"
            etext += f" cr: {event['cache_read']}"
            etext += "  "
            etext += f" pa: {event['predict_accepted']}"
            etext += f" pr: {event['predict_rejected']}"

        case 'tools_usage':
            etext = f"tools_usage: {event['tool_name']}: {event['tool_args']}"

        case 'tools_event':
            etext = f"tools_event: {event['tool_name']}: {event['tool_data']}"

        case _:
            raise RuntimeError

    with style.wrap_print(file=file):
        print(etext, end="", flush=True, file=file)


def _run_chat_chunk(chunk, style, hascr, file=None):

    for chunk_line in chunk.splitlines(keepends=True):
        result = ""
        if hascr:
            result += style.color + style.prefix

        hascr = chunk_line.endswith("\n")
        if hascr:
            result += chunk_line[:-1]
            result += style.suffix
            result += "\n"
        else:
            result += chunk_line

        print(result, end="", flush=True, file=file)

    return hascr


def _run_chat(events, model_style=None, event_style=None, tools_style=None, file=None):
    model_style = _mk_style(model_style)
    tools_style = _mk_style(tools_style)
    event_style = _mk_style(event_style)

    defer = None
    for event in events:
        etype = event.get("type")
        label = event.get("label")

        style = None
        match etype, label:
            case "model_chunk", None:
                style = model_style
            case "model_chunk", _:
                style = tools_style
            case "tools_chunk", _:
                style = tools_style
            case _, _:
                style = event_style

        if defer != style and defer:
            _run_chat_chunk('\n', style, not defer, file)
            defer = None

        chunk = event.get("text")
        match etype:
            case "model_chunk":
                hascr = _run_chat_chunk(chunk, style, not defer, file)
                defer = None if hascr else style
                yield chunk
            case "tools_chunk":
                hascr = _run_chat_chunk(chunk, style, not defer, file)
                defer = None if hascr else style
            case _:
                _run_chat_event(event, style, file)
                defer = None


def run_chat(events, model_style=None, event_style=None, tools_style=None, file=None):
    return "".join(_run_chat(events, model_style, event_style, tools_style, file))
