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
            {"role": "system","content": "You are an AI assistant tasked with helping editors trim their videos that they streamed, in a shorter form that attracts more viewers. Your role is to analyze the user’s prompt, identify the keywords and run our functions based on this function map '{\"trim_video(self, trim_start_sec, trim_end_sec)\": 1, \"crop_video(self, scale)\": 2,\"zoom_video(self, zoom_scale)\": 3, \"change_speed(self, speed_factor)\": 4, \"fade_in_video(self, duration=2)\": 5, \"fade_out_video(self, duration=2)\": 6}'. *Explanation of these functions* 'trim_video(self, trim_start_sec, trim_end_sec)' is a function that cuts the video out for 'trim_start_sec' seconds from the beginning and for 'trim_end_sec' seconds from the end. If no value is given, assume trim_start_sec and trim_end_sec to be 2 seconds. 'crop_video(self, scale)' adjusts the video’s aspect ratio and dimensions to fit mobile viewing or some other application where cropping is required based on an integer value 'scale' If the ‘scale’ value isn’t given, assume it to be 2. 'zoom_video(self, zoom_scale)' zooms into the video if zoom_scale is a positive integer value greater than 1. Assume the zoom_scale to be 2 if no value is given. 'change_speed(self, speed_factor)' increases the speed of the video based on the integer value of 'speed_factor.' If it’s greater than 1, we increase the speed of the video by that factor. If speed_factor is a negative value, we decrease the speed of the video by a factor of that value. Assume the speed_factor to be 2, if no value is given. 'fade_in_video(self, duration=2)' this function applies a fade in effect to the video for a duration of an integer value represented in the 'duration' parameter. If no value is given, assume the duration to be 2 seconds. 'fade_out_video(self, duration=2)' does the exact opposite of fade_in_video(self, duration=2)'. It applies a fade out effect to the video for a duration of that integer value represented in the duration parameter. If no duration is given, assume the duration to be 2 seconds If any of the parameters is incorrectly inputted by the user or is invalid based on the above description, use the default values as mentioned. The output must strictly adhere to the following format and guidelines:\\n\\n1. *Output Format: It is EXTREMELY IMPORTANT and STRICT that the response is outputted in a JSON Structure. The JSON object should include a list of commands to execute, where each command has the value of the function to call in the corresponding function map, the integer values representing the parameters to those functions, and a justification field \\n - Ensure the keywords match currently with the function parameters.\\n\\n4. **Example Output Structure*:\njson\n{\n  \"clip\": [\n    {\"function_id\": 1, \"parameters\": [12,15]},\n    {\"function_id\": 2, \"parameters\": [2]}, {\"function_id\": 3, \"parameters\": [2]}, {\"function_id\": 4, \"parameters\": [1]}, {\"function_id\": 5, \"parameters\": [2]}, {\"function_id\": 6, \"parameters\": [3]}'\n ],\n  \"justification\": \"Sure, based on the given information, I will show you, your clips. [Brief explanation of what ‘s happening to the video, and how you are defaulting values if no values are given by the user].\"\n}\n\n\nIt is EXTREMELY IMPORTANT and STRICT that the response is outputted as a JSON String within "}
        ]

        for qa in self.chats[self.current_chat]:
            messages.append({"role": "user", "content": qa.question})
            messages.append({"role": "assistant", "content": qa.answer})

        # Remove the last mock answer.
        messages = messages[:-1]
        response = openai.ChatCompletion.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4"),
            temperature=0.7,
            max_tokens=300,
            messages=messages,
            stream=True
        )

        # Stream the results, yielding after every word.
        for item in response:
            if hasattr(item.choices[0].delta, "content"):
                # if answer_text.strip():
                answer_text = item.choices[0].delta.content
                '''if "" in answer_text:
                    parts = answer_text.split("```")
                    json_str = parts[1] if len(parts) > 1 else ""
                    if json_str != "":
                        json_str = json_str.split("json ") 
                        json_obj = json.loads(json_str)
                        function_ids = [item["function_id"] for item in json_obj["clip"]]
                        parameters = [item["parameters"] for item in json_obj["clip"]]
                        justification = json_obj["justification"]
                        self.chats[self.current_chat][-1].answer += justification
                        self.chats = self.chats
                        yield
                else:
                    '''
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
