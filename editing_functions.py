import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import cv2
import numpy as np
import tempfile
import os
import ffmpeg

class VideoProcessor(QThread):
    update_signal = pyqtSignal(QImage)
    finished = pyqtSignal()

    def __init__(self, video_path):
        super().__init__()
        self.original_video_path = video_path
        self.video_path = video_path
        self.video_history = [video_path]  # Initialize history with the original path
        self.running = True
        self.trim_required = False
        self.start_sec = 0
        self.end_sec = 0

    def run(self):
        while self.running:
            if self.trim_required:
                self.trim_video(self.start_sec, self.end_sec)
                self.trim_required = False
                self.finished.emit()
            self.play_video()

    #Trimming feature
    def trim_video(self, trim_start_sec, trim_end_sec):
        probe = ffmpeg.probe(self.video_path)
        total_duration = float(probe['format']['duration'])
        
        # Adjust the start and end times based on the trimming requirements
        adjusted_start_sec = trim_start_sec  # Start trimming 1 second into the video
        adjusted_end_sec = total_duration - trim_end_sec  # End trimming 1 second before the video ends
        
        # Calculate the new duration to keep after trimming from both ends
        duration_to_keep = adjusted_end_sec - adjusted_start_sec
        
        if duration_to_keep <= 0:
            print("Error: The resulting duration is non-positive after trimming.")
            return
        
        temp_video_path = tempfile.mktemp(suffix='.mp4')
        
        try:
            # Use 'ss' for the adjusted start time and 't' for the duration to keep
            (
                ffmpeg
                .input(self.video_path, ss=adjusted_start_sec, t=duration_to_keep)
                .output(temp_video_path, c='copy')  # Use 'copy' to avoid re-encoding
                .run(overwrite_output=True)
            )
            self.video_path = temp_video_path  # Update self.video_path to use the trimmed video
            self.video_history.append(self.video_path)
        except ffmpeg.Error as e:
            print(f"Failed to trim video: {e.stderr.decode() if e.stderr else 'Unknown FFmpeg error'}")

    #Cropping feature by a specific scale
    def crop_video(self, scale):
        # Fetch video dimensions using ffprobe
        probe = ffmpeg.probe(self.video_path)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        original_width = int(video_stream['width'])
        original_height = int(video_stream['height'])
    
        # Calculate new width to make the video vertical with the same height
        new_width = original_height*scale # For a mobile-friendly vertical aspect ratio
    
        # Ensure new width is an even number (required by some codecs)
        if new_width % 2 != 0:
            new_width -= 1
    
        # Calculate the horizontal offset to crop the video from the center
        x_offset = (original_width - new_width) // 2
    
        # Prepare the crop filter dimensions
        crop_filter = f"{new_width}:{original_height}:{x_offset}:0"
    
        # Generate a temporary path for the cropped video
        temp_video_path = tempfile.mktemp(suffix='.mp4')
    
        try:
            # Apply the crop filter and save the output to a temporary file
            (
                ffmpeg
                .input(self.video_path)
                .filter('crop', *crop_filter.split(':'))
                .output(temp_video_path, vcodec='libx264', crf=22)  # Re-encode for compatibility
                .overwrite_output()
                .run()
            )
            self.video_path = temp_video_path  # Update to use the cropped video
            self.video_history.append(self.video_path)
        except ffmpeg.Error as e:
            print(f"Failed to crop video: {e.stderr.decode('utf-8')}")
            
    #Zooming in only (out is undo)
    def zoom_video(self, zoom_scale):
        # Fetch video dimensions using ffprobe
        probe = ffmpeg.probe(self.video_path)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        original_width = int(video_stream['width'])
        original_height = int(video_stream['height'])
    
        # Calculate the new dimensions based on the zoom scale
        new_width = int(original_width * zoom_scale)
        new_height = int(original_height * zoom_scale)
    
        # Ensure the new dimensions are even
        new_width += (new_width % 2)
        new_height += (new_height % 2)
    
        # Calculate the offsets to keep the crop centered
        x_offset = (original_width - new_width) // 2
        y_offset = (original_height - new_height) // 2
    
        # Generate a temporary path for the zoomed video
        temp_video_path = tempfile.mktemp(suffix='.mp4')
    
        try:
            # Apply the crop filter with calculated dimensions and offsets
            (
                ffmpeg
                .input(self.video_path)
                .filter('crop', w=new_width, h=new_height, x=x_offset, y=y_offset)
                .output(temp_video_path, vcodec='libx264', crf=22)  # Re-encode for compatibility
                .overwrite_output()
                .run()
            )
            self.video_path = temp_video_path  # Update to use the zoomed video
            self.video_history.append(self.video_path)  # Add to history for undo functionality
        except ffmpeg.Error as e:
            print(f"Failed to zoom video: {e.stderr.decode('utf-8')}")

    #Speed changing
    def change_speed(self, speed_factor):
        """
        Changes the speed of the video.
        A speed_factor > 1.0 speeds up the video.
        A speed_factor < 1.0 slows down the video.
        """
        temp_video_path = tempfile.mktemp(suffix='.mp4')
        
        try:
            # The filter 'setpts' adjusts the presentation timestamp of each frame
            # Speeding up (reducing duration) if speed_factor > 1, 
            # Slowing down (increasing duration) if speed_factor < 1
            (
                ffmpeg
                .input(self.video_path)
                .filter('setpts', f'{1/speed_factor}*PTS')
                .output(temp_video_path, vcodec='libx264', crf=22)  # Re-encoding might be necessary
                .run(overwrite_output=True)
            )
            self.video_path = temp_video_path
            self.video_history.append(self.video_path)
        except ffmpeg.Error as e:
            print(f"Failed to change video speed: {e.stderr.decode('utf-8')}")

    #Fade content in or out
    def fade_in_video(self, duration=2):
        """
        Applies a fade-in effect to the video over the specified duration in seconds.
        """
        temp_video_path = tempfile.mktemp(suffix='.mp4')
        
        try:
            (
                ffmpeg
                .input(self.video_path)
                .filter('fade', t='in', d=duration)
                .output(temp_video_path, vcodec='libx264', crf=22)
                .run(overwrite_output=True)
            )
            self.video_path = temp_video_path
            self.video_history.append(self.video_path)
        except ffmpeg.Error as e:
            print(f"Failed to apply fade in effect: {e.stderr.decode('utf-8')}")
    #Fade out video
    def fade_out_video(self, duration=2):
        """
        Applies a fade-out effect to the video over the specified duration in seconds.
        """
        temp_video_path = tempfile.mktemp(suffix='.mp4')
        probe = ffmpeg.probe(self.video_path)
        total_duration = float(probe['format']['duration'])
        fade_start = total_duration - duration
        
        try:
            (
                ffmpeg
                .input(self.video_path)
                .filter('fade', t='out', start_time=fade_start, d=duration)
                .output(temp_video_path, vcodec='libx264', crf=22)
                .run(overwrite_output=True)
            )
            self.video_path = temp_video_path
            self.video_history.append(self.video_path)
        except ffmpeg.Error as e:
            print(f"Failed to apply fade out effect: {e.stderr.decode('utf-8')}")
            
    def play_video(self):
        cap = cv2.VideoCapture(self.video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        while self.running:
            ret, frame = cap.read()
            if not ret:
                # Reload the video to start from the beginning after finishing or trimming
                cap.release()
                cap = cv2.VideoCapture(self.video_path)
                continue
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(rgb_frame.data, rgb_frame.shape[1], rgb_frame.shape[0], QImage.Format_RGB888)
            p = image.scaled(640, 480, Qt.KeepAspectRatio)
            self.update_signal.emit(p)
            QThread.msleep(int(1000 / fps))
        cap.release()  # Ensure the capture is released if self.running becomes False

    def start_playback(self):
        self.running = True
        if not self.isRunning():
            self.start()

    def pause_playback(self):
        self.running = False
        self.wait()  # Wait for the thread to pause
        
    #Undo stack    
    def undo_last_action(self):
        if len(self.video_history) > 1:
            self.video_history.pop()  # Remove the latest action
            self.video_path = self.video_history[-1]  # Revert to the previous state
            # Trigger UI update, may need adjustment
            print("Last action undone.")
        else:
            print("No actions to undo.")

class App(QWidget):
    #Create Multiple Video Processors and run it based on LLM
    def __init__(self):
        super().__init__()
        self.setWindowTitle('LLM Guided Video Editor')
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.videoLabel = QLabel('Video Display Here')
        self.uploadButton = QPushButton('Upload Video')  # Upload button
        self.input = QLineEdit()
        self.input.setPlaceholderText('Enter command (e.g., "trim the video by 1 second on each side", "undo")')
        self.input.returnPressed.connect(self.process_command)
        self.uploadButton.clicked.connect(self.upload_video)  # Connect the button click to upload_video method

        self.layout.addWidget(self.uploadButton)
        self.layout.addWidget(self.videoLabel)
        self.layout.addWidget(self.input)

        self.setLayout(self.layout)

        self.video_processor = VideoProcessor("./stock.mp4")  # Adjust this path
        self.video_processor.update_signal.connect(self.update_image)
        self.video_processor.finished.connect(self.on_finished_trim)
        # self.video_processor.start_playback()  # Start playback only after a video is uploaded

    def upload_video(self):
        videoPath, _ = QFileDialog.getOpenFileName(self, "Select Video", "", "Video Files (*.mp4 *.avi *.mov)")
        if videoPath:
            self.video_processor.pause_playback()  # Ensure any existing video processing is stopped
            self.video_processor = VideoProcessor(videoPath)  # Create a new VideoProcessor instance with the new video
            self.video_processor.update_signal.connect(self.update_image)
            self.video_processor.finished.connect(self.on_finished_trim)
            self.video_processor.start_playback()
        
    def update_image(self, image):
        self.videoLabel.setPixmap(QPixmap.fromImage(image).scaled(self.videoLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def process_command(self):
        #Zoom out can be undoing
        command = self.input.text().lower()
        if command == "undo":
            self.video_processor.pause_playback()
            self.video_processor.undo_last_action()
            self.video_processor.start_playback()
        elif command == "fade in":
            self.video_processor.pause_playback()
            self.video_processor.fade_in_video(2)  # Apply a 2-second fade-in effect
            self.video_processor.start_playback()
        elif command == "fade out":
            self.video_processor.pause_playback()
            self.video_processor.fade_out_video(2)  # Apply a 2-second fade-out effect
            self.video_processor.start_playback()
        elif command == "zoom in":
            self.video_processor.pause_playback()
            self.video_processor.zoom_video(0.9)  # Example scale for zooming in
            self.video_processor.start_playback()
        elif "speed up" in command:
            try:
                temp = command.split()
                factor = float(temp[-1])
                self.video_processor.pause_playback()
                self.video_processor.change_speed(factor)  # Example: "speed up 2" to double the speed
                self.video_processor.start_playback()
            except ValueError:
                QMessageBox.warning(self, "Error", "Invalid speed factor. Please try again.")
        elif "slow down" in command:
            try:
                temp = command.split()
                factor = float(temp[-1])
                self.video_processor.pause_playback()
                self.video_processor.change_speed(1/factor)  # Example: "slow down 2" to halve the speed
                self.video_processor.start_playback()
            except ValueError:
                QMessageBox.warning(self, "Error", "Invalid speed factor. Please try again.")
            
        elif command.startswith("trim the video by") and command.endswith("seconds on each side"):
            parts = command.split()
            seconds = int(parts[4])
            self.video_processor.pause_playback()
            self.video_processor.start_sec = seconds
            self.video_processor.end_sec = seconds
            self.video_processor.trim_required = True
            self.video_processor.start_playback()
        elif command == "crop to mobile dimensions":
            self.video_processor.pause_playback()
            self.video_processor.crop_video(9/16)
            self.video_processor.start_playback()
        else:
            QMessageBox.warning(self, "Error", "Invalid command format. Please try again.")

    def on_finished_trim(self):
        # This slot will be called when trimming is finished.
        # You can implement additional logic here if needed.
        print('Trimmed')
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())





