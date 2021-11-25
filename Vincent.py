import pyttsx3, re, urllib.request, os, moviepy.editor
from PyDictionary import PyDictionary
from pytube import YouTube
import speech_recognition as sr
from pygame import mixer
mixer.init()
dictionary = PyDictionary()
ears = sr.Recognizer()
mouth = pyttsx3.init()
mouth.setProperty("rate", 130)
mic = sr.Microphone()
while True:
    try:
        with mic as source:
            ears.adjust_for_ambient_noise(source)
            audio = ears.listen(source)
        speech = ears.recognize_google(audio).split()
        print(speech)
        if speech[0] == "Vincent":
            if " ".join(speech[1:]) == "introduce yourself":
                mouth.say("Hi, my name is Vincent. I am a general assistance AI.")
                mouth.runAndWait()
            elif speech[1] == "play":
                title = " ".join(speech[2:])
                mouth.say("OK, playing " + title)
                mouth.runAndWait()
                if title + ".mp3" not in os.listdir("music"):
                    YouTube("https://www.youtube.com/watch?v=" + re.findall(r"watch\?v=(\S{11})", urllib.request.urlopen("https://www.youtube.com/results?search_query=" + "+".join(speech[2:])).read().decode())[0]).streams.get_by_itag(18).download(filename = title + ".mp4")
                    moviepy.editor.VideoFileClip(title + ".mp4").audio.write_audiofile(f"music/{title}.mp3")
                    os.remove(title + ".mp4")
                mixer.music.load(f"music/{title}.mp3")
                mixer.music.play()
            elif speech[1] == "pause":
                mixer.music.pause()
            elif speech[1] == "resume":
                mixer.music.unpause()
            elif speech[1] == "stop":
                mixer.music.stop()
            elif speech[1] == "define":
                mouth.say(f"The definition of {speech[2]} is the following." + str(dictionary.meaning(speech[2])))
                mouth.runAndWait()
            elif speech[1] == "quit":
                mouth.say("Quitting, goodbye for now.")
                mouth.runAndWait()
                mixer.quit()
                break
    except sr.UnknownValueError:
        print("No clear audio detected.")
    except:
        print("An error occurred.")
