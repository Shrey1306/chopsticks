"""The main Chat app."""

import reflex as rx

from webui import styles
from webui.components import chat, modal, navbar, sidebar, videodisplay
from webui.state import State

@rx.page(
    title="Chopsticks", 
)

def index() -> rx.Component:
    """The main app."""
    return rx.chakra.vstack(
        rx.script(src='/custom_video_controls.js'),
        navbar(),
        rx.chakra.hstack(
            rx.scroll_area(  # Scrollable area for the videodisplay
                rx.chakra.flex(  # Flex container for the videodisplay content
                    videodisplay(),  # Assuming videodisplay() returns the content to display
                    direction="column",
                    spacing="4",
                ),
                type="always",
                scrollbars="vertical",
                style={"height": "calc(100vh - 20vh)", "width": "80%", "borderRightWidth": '1px', 'borderColor': 'white'},
            
            ),
            rx.scroll_area(  # Scrollable area for the chat
                rx.chakra.flex(  # Flex container for the chat content
                    chat.chat(),  # Assuming chat.chat() returns the chat component
                    direction="column",
                    spacing="4",
                ),
                type="always",
                scrollbars="vertical",
                style={"height": "calc(100vh - 20vh)", "width": "20%"},
            ),
            align="stretch",
            spacing="0",
        ),
        chat.action_bar(),
        sidebar(),
        modal(),
        bg=styles.bg_dark_color,
        color=styles.text_light_color,
        min_h="100vh",
        align_items="stretch",
        spacing="0",
    )

# Add state and page to the app.
app = rx.App(style=styles.base_style)
app.add_page(index)
