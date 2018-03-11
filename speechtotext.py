import speech_recognition as sr
from texttospeech import say

#mic_name = "USB Device 0x46d:0x825: Audio (hw:1, 0)"
#crw-rw----+ 1 root video 81, 0 Dec  7 22:29 /dev/video0
def getallmicrophones():
    mic_list = sr.Microphone.list_microphone_names()
    print mic_list

def voiceconverter(file):
    r = sr.Recognizer()
    with sr.AudioFile(file) as source:
        audio = r.record(source)
    
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return (False, "")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service: {}".format(e))
        return (False, "stop")

def gettext():
    r = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)
            print("Finished recording")
            say("Okay.")

        try:
            text = r.recognize_google(audio)
            print("You said : " + text)
            return text

        except sr.UnknownValueError:
            say("Hey")

        except sr.RequestError as e:
            say("Hey")

if __name__ == '__main__':
    print(gettext())
    getallmicrophones()
