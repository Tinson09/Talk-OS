# Talk-OS
An AI personal assistant like JARVIS, with which users can communicate with their Ubuntu systems in informal language. With an Articial Neural Network working at the center. This system understands what you want from the informal language that you use to talk to the system. And does exactly what you ask it to do.
This system is also integrated with an AI chatbot, with which you can converse.

## Requirements:
- OS: Linux (Ubuntu or Mint)
- Python2.7
- xdotool

```
Python Libraries :-
 - tensorflow==0.12.0
 - Pyttsx
 - speech_recognition
 - Numpy
 - webbrowser
 - time
```

## Installation:
### Training
To train Jarvis model:-
- Go to execute.py and make Perform_Train = True
```
Run python execute.py
```

To train chatbot model:-
- Go to execute.py and make Perform_Train = False
```
Run python execute.py
```

### Deployment
```
Run ./main.sh
```
* ** . Today's date? **
* ** . What day is today? **
* ** . What time is it? **
* ** . Open firefox **
* ** . Go to [Folder name] **
* ** . Go back **
* ** . Google [Something] **
* ** . Select file or folder **
* ** . Press [Key] **
* ** . Close [Application] **
* ** . Copy [File or Folder] **
* ** . Paste **
* ** . Delete [Folder or File] **
* ** . Let's Chat **

