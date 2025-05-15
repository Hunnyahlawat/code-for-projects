import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import moviepy.editor as mp
import speech_recognition as sr
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import os
from pydub import AudioSegment

# Initialize translator and recognizer
translator = Translator()
recognizer = sr.Recognizer()

# Function to transcribe audio in segments
def transcribe_audio_in_segments(audio_path):
    transcription = ""
    audio = AudioSegment.from_file(audio_path)
    segment_length = 30000  # Transcribe in 30-second chunks
    for i in range(0, len(audio), segment_length):
        segment = audio[i:i+segment_length]
        segment_path = "temp_segment.wav"
        segment.export(segment_path, format="wav")
        with sr.AudioFile(segment_path) as source:
            audio_data = recognizer.record(source)
            try:
                transcription += recognizer.recognize_google(audio_data) + " "
            except sr.UnknownValueError:
                transcription += "[Unintelligible Segment] "
            except sr.RequestError as e:
                transcription += f"[Request Error: {str(e)}] "
    return transcription

# Function to handle video input
def handle_video_input():
    video_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video Files", "*.mp4;*.avi;*.mov")])
    if video_path:
        video = mp.VideoFileClip(video_path)
        audio_path = "extracted_audio.wav"
        video.audio.write_audiofile(audio_path)
        
        # Transcribe audio from video
        transcription = transcribe_audio_in_segments(audio_path)
        
        # Translate the transcription
        handle_translation_and_voice_output(transcription)

# Function to handle audio input
def handle_audio_input():
    audio_path = filedialog.askopenfilename(title="Select Audio File", filetypes=[("Audio Files", "*.wav;*.mp3;*.ogg")])
    if audio_path:
        # Transcribe audio
        transcription = transcribe_audio_in_segments(audio_path)
        
        # Translate the transcription
        handle_translation_and_voice_output(transcription)

# Function to handle text file input
def handle_text_file_input():
    text_file_path = filedialog.askopenfilename(title="Select Text File", filetypes=[("Text Files", "*.txt")])
    if text_file_path:
        with open(text_file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        
        # Translate the text
        handle_translation_and_voice_output(text)
async def fetch_data():
 response = client.get(url)
 data = response.text
 return data

# Function to handle translation and voice output
def handle_translation_and_voice_output(text):
    # Create a new window for language selection
    lang_window = tk.Toplevel(root)
    lang_window.title("Select Language")
    
    # Dropdown menu for language selection
    tk.Label(lang_window, text="Choose the target language:").pack(pady=5)
    lang_code = tk.StringVar()
    lang_dropdown = ttk.Combobox(lang_window, textvariable=lang_code, values=list(LANGUAGES.values()))
    lang_dropdown.pack(pady=5)
    
    def translate_and_save():
        selected_language = lang_code.get()
        target_lang_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(selected_language)]
        
        translated_text = translator.translate(text, dest=target_lang_code).text
        print("Translated Text:", translated_text)
        
        # Generate AI voice audio from translated text
        audio_output_path = "translated_audio.mp3"
        tts = gTTS(text=translated_text, lang=target_lang_code)
        tts.save(audio_output_path)
        
        # Save the audio to the desktop
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "translated_audio.mp3")
        os.rename(audio_output_path, desktop_path)
        
        # Success message
        messagebox.showinfo("Success", f"The translated audio has been saved as 'translated_audio.mp3' on the desktop!")
        lang_window.destroy()

    # Button to confirm language selection
    tk.Button(lang_window, text="Translate and Save", command=translate_and_save).pack(pady=10)

# Main application setup
root = tk.Tk()
root.title("Audio, Video, and Text Translation App")
root.geometry("300x300")

# Interface buttons
video_button = tk.Button(root, text="Upload Video", command=handle_video_input)
video_button.pack(pady=10)

audio_button = tk.Button(root, text="Upload Audio", command=handle_audio_input)
audio_button.pack(pady=10)

text_file_button = tk.Button(root, text="Upload Text File", command=handle_text_file_input)
text_file_button.pack(pady=10)

# Run the application
root.mainloop()
