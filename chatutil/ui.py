
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
    with chat(content) as stream:
        for chunk in stream.text_stream:
            print(chunk, end="", flush=True)
        print()
