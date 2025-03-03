
def run_info(chat, file=None):
    info = chat.info()

    print("::: chatio: model: %s tools: %s system: %s messages: %s" % (
        info.model,
        info.tools,
        info.system,
        info.messages), file=file)

def run_user(prefix=None):
    if prefix is not None:
        print(prefix, end="", flush=True)
    try:
        return input()
    except (EOFError, KeyboardInterrupt):
        return None


def _run_chat_chunk(chat, chunk, prefix=None, file=None, newline=False):
    for index, chunk_line in enumerate(chunk.splitlines()):
        if index:
            print(flush=True, file=file)
        if (index or newline) and prefix is not None:
            print(prefix, end="", flush=True, file=file)

        print(chunk_line, end="", flush=True, file=file)

    if chunk.endswith("\n"):
        print(flush=True, file=file)


def _run_chat_event(chat, event, prefix=None, file=None, newline=False):
    if not newline:
        print(flush=True, file=file)

    if prefix is not None:
        print(prefix, end="", flush=True, file=file)

    etype = event['type']
    match etype:

        case 'token_stats':
            print("token_stats: %s:" % event['scope'], end="", file=file)
            print(" input_tokens: %s" % event['input_tokens'], end="", file=file)
            print(" output_tokens: %s" % event['output_tokens'], end="", file=file)
            print(" cache_written: %s" % event['cache_written'], end="", file=file)
            print(" cache_read: %s" % event['cache_read'], end="", file=file)
            print(file=file)

        case 'tools_usage':
            print("tools_usage: %s: %s" % (event['tool_name'], event['tool_args']), file=file)

        case 'tools_event':
            print("tools_event: %s: %s" % (event['tool_name'], event['tool_data']), file=file)

        case _:
            raise RuntimeError()


def _run_chat(chat, content, prefix=None, file=None):
    isline = True

    for chunk in chat(content):
        match chunk:
            case str():
                _run_chat_chunk(chat, chunk, prefix, file, isline)
                if chunk:
                    isline = chunk.endswith("\n")
                yield chunk
            case dict():
                _run_chat_event(chat, chunk, "::: ", file, isline)
            case _:
                raise RuntimeError()


def run_chat(chat, content, prefix=None, file=None):
    return "".join(_run_chat(chat, content, prefix, file))
