from subprocess import Popen
import shlex
import os
import webbrowser
import time
from datetime import datetime, date
from texttospeech import say, Inform
from inputManager import confirmation

DELAY = 0.25
LONG_DELAY = 6

class Execution:
    def __init__(self, string):
        self.dictionary = {"move":self.move, "copy":self.copy, 
                            "cfile":self.createFile, "cfolder":self.createFolder, 
                            "delete":self.deleteFun, "press":self.press, 
                            "shutdown":self.shutdown, "restart":self.restart, 
                            "folder":self.openFolder, "file":self.openFile, 
                            "open": self.openApp, "close":self.closeApp, 
                            "switch":self.switchWindow, "close":self.closeWindow, 
                            "sleep":self.sleepPC, "date":self.dateInform, 
                            "chatbot":self.chatbot, "type":self.Type, "select":self.select,
                            "search":self.search, "google":self.google}

        self.command = ""
        self.string = string
        self.string = self.string.rstrip(' , \x00')
        self.string = self.string.replace(' , \0 ','')
        print self.string
        
        # Tokenizing the given instruction string.
        instruction = self.string.split()[0]
        tokens = self.string.split(',')
        tokens[0] = tokens[0].replace(instruction, '', 1)
        tokens[0] = tokens[0][1:]
        tokens = [x for x in tokens if (x != '\0' and x != ',' and x != '\x00' and x != '\\0')]
        # Remove ',' from the list of tokens for instructions with 2 operands. 
        tokens = [instruction] + tokens
        tokens = [x.strip() for x in tokens]
        print "Tokens :-"
        if '\\0' in tokens:
            tokens.remove('\\0')
        tokens = filter(None, tokens)
        print tokens
        if instruction in self.dictionary:
            self.dictionary[instruction](tokens)
        self.processid = -1

    def execute(self):
        if self.command == "Nothing":
            return 1
        elif self.command == "Chatbot":
            return 2
        else:
            commands = self.command.split('\n')
            print commands
            for command in commands:
                """
                arg = shlex.split(self.command)
                p = Popen(arg)
                self.processid = p.pid
                """
                os.system(command)
                self.processid = 0
            say("Done.")
            return 0
    
    def getcommand(self):
        return self.command

    def chatbot(self, tokens):
        self.command = "Chatbot"
    
    def getprocessid(self):
        return self.processid
    
    def search(self, tokens):
        self.command = """xdotool key ctrl+f
xdotool type {}
xdotool key Return
""".format(tokens[1])
    
    def google(self, tokens):
        topic = tokens[1]
        topic = topic.split()
        search = ""
        for i in topic:
            search = search + "+" + i
        url = "http://www.google.com/search?q={}".format(search)
        browser = webbrowser.get('firefox')
        browser.open_new(url)
    
    def switchWindow(self, tokens):
        self.command = "sleep {}; xdotool keydown Alt_L; xdotool key Tab; sleep {}; xdotool keyup Alt_L".format(DELAY, DELAY)

    def closeWindow(self, tokens):
        self.command = "xdotool key alt+F4"

    def sleepPC(self, tokens):
        self.command = "Nothing"

    def move(self, tokens):
        if "\\0" in tokens:
            tokens.remove("\\0")
        if len(tokens) == 1:
            self.command = "xdotool key Control_L+x"
        elif len(tokens) == 2:
            self.command = """sleep {}
xdotool key ctrl+BackSpace
sleep {}
xdotool type {}
sleep {}
xdotool key Control_L+x""".format(DELAY, DELAY, tokens[1], LONG_DELAY)
            say("Copied")
        else:
            self.command = "mv -a " + tokens[1] + " " + tokens[2]

    def copy(self, tokens):
        if "\\0" in tokens:
            tokens.remove("\\0")
        if len(tokens) == 1:
            self.command = "xdotool key Control_L+c"
        elif len(tokens) == 2:
            self.command = """sleep {}
xdotool key ctrl+BackSpace
sleep {}
xdotool type {}
sleep {}
xdotool key Control_L+c""".format(DELAY, DELAY, tokens[1], LONG_DELAY)
            say("Copied")
        else:
            self.command = "cp -a " + tokens[1] + " " + tokens[2]
    
    def paste(self, tokens):
        self.command = "xdotool key Control_L+v"
    
    def select(self, tokens):
        self.Type(tokens)

    def createFile(self, tokens):
        say("Doesn't support this operation right now.")

    def createFolder(self, tokens):
        if len(tokens) == 2:
            say("Creating folder {}".format(tokens[1]))
            self.command = """sleep {}
xdotool key Control_L+Shift_L+n
sleep {}
xdotool type {}
xdotool key Return""".format(DELAY, DELAY, tokens[1])

        if len(tokens) > 2:
            if os.path.isdir(tokens[2]):
                destination = tokens[2]
                if destination[-1] != '/':
                    destination = destination + '/'
                destination = destination + tokens[1]
                self.command = "mkdir " + destination
            
            else:
                pass
                Inform(" Location " + tokens[2] + " does not exists.")

    def deleteFun(self, tokens):
        if os.path.isdir(tokens[1]) or os.path.isfile(tokens[1]):
            self.command = "rm -rf " + tokens[1]
        
        elif len(tokens) > 1:
            self.command = """sleep {}
xdotool key ctrl+BackSpace
sleep {}
xdotool type {}
sleep {}
xdotool key Delete""".format(DELAY, DELAY, tokens[1], LONG_DELAY)

        else:
            self.command = "xdotool key Delete"
   
    def pressutil(self, key):

        dictionary = {"control":"Control_L", "shift":"Shift_L", "alt":"alt", 
                      "backspace":"BackSpace", "super":"Super_L", "tab":"Tab", 
                      "enter":"Return", "return":"Return", "delete":"Delete",
                      "escape":"Escape", "home":"Home", "end":"End", "left":"Left", 
                      "right":"Right", "up":"Up", "down":"Down"}
        
        punctuations = {",":"comma", "!":"exclam", '"':"quotedbl","#":"numbersign", 
                        "$":"dollar", "%":"percent", "&":"ampersand", "'":"quoteright",
                        "(": "parenleft", ")":"parenright", "[":"bracketleft", "]":"bracketright",
                        "*":"asterisk", "\\":"backslash","+":"plus", "^": "asciicircum", 
                        "_":"underscore",".":"period", "/":"slash",":":"colon",";":"semicolon", "<":"less",
                        ">":"greater", "=":"equal", "~":"asciitilde", "-":"minus"}
        
        Functional_keys = {}

        for i in range(1, 13):
            k = "f" + str(i)
            item = "F" + str(i)
            Functional_keys[k] = item
        
        dictionary.update(punctuations)
        dictionary.update(Functional_keys)
        key = key.lower()
        key = key.replace(' plus ', ' + ')
        keys = key.split('+')
        keys = [x.strip() for x in keys]
        if keys[-1] == '':
            keys[-1] = '+'
            keys.remove('')
        print keys
        if len(keys) > 1:
            output = ""        
            for i in keys:
                if not i in dictionary:
                    output = output + i + "+"
                else:
                    output = output + dictionary[i] + "+"

            output = output[:-1]
            return output
        else:
            if len(key) == '1':
                if key == '':
                    return '+'
                return key
            
            else:
                if key in dictionary:
                    return dictionary[key]
                else:
                    return key

    def press(self, tokens):
        self.command = "xdotool key " + self.pressutil(str(tokens[1]))
    
    def Type(self, tokens):
        self.command = "sleep {}; xdotool type ".format(DELAY) + tokens[1]

    def shutdown(self, tokens):
        if confirmation("Do you want me to shutdown system?"):
            self.command = "shutdown now"

    def restart(self, tokens):
        if confirmation("Do you want me to restart system?"):
            self.command = "shutdown -r now"

    def openFolder(self, tokens):
        if tokens[1] == "back":
            self.command = "xdotool key alt+Left"
        else:
            self.command = """xdotool key ctrl+BackSpace
sleep {}
xdotool type {}
sleep {}
xdotool key Return""".format(DELAY, tokens[1], DELAY)
    
    def openFile(self, tokens):
        self.command = """xdotool key ctrl+BackSpace
sleep {}
xdotool type {}
sleep {}
xdotool key Return""".format(DELAY, tokens[1], DELAY)

    def openApp(self, tokens):
        say("Opening " + tokens[1])
        self.command = """xdotool key Super_L
sleep {}
xdotool type {}
sleep {}
xdotool key Return""".format(DELAY, tokens[1], DELAY)

    def closeApp(self, tokens):
        self.command = "sleep {}; xdotool key alt+f4".format(DELAY)
    
    def dateInform(self, tokens):

        months = ["January", "February", "March", "April", "May", "June", 
                  "July", "August", "September", "October", "November", "December"]
        if len(tokens) == 2:
            if tokens[1] == "time":
                say("Time is "+ str(time.strftime("%I:%M %p")))

            elif tokens[1] == "date":
                today = str(date.today())
                features = today.split('-')
                features = features[::-1]
                if features[0][0] == '0':
                    features[0] = features[0][1]
                speech = "Today is " + str(features[0]) + "th " + months[int(features[1])-1] + " " + features[2]
                say(speech)
        
        else:
            week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            today = datetime.today().weekday()
            today = week[int(today)]
            speech = "Today is " + today
            say(speech)

if __name__ == '__main__':
    a = Execution('close sound')
    print a.getcommand()
    b = a.execute()