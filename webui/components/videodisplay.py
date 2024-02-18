import reflex as rx
from webui.state import State  # Assuming State is defined with necessary video handling logic
from webui import styles

class VideoDisplayState(State):
    @rx.var
    def dynamic_section(self) -> rx.Component:
        """Dynamically returns a section based on the presence of video segments."""
        video_segments = self.video_segments  # Assuming this is populated with video URLs
        if len(video_segments) > 0:
            videos_html = "<script src='./custom_video_controls.js'></script><div style='width: 100%;'>"
            for url_v in video_segments[:1]:
                videos_html += f"""
                <div class="custom-video-player" style="max-width: 100%; overflow: hidden;"> <!-- Ensure the video player doesn't exceed the screen width -->
                    <video id="video_1" width="auto" height="auto" controls autoplay loop muted style="max-height: 440px; width: 100%; align-self: center;">
                        <source src="/{url_v}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                    <!-- Container for the play/pause button, image, and mini video player -->
                    <div style="display: flex; align-items: center; justify-content: center; padding: 10px; gap: 10px; box-sizing: border-box; width: '100%'"> <!-- Added gap and box-sizing -->
                        <div style="flex: 0 0 30%; display: flex; flex-direction: column; align-items: center;"> <!-- Wrapper for buttons to control width and alignment -->
                            <button id="playPauseBtn" data-video-id="video_1" style="background-color: #ce4a4e; border-radius: 10px; padding: 10px 20px; color: white; cursor: pointer; width: 100%;">Pause</button>
                            <button disabled style="background-color: #ce4a4e; border-radius: 10px; padding: 10px 20px; color: white; cursor: not-allowed; width: 100%; opacity: 0.5; margin-top: 10px;" id="swap">Edit this ➡️</button> <!-- New disabled button -->
                        </div>
                                        
                        <!-- Thin Image -->
                        <img src="/arrow.png" alt="Thin Image" style="flex: 0 0 5%; height: auto; max-height: 140px;"> <!-- Adjust the src and styles as needed -->
                                        
                        <!-- Mini Video Player -->
                        <div class="mini-video-player" style="flex: 0 0 50%; display: flex; flex-direction: column; align-items: center;">
                            <video id="mini_video_1" width="300" height="140" loop muted style="border: 2px solid #9B6A6C; border-radius: 5px;" controls autoplay>
                                <source src="/{url_v}" type="video/mp4">
                                Your browser does not support the video tag.
                            </video>
                            <div id="miniPlayerMessage" style="display: none; padding-top: 3px;">Last Clip</div>
                        </div>
                    </div>
                    <div class="seek-bar-container" style="position: relative; width: 100%;">
                        <input type="range" id="seekBar" value="0" min="0" max="100" step="1" style="width: 100%; z-index: 2; position: relative;">
                        <canvas id="highlightCanvas" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 2; pointer-events: none; opacity: 0.4;"></canvas>
                    </div>
                    <!-- Additional custom controls here -->
                </div>
                """
            videos_html += "</div>"
            return videos_html
        else:
            return "<p style='font-size: large; padding: 50px;`'>Upload a Stream to Start Editing! ⏩</p>"
        
    # videos_html now contains the HTML string to be used


def videodisplay():
    """Component for uploading and displaying video segments."""
    color = "#5ea09e"
    # Define the upload and action buttons section
    upload_section = rx.chakra.vstack(
        rx.upload(
            rx.chakra.vstack(
                rx.button("Select File", _hover={"bg": '#7f2225'}, style=styles.input_style),
                rx.text("Drag and drop Stream here or Click to Select 📀"),
            ),
            border=f"1px dotted {color}",
            padding="50px",
            border_radius="lg"
        ),
        rx.hstack(rx.foreach(rx.selected_files, rx.text)),
        rx.button(
            "Upload",
            on_click=lambda: State.handle_upload(rx.upload_files()),
            bg=color
        ),
        rx.button(
            "Clear",
            on_click=rx.clear_selected_files,
            bg=color
        ),
        rx.chakra.heading("What is this?", size="lg", padding_top="10", padding_bottom="2", align="center"),
        rx.chakra.text("""
        Chopsticks is the premier AI-powered editing software that utilizes deep learning to improve efficiency, 
        enhance user experience, and (amazingly) _increase_ creator profits.
        """, padding_y="5", align="center"),
        rx.chakra.image(
            src="/arrow.png",
            padding_y="5",
            align="center",  # This assumes there's an align prop; if not, alignment might need to be handled by the parent
            width="100px",
        ),
        spacing="4",
    )
    
    # Define the video display section
    video_display_section = rx.grid(
        rx.foreach(
            State.video_segments,
            lambda url_v: rx.video(url=('/' + url_v), width="100%", height="auto", playing=True, loop=True, controls=True, muted=True)
        ),
        columns="1",
        width="100%",
    )
    
    # Define the message section
    message_section = rx.chakra.text("Hi!", font_size="lg", padding="4")
    
    #returned_section = (video_display_section if len(State.video_segments) >0 else message_section)

    # Combine sections into a split layout
    return rx.chakra.box(
        rx.chakra.hstack(
            rx.chakra.box(
                upload_section,
                width="40%",
                margin="0px",
                padding="10px",
                flex_grow="1",
                align_self="start",
            ),
            rx.chakra.box(rx.html(VideoDisplayState.dynamic_section), width="60%", border_radius="lg", padding="10px", flex_grow="1", text_align="center", bg='rgba(255,255,255, 0.1)', align_items="center"),
            spacing="4",
            align_items="start",
            justify_content="start",
        ),
        flex_grow="1",
        padding_right="20px",
    )