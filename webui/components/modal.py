import reflex as rx
from webui.state import State

def modal() -> rx.Component:
    """A modal to create a new chat."""
    return rx.chakra.modal(
        rx.chakra.modal_overlay(
            rx.chakra.modal_content(
                rx.chakra.modal_header(
                    rx.chakra.hstack(
                        rx.chakra.text("Create new chat"),
                        rx.chakra.icon(
                            tag="close",
                            font_size="sm",
                            on_click=State.toggle_modal,
                            color="#fff8",  # Light text/icon color can remain for contrast
                            _hover={"color": "#fff"},  # Same here for hover effect
                            cursor="pointer",
                        ),
                        align_items="center",
                        justify_content="space-between",
                    )
                ),
                rx.chakra.modal_body(
                    rx.chakra.input(
                        placeholder="Type something...",
                        on_blur=State.set_new_chat_name,
                        bg='#262730',  # Dark background color for input
                        border_color="#5F1A37",  # Use the deep maroon for border
                        _placeholder={"color": "#776885"},  # Placeholder text in lighter plum
                    ),
                ),
                rx.chakra.modal_footer(
                    rx.chakra.button(
                        "Create",
                        bg="#ce4a4e",  # Button background in deep maroon
                        box_shadow="md",
                        px="4",
                        py="2",
                        h="auto",
                        _hover={"bg": "#7f2225"},  # Hover in lighter plum
                        on_click=State.create_chat,
                    ),
                ),
                bg="#1D1C27",  # Modal background in almost black
                color="#fff",  # Text color in white for contrast
            ),
        ),
        is_open=State.modal_open,
    )
