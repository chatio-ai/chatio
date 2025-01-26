
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

    for chunk in chat(content):
        print(chunk, end="", flush=True)

    print()


def run_stat(chat, prefix=None):

    while chat.events:
        event = chat.events.pop(0)
        if prefix is not None:
            print(prefix, end="", flush=True)
        etype = event['type']
        if not etype:
            pass
        elif etype == 'usage':
            print("usage: input_tokens: %s / output_tokens: %s" % (event['input_tokens'], event['output_tokens']))
        elif etype == 'tools':
            print("tools: %s: %s" % (event['tool_name'], event['tool_args']))
