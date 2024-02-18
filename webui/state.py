import os
import requests
import json
import openai
import reflex as rx
#import clipsai


openai.api_key = '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'
openai.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

BAIDU_API_KEY = os.getenv("BAIDU_API_KEY")
BAIDU_SECRET_KEY = os.getenv("BAIDU_SECRET_KEY")


if not openai.api_key and not BAIDU_API_KEY:
    raise Exception("Please set OPENAI_API_KEY or BAIDU_API_KEY")


def get_access_token():
    """
    :return: access_token
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": BAIDU_API_KEY,
        "client_secret": BAIDU_SECRET_KEY,
    }
    return str(requests.post(url, params=params).json().get("access_token"))


class QA(rx.Base):
    """A question and answer pair."""

    question: str
    answer: str


DEFAULT_CHATS = {
    "Edit 1": [QA(question='Upload an Image and Type to Edit. 🔥', answer='Go on!')],
}


class State(rx.State):
    """The app state."""

    # A dict from the chat name to the list of questions and answers.
    chats: dict[str, list[QA]] = DEFAULT_CHATS

    # The current chat name.
    current_chat = "Edit 1"

    # The current question.
    question: str

    # Whether we are processing the question.
    processing: bool = False

    # The name of the new chat.
    new_chat_name: str = ""

    # Whether the drawer is open.
    drawer_open: bool = False

    # Whether the modal is open.
    modal_open: bool = False

    api_type: str = "baidu" if BAIDU_API_KEY else "openai"

    markers: list[dict] = [{'start': 1127.62, 'end': 1161.58}, {'start': 312.18, 'end': 346.48}, {'start': 1151.24, 'end': 1183.42}, {'start': 351.1, 'end': 391.5}, {'start': 307.5, 'end': 342.14}, {'start': 256.34, 'end': 290.84}, {'start': 252.5, 'end': 287.0}, {'start': 154.38, 'end': 188.04}]

    video_segments: list[str] = []

    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of file(s) and process video.

        Args:
            files: The uploaded files.
        """
        
        '''for file in files:
            upload_data = await file.read()
            # Define the outfile path directly in the current directory with the uploaded file's name
            assets_dir = os.path.join(os.getcwd(), "assets")
            outfile = os.path.join(assets_dir, file.filename)  # os.getcwd() gets the current working directory

            # Save the file to the outfile path
            with open(outfile, "wb") as file_object:
                file_object.write(upload_data)

            # Update the state with the path to the saved file
            '''
        self.video_segments.append('pewdie.mp4')  # Appending the path of the saved file to video_paths
        '''
            Clipping done

            media_editor = clipsai.MediaEditor()
            media_file = clipsai.AudioVideoFile(outfile)
            for index, marker in enumerate(self.markers):
                start_time = marker["start"]
                end_time = marker["end"]
                save_path = os.path.join(assets_dir, 'segment_'+str(index)+'.mp4')
                media_editor.trim(
                    media_file=media_file,
                    start_time=start_time,
                    end_time=end_time,
                    trimmed_media_file_path=save_path,  # doesn't exist yet
                )
                '''

    def create_chat(self):
        """Create a new chat."""
        # Add the new chat to the list of chats.
        self.current_chat = self.new_chat_name
        self.chats[self.new_chat_name] = []

        # Toggle the modal.
        self.modal_open = False

    def toggle_modal(self):
        """Toggle the new chat modal."""
        self.modal_open = not self.modal_open

    def toggle_drawer(self):
        """Toggle the drawer."""
        self.drawer_open = not self.drawer_open

    def delete_chat(self):
        """Delete the current chat."""
        del self.chats[self.current_chat]
        if len(self.chats) == 0:
            self.chats = DEFAULT_CHATS
        self.current_chat = list(self.chats.keys())[0]
        self.toggle_drawer()

    def set_chat(self, chat_name: str):
        """Set the name of the current chat.

        Args:
            chat_name: The name of the chat.
        """
        self.current_chat = chat_name
        self.toggle_drawer()

    @rx.var
    def chat_titles(self) -> list[str]:
        """Get the list of chat titles.

        Returns:
            The list of chat names.
        """
        return list(self.chats.keys())

    #The processing function
    async def process_question(self, form_data: dict[str, str]):
        # Get the question from the form
        question = form_data["question"]

        # Check if the question is empty
        if question == "":
            return

        if self.api_type == "openai":
            model = self.openai_process_question
        else:
            model = self.baidu_process_question

        async for value in model(question):
            yield value

    async def openai_process_question(self, question: str):
        """Get the response from the API.

        Args:
            form_data: A dict with the current question.
        """

        # Add the question to the list of questions.
        qa = QA(question=question, answer="")
        self.chats[self.current_chat].append(qa)

        # Clear the input and start the processing.
        self.processing = True
        yield

        # Build the messages.
        messages = [
            {"role": "system", "content": "You are a friendly chatbot named prod.ai, a language powered video editing tool to simplify content creation."}
        ]
        for qa in self.chats[self.current_chat]:
            messages.append({"role": "user", "content": qa.question})
            messages.append({"role": "assistant", "content": qa.answer})

        # Remove the last mock answer.
        messages = messages[:-1]

        # Start a new session to answer the question.
        session = openai.ChatCompletion.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4"),
            messages=messages,
            stream=True,
        )

        # Stream the results, yielding after every word.
        for item in session:
            if hasattr(item.choices[0].delta, "content"):
                answer_text = item.choices[0].delta.content
                self.chats[self.current_chat][-1].answer += answer_text
                self.chats = self.chats
                yield

        # Toggle the processing flag.
        self.processing = False

    async def baidu_process_question(self, question: str):
        """Get the response from the API.

        Args:
            form_data: A dict with the current question.
        """
        # Add the question to the list of questions.
        qa = QA(question=question, answer="")
        self.chats[self.current_chat].append(qa)

        # Clear the input and start the processing.
        self.processing = True
        yield

        # Build the messages.
        messages = []
        for qa in self.chats[self.current_chat]:
            messages.append({"role": "user", "content": qa.question})
            messages.append({"role": "assistant", "content": qa.answer})

        # Remove the last mock answer.
        messages = json.dumps({"messages": messages[:-1]})
        # Start a new session to answer the question.
        session = requests.request(
            "POST",
            "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token="
            + get_access_token(),
            headers={"Content-Type": "application/json"},
            data=messages,
        )

        json_data = json.loads(session.text)
        if "result" in json_data.keys():
            answer_text = json_data["result"]
            self.chats[self.current_chat][-1].answer += answer_text
            self.chats = self.chats
            yield
        # Toggle the processing flag.
        self.processing = False
