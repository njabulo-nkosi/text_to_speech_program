from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
import pymupdf
import requests
import builtins
import os
import re
from pyht import Client
from dotenv import load_dotenv

load_dotenv()

USER_ID = os.getenv('PLAY_HT_USER_ID')
SECRET_KEY = os.getenv('PLAY_HT_SECRET_KEY')


class PdfToAudio:

    def __init__(self, window):
        self.window = window
        self.window.title('PDF To Audio')
        self.window.config(pady=50, padx=50, bg='black')

        self.setup_window()
        self.setup_image()
        self.setup_labels()
        self.setup_buttons()

    def setup_window(self):
        title = Label(self.window, text='PDF To Audio Tool\n Text to Audio',
                      font=('Courier', 30, 'bold'), pady=20, padx=20,
                      bg='black',
                      fg='white')
        title.grid(column=1, row=0)

    def setup_image(self):
        image = Image.open('Audiobook-amico.png')

        max_size = 600
        image.thumbnail((max_size, max_size - 200), Image.Resampling.LANCZOS)

        self.display_image = ImageTk.PhotoImage(image)

        image_label = Label(self.window, image=self.display_image, bg='black')
        image_label.grid(column=1, row=1, pady=20)

    def setup_labels(self):
        pass

    def setup_buttons(self):
        self.start_button = Button(self.window, text='Upload PDF',
                                   font=('Courier', 10, 'bold'), pady=10,
                                   command=self.upload_and_process_pdf)
        self.start_button.grid(column=1, row=4)

    def upload_and_process_pdf(self):
        file_path = self.get_local_file()
        if file_path:
            extracted_text = self.extract_text(file_path)
            if extracted_text:
                self.text_to_audio(extracted_text)

    def get_local_file(self):
        file_path = filedialog.askopenfilename(defaultextension='.pdf', filetypes=[('pdf files', '*.pdf')])

        if file_path:
            print(f'File path: {file_path}')

            return file_path

    def extract_text(self, file_path):

        doc = pymupdf.open(file_path)
        print(f"Opening file: {file_path}")

        completed_text = ""
        for page in doc:
            completed_text += page.get_text()

        cleaned_text = self.clean_text(completed_text)

        return cleaned_text

    def clean_text(self, text):
        text = text.strip()

        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\x20-\x7E]+', '', text)
        text = re.sub(r'\n+', ' ', text)

        return text

    def text_to_audio(self, text):
        play_ht_endpoint = 'https://api.play.ht/api/v2/tts/stream'

        client = Client(user_id=USER_ID,
                        api_key=SECRET_KEY
                        )

        payload = {
            "voice": "s3://voice-cloning-zero-shot/d9ff78ba-d016-47f6-b0ef-dd630f59414e/female-cs/manifest.json",
            "output_format": "mp3",
            "text": text,
            "voice_engine": "PlayHT2.0"
        }

        headers = {
            "accept": "audio/mpeg",
            "content-type": "application/json",
            "AUTHORIZATION": SECRET_KEY,
            "X-USER-ID": USER_ID
        }

        response = requests.post(url=play_ht_endpoint, json=payload, headers=headers)

        audio_path = "dialogue_2.mp3"
        with builtins.open(audio_path, 'wb') as audio_file:
            audio_file.write(response.content)
            print(f'Audio saved.')




