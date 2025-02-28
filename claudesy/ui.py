
def run_user(prefix=None):
    if prefix is not None:
        print(prefix, end="", flush=True)
    try:
        return input()
    except (EOFError, KeyboardInterrupt):
        return None


def _run_chat(chat, content, prefix=None, file=None):
    if prefix is not None:
        print(prefix, end="", flush=True)

    events = []
    result = ""

    for chunk in chat(content):
        if not isinstance(chunk, str):
            events.append(chunk)
            continue

        result += chunk
        for index, chunk_line in enumerate((chunk + "\n").splitlines()):
            if index:
                print(flush=True, file=file)
            if index and prefix is not None:
                print(prefix, end="", flush=True, file=file)

            print(chunk_line, end="", flush=True, file=file)

        if file:
            chunk_raw = chunk.replace('\\', '\\\\').replace('\n', '\\n')
            print(chunk_raw, end="", flush=True)

    print(file=file)
    print(file=file)

    if file:
        print()
        print()

    return events, result


def run_chat(chat, content, prefix=None, file=None):
    events, result = _run_chat(chat, content, prefix, file)
    return events


def run_stat(events, prefix=None, file=None):

    for event in events:
        if prefix is not None:
            print(prefix, end="", flush=True, file=file)
        etype = event['type']
        if not etype:
            pass
        elif etype == 'token_stats':
            print("token_stats: %s: input_tokens: %s / output_tokens: %s / cache_written: %s / cache_read: %s" % (
                event['scope'], event['input_tokens'], event['output_tokens'], event['cache_written'], event['cache_read']), file=file)
        elif etype == 'tools_usage':
            print("tools_usage: %s: %s" % (event['tool_name'], event['tool_args']), file=file)
        elif etype == 'tools_event':
            print("tools_event: %s: %s" % (event['tool_name'], event['tool_data']), file=file)
        else:
            raise RuntimeError()
