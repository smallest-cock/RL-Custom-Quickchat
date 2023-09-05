# RL-Custom-Quickchat
Enables custom quick chats in Rocket League (or any game with chat) using button macros

## Video Tutorial
[![custom quick chats](https://i.imgur.com/U83sQM9.png)](https://youtu.be/G0Lperc-UU0)

## Features
- Custom quick chats
- Speech-to-text chats
- Create button combination macros (e.g. Circle + Up) or button sequence macros (e.g. Left -> Up) for controller
- Choose how many times to spam a chat
  - Customize spam interval (in seconds)
- Specify chat mode (lobby/team/party)
- Add word variations to spice up your chats
  - e.g. "thx [friend]"  ............  where [friend] can be "homie", "bro", "dude", "playa", "my guy", etc.
- Toggle all macros on/off with one press of a button

## How to install (for beginners):
1. Download & install [python](https://www.python.org/getit/). Make sure to check "Add Python 3.x to PATH" and click "Install Now"
2. Open a Windows cmd (command prompt) and type `pip install pyautogui pygame pyaudio SpeechRecognition`. This will install the required python packages for the script.
   - If on KBM, use this command instead: `pip install pyautogui keyboard pyaudio SpeechRecognition`
   - To open a command prompt: press the windows button -> type "cmd" -> hit enter
3. [Download the code](https://github.com/smallest-cock/RL-Custom-Quickchat/archive/refs/heads/main.zip), extract the zip file, & put the `example.py` file somewhere (the one that applies to you)
   - If you want to rename the .py file, do it before step 4
4. Right-click the .py file -> Create shortcut
5. Right-click the shortcut -> Properties -> Target: -> add the word "python" to the beginning, so it looks like: `python "C:\Users\....."`. Click Apply.
    - You can also change Run: -> Minimized to have it start minimized
6. Leave the script running any time you want to use custom quick chats :)
   - Edit the .py file to change quick chats, macros, etc.

### Support
[Buy me a coffee ☕](https://cash.app/$naptime559) <3
