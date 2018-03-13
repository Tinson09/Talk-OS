# Talk-OS
An AI personal assistant like JARVIS, with which users can communicate with their Ubuntu systems in informal language. With an Articial Neural Network working at the center. 
This system understands what you want from the informal language that you use to talk to the system. And does exactly what you ask it to do.
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
#### Examples :-
* **Today's date?**
```
 Bot: "Today is 25th Sepetember 2010"
 ```
* **What day is today?**
```
Bot: "Today is Tuesday"
```
* **What time is it?**
```
Bot: "Time is 3:30 PM"
```
* **Open [Application name]**
```
Bot :- Launch the application that user asks.
```
* **Go to [Folder name]**
```
Bot :- Go to the folder which is in the given opened File browser session
```
* **Go back**
```
Bot :- Goes back to the previous directory
```
* **Google [Something]**
```
Bot :- Googles what you asks
```
* **Select file or folder**
```
Bot :- Select the file or folder in the given file browser session
```
* **Press [Key]**
```
Bot :- Press the specified key
```
* **Close [Application]**
```
Bot :- Close the application
```
* **Copy [File or Folder]**
```
Bot :- Copy the file or folder to clipboard
```
* **Paste**
```
Bot :- Executes paste operation
```
* **Delete [Folder or File]**
```
Bot :- Delete the specified folder or file
```
* **Switch window**
```
Bot :- Switch to next window (Alt+Tab action)
```
* **Create folder [Folder name]**
```
Bot :- Creates a folder at the specified position
```
* **Type [Something]**
```
Bot :- Types what user asks to type
```
* **Let's Chat**
```
Bot :- System goes to AI chatbot mode with which the user can converse
```
