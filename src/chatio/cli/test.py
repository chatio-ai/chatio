
# ruff: noqa: ERA001

from chatio.chat import Chat
from chatio.misc import build_chat

from ._cli.stdio import run_info, run_chat
from ._cli import entry_point


def makechat() -> Chat:

    prompt = "Отвечай на русском"
    prompt = "duplicate user message as is"
    prompt = """\
You are 'determenistic parrot' system.
Each user's message should be repeated back to them.
Reproduce user message as verbatim as possible.
Do not remove anything and do not add anything!
"""

    messages = [
        "How do you do? duplicate my message as is",
        "How do you do? duplicate my message as is",

        "<data>data</data>\n\nWhat is my data? duplicate my message as is",
        "<data>data</data>\n\nWhat is my data? duplicate my message as is",

        "[content description]\n\nWhat is my content about? duplicate my message as is",
        "[content description]\n\nWhat is my content about? duplicate my message as is",
    ]

    for _ in range(5):
        messages += [
            (
                "[abra cadabra] something strange and not sdf;sljkdfs;ldk sdf "
                "<content>sdflskdgjlskdjgsldkgj</content> duplicate my message as is"
            ),
            (
                "[abra cadabra] something strange and not sdf;sljkdfs;ldk sdf "
                "<content>sdflskdgjlskdjgsldkgj</content> duplicate my message as is"
            ),
        ]

    for _ in range(5):
        messages += [
            (
                "any random text and markup <data>here is the data</data>\n\n"
                "duplicate my message as is"
            ),
            (
                "any random text and markup <data>here is the data</data>\n\n"
                "duplicate my message as is"
            ),
        ]

    for _ in range(5):
        messages += [
            "any random text and markup <data>here is the data</data>",
            "any random text and markup <data>here is the data</data>",
        ]

    for _ in range(5):
        messages += [
            "content.jpeg [Image depicting holy grail of Roman Empire]",
            "content.jpeg [Image depicting holy grail of Roman Empire]",
        ]

    return build_chat(prompt, messages)


@entry_point
def main(*filenames: str) -> None:

    with makechat() as chat:

        run_info(chat)

        for filename in filenames:
            chat.state.attach_document_auto(file=filename)

        # chat.state.append_input_message("duplicate my message as is")

        run_info(chat)

        print()

        if filenames:
            run_chat(chat.stream_content())

        chat.state.append_input_message("what is the exact text on first image?")
        # chat.state.append_input_message("duplicate my message as is")

        run_chat(chat.stream_content())

        print()
