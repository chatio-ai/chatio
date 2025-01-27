
def run_user(prefix=None):
    if prefix is not None:
        print(prefix, end="", flush=True)
    try:
        return input()
    except (EOFError, KeyboardInterrupt):
        return None


def run_chat(chat, content, prefix=None):
    if prefix is not None:
        print(prefix, end="", flush=True)

    events = []

    for chunk in chat(content):
        if not isinstance(chunk, str):
            events.append(chunk)
            continue

        print(chunk, end="", flush=True)

    print()

    return events


def run_stat(events, prefix=None):

    for event in events:
        if prefix is not None:
            print(prefix, end="", flush=True)
        etype = event['type']
        if not etype:
            pass
        elif etype == 'token_stats':
            print("token_stats: input_tokens: %s / output_tokens: %s" % (event['input_tokens'], event['output_tokens']))
        elif etype == 'tools_usage':
            print("tools_usage: %s: %s" % (event['tool_name'], event['tool_args']))
        elif etype == 'tools_event':
            print("tools_event: %s: %s" % (event['tool_name'], event['tool_data']))
