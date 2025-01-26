
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
