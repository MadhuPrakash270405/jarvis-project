import os
import random
from pydub import AudioSegment
import speech_recognition as sr
import pyttsx3
from pydub.silence import split_on_silence


def get_all_voices(engine):
    voices = engine.getProperty("voices")
    for voice in voices:
        print(f"Trying voice: {voice.name} - {voice.id}")


def text_to_voice(text):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    selected_voice = random.choice(voices)
    print(selected_voice)
    engine.setProperty("voice", selected_voice.id)
    # Adjusting the rate and volume
    engine.setProperty("rate", 185)  # Adjust the speed as needed
    engine.setProperty("volume", 1)  # Adjust the volume level (0.0 to 1.0)
    engine.say(text)
    engine.runAndWait()


def voice_to_text():
    recognizer = sr.Recognizer()
    """recording the sound"""
    with sr.Microphone() as source:
        print("Adjusting noise ")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Recording for 4 seconds")
        recorded_audio = recognizer.listen(source, timeout=4)
        print("Done recording")
    """ Recorgnizing the Audio """
    try:
        print("Recognizing the text")
        text = recognizer.recognize_google(recorded_audio, language="en-US")
        print("Decoded Text : {}".format(text))
        return {"transcription": text}
    except sr.UnknownValueError:
        return {"error": "Could not understand audio", "transcription": ""}
    except sr.RequestError or Exception as e:
        return {
            "error": "Could not request results; {0}".format(e),
            "transcription": "",
        }


def load_chunks(filename):
    long_audio = AudioSegment.from_mp3(filename)
    audio_chunks = split_on_silence(
        long_audio, min_silence_len=1800, silence_thresh=-17
    )
    return audio_chunks


def get_audio_lyrics(audio_file):
    recognizer = sr.Recognizer()
    for audio_chunk in load_chunks(audio_file):
        audio_chunk.export("temp", format="wav")
        with sr.AudioFile("temp") as source:
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio)
                print("Chunk : {}".format(text))
            except Exception as ex:
                print("Error occured")
                print(ex)
    print("++++++")


if __name__ == "__main__":
    text_to_voice("Hello, how are you doing today?")
    # voice_to_text()
    # get_audio_lyrics("audio.mp3")