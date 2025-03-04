
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


def _run_chat_event(event, style, file=None, newline=False):
    if not newline:
        print(flush=True, file=file)

    etype = event['type']
    etext = ""

    match etype:

        case 'token_stats':
            etext = "token_stats: %s:" % event['scope']
            etext += " input_tokens: %s" % event['input_tokens']
            etext += " output_tokens: %s" % event['output_tokens']
            etext += " cache_written: %s" % event['cache_written']
            etext += " cache_read: %s" % event['cache_read']

        case 'tools_usage':
            etext = "tools_usage: %s: %s" % (event['tool_name'], event['tool_args'])

        case 'tools_event':
            etext = "tools_event: %s: %s" % (event['tool_name'], event['tool_data'])

        case _:
            raise RuntimeError()

    with style.wrap(file=file):
        print(etext, end="", flush=True, file=file)


def _run_chat_chunk(chunk, style, file=None, newline=False):
    for index, chunk_line in enumerate(chunk.splitlines()):
        if index:
            print(style.suffix, flush=True, file=file)
        if index or newline:
            print(style.prefix, end="", flush=True, file=file)

        print(chunk_line, end="", flush=True, file=file)

    if chunk.endswith("\n"):
        print(style.suffix, flush=True, file=file)


def _run_chat(chat, content, model_style=None, event_style=None, tools_style=None, file=None):
    model_style = _mk_style(model_style)
    event_style = _mk_style(event_style)
    tools_style = _mk_style(tools_style)

    isline = True
    for event in chat(content):
        etype = event.get("type")
        chunk = event.get("text")
        match etype:
            case "model_chunk":
                _run_chat_chunk(chunk, model_style, file, isline)
                if chunk:
                    isline = chunk.endswith("\n")
                yield chunk
            case "tools_chunk":
                _run_chat_chunk(chunk, tools_style, file, isline)
            case _:
                _run_chat_event(event, event_style, file, isline)


def run_chat(chat, model_style=None, event_style=None, tools_style=None, file=None):
    return "".join(_run_chat(chat, None, model_style, event_style, tools_style, file))
