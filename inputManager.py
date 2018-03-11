import sys
from nltk import sent_tokenize
from speechtotext import gettext
from texttospeech import say

VOICE = False

cliche_choices = {"what is your name":"My name is Eva", "your name":"My name is Eva", "What is your name?":"My name is Eva."}

def cliche(string):
    if string in cliche_choices:
        return cliche_choices[string]
    else:
        return "0"

def commonelements(a, b):
    c = list(set(a).intersection(b))
    if c:
        return True
    return False

def text_input():
    sys.stdout.write("> ")
    sys.stdout.flush()
    sentence = sys.stdin.readline()
    return sentence

def voice_input():
    return gettext()

def confirmation(text):
    say(text)
    if VOICE:
        answer = voice_input()
    else:
        answer = text_input()
    answer = answer.lower()

    affirmative = ["yes", "ya", "aye", "yeah"]
    negative = ["no", "nope", "don't"]
    
    if (commonelements(affirmative, answer.split())) and (not commonelements(negative, answer.split())):
        return True
    elif (commonelements(negative, answer.split())) and (not commonelements(affirmative, answer.split())):
        return False
    else:
        return confirmation()

def read_input(signal = False):
    punctuations = [',','?',"'", '"','!','@','#','$','%','^','&','*','-','|','=','`']
    flag = True
    sentence = ""
    wake = ["wake", "awake"]
    while flag:
        if VOICE:
            sentence = voice_input()
        else:
            sentence = text_input()
        chat_sentence = sentence

        sentences = sent_tokenize(sentence)
        split_sentence = []
        for i in sentences:
            phrases = i.split('and')
            split_sentence = split_sentence + phrases
        
        split_sentence = [i.strip() for i in split_sentence]

        """
        Formatting of input
        """
        sentences = []

        for sentence in split_sentence:
            sentence = sentence.lower()
            for i in punctuations:
                sentence = sentence.replace(i, "")
            sentence = sentence.replace("  ", " ")
            sentence = sentence.replace("please", "")
            sentence = sentence.strip('.')
            sentence = sentence.strip()
            if commonelements(wake, sentence.split()) or (not signal):
                flag = False
            else:
                flag = True

            if sentence in cliche_choices:
                flag = True
                say(cliche(sentence))
            sentences.append(sentence)
    print sentences
    return (sentences, chat_sentence)
