
def run_user(prefix=None):
    if prefix is not None:
        print(prefix, end="", flush=True)
    try:
        return input()
    except (EOFError, KeyboardInterrupt):
        return None


def run_chat(chat, content, prefix=None, file=None):
    if prefix is not None:
        print(prefix, end="", flush=True)

    events = []

    for chunk in chat(content):
        if not isinstance(chunk, str):
            events.append(chunk)
            continue

        print(chunk, end="", flush=True, file=file)

        if file:
            chunk_raw = chunk.replace('\\', '\\\\').replace('\n', '\\n')
            print(chunk_raw, end="", flush=True)

    print(file=file)

    if file:
        print()

    return events


def run_stat(events, prefix=None, file=None):

    for event in events:
        if prefix is not None:
            print(prefix, end="", flush=True, file=file)
        etype = event['type']
        if not etype:
            pass
        elif etype == 'token_stats':
            print("token_stats: round: input_tokens: %s / output_tokens: %s / cache_written: %s / cache_read: %s" % (
                event['input_tokens'], event['output_tokens'], event['cache_written'], event['cache_read']), file=file)
            if prefix is not None:
                print(prefix, end="", flush=True, file=file)
            print("token_stats: total: input_tokens: %s / output_tokens: %s / cache_written: %s / cache_read: %s" % (
                event['input_tokens_total'], event['output_tokens_total'], event['cache_written_total'], event['cache_read_total']), file=file)
        elif etype == 'tools_usage':
            print("tools_usage: %s: %s" % (event['tool_name'], event['tool_args']), file=file)
        elif etype == 'tools_event':
            print("tools_event: %s: %s" % (event['tool_name'], event['tool_data']), file=file)
        else:
            raise RuntimeError()
