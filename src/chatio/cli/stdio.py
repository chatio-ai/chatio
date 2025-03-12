
from .style import Style, Empty


def _mk_style(style=None):
    if style is None:
        return Empty
    elif isinstance(style, str):
        return Style(prefix=style)
    else:
        return style


def run_text(text, style=None, file=None):
    with _mk_style(style).wrap(file=file):
        print(text, end="", flush=True, file=file)


def run_info(chat, style=None, file=None):
    info = chat.info()

    run_text("chatio: model: %s tools: %s system: %s messages: %s" % (
            info.model,
            info.tools,
            info.system,
            info.messages), style=style, file=file)


def run_user(style=None, file=None):
    with _mk_style(style).wrap(end="", file=file):
        try:
            return input()
        except (EOFError, KeyboardInterrupt):
            return None


def _run_chat_event(event, style, file=None):

    etype = event['type']
    etext = ""

    match etype:

        case 'token_stats':
            etext = "token_stats: %s:" % event['scope']
            etext += " in: %s" % event['input_tokens']
            etext += " (hist: %s" % event['input_history_tokens']
            etext += " curr: %s)" % event['input_current_tokens']
            etext += " out: %s" % event['output_tokens']
            etext += "  "
            etext += " nc: %s" % event['cache_missed']
            etext += " cw: %s" % event['cache_written']
            etext += " cr: %s" % event['cache_read']
            etext += "  "
            etext += " pa: %s" % event['predict_accepted']
            etext += " pr: %s" % event['predict_rejected']

        case 'tools_usage':
            etext = "tools_usage: %s: %s" % (event['tool_name'], event['tool_args'])

        case 'tools_event':
            etext = "tools_event: %s: %s" % (event['tool_name'], event['tool_data'])

        case _:
            raise RuntimeError()

    with style.wrap(file=file):
        print(etext, end="", flush=True, file=file)


def _run_chat_chunk(chunk, style, hascr, file=None):

    for chunk_line in chunk.splitlines(keepends=True):
        result = ""
        if hascr:
            result += style.prefix

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
    theme = {
        'model_chunk': _mk_style(model_style),
        'tools_chunk': _mk_style(tools_style),
    }

    event_style = _mk_style(event_style)

    defer = None
    for event in events:
        etype = event.get("type")
        chunk = event.get("text")

        if not defer == etype:
            if defer:
                style = theme.get(defer, None)
                _run_chat_chunk('\n', style, not defer, file)
                defer = None

        style = theme.get(etype, event_style)
        match etype:
            case "model_chunk":
                hascr = _run_chat_chunk(chunk, style, not defer, file)
                defer = None if hascr else etype
                yield chunk
            case "tools_chunk":
                hascr = _run_chat_chunk(chunk, style, not defer, file)
                defer = None if hascr else etype
            case _:
                _run_chat_event(event, style, file)
                defer = None


def run_chat(events, model_style=None, event_style=None, tools_style=None, file=None):
    return "".join(_run_chat(events, model_style, event_style, tools_style, file))
