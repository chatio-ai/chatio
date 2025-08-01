
from chatio.misc import build_chat

from ._cli.stdio import run_info, run_user_extra, run_chat
from ._cli.style import Theme, Color
from ._cli import entry_point


@entry_point
def main(*args: str) -> None:

    prompt = " ".join(args)

    input_theme = Theme(direction=Theme.INPUT, color=Color.BRIGHT_GREEN)
    model_theme = Theme(direction=Theme.OUTPUT, color=Color.BRIGHT_CYAN)

    with build_chat(prompt) as chat:

        run_info(chat, model_theme)

        results = None
        while True:
            print()
            content, files = run_user_extra(input_theme)
            if content is None:
                break
            if not files and not content:
                continue

            for file in files:
                chat.state.attach_document_auto(file=file)

            if content:
                chat.state.append_input_message(content)

            chat.state.update_prediction_message(results)

            print()
            results = run_chat(chat.stream_content(), model_theme)

        print()
