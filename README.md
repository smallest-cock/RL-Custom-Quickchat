# RL-Custom-Quickchat

Enables custom quick chats (and more) in Rocket League using button macros

## Video Overview

https://youtu.be/G0Lperc-UU0

[![custom quick chats](https://i.imgur.com/U83sQM9.png)](https://youtu.be/G0Lperc-UU0)

## Features

- Custom quick chats
- Custom ball textures in online matches
  - [Video tutorial](https://youtu.be/qjvJxKlpNx0)
- Speech-to-text chats
  - [Video demo](https://youtu.be/cqEdJQ-X7X4)
- KBM version
- Create button combination macros (e.g. Circle + Up) or button sequence macros (e.g. Left → Up)
- Choose how many times to spam a chat
  - Customize spam interval (in seconds)
- Specify chat mode (lobby/team/party)
- Add word variations to spice up your chats
  - "thx [friend]" ........... where [friend] is a random word from a list containing "homie", "bro", "blud", "my guy", "foo" etc.
  - Easily customize the word lists
- Toggle all macros on/off with one press of a button

## How to install (for beginners):

### Installation video guide:

https://www.youtube.com/watch?v=Epbn-Oste64

[![installation tutorial](https://i.imgur.com/b9ZTJFl_d.webp?maxwidth=760&fidelity=grand)](https://www.youtube.com/watch?v=Epbn-Oste64)

1. Download & install [python](https://www.python.org/getit/). Make sure to check "Add Python 3.x to PATH" and click "Install Now"
2. Open a Windows cmd (command prompt) and type:
   ```
   pip install pyautogui pygame pyaudio SpeechRecognition opencv-python setuptools
   ```
   This will install the required python packages for the script.
   - To open a command prompt: press the windows button → type "cmd" → hit enter
   - If on KBM, use this command instead:
     ```
     pip install pyautogui keyboard pyaudio SpeechRecognition opencv-python setuptools
     ```
3. [Download the code](https://github.com/smallest-cock/RL-Custom-Quickchat/archive/refs/heads/main.zip), extract the zip file, & put the `example.py` file somewhere (the one that applies to you)
   - If you want to rename the .py file, do it before step 4
   - Put all the .png images (for the autoclicker) in the same folder as your .py file if you want to use the feature which enables custom ball texures in matches
4. Right-click the .py file → Create shortcut
5. Right-click the shortcut → Properties → Target: → add the word "python" to the beginning, so it looks like: `python "C:\Users\....."`. Click Apply.
   - You can also change Run: → Minimized to have it start minimized
6. Leave the script running any time you want to use custom quick chats or custom ball textures in matches :)
   - Edit the .py file to change quick chats, macros, etc.

## Troubleshooting / Errors:

### Macros not being detected

If the script isn't detecting your button presses properly, you may need to edit the `buttons` dictionary in your script:

![buttonslist](https://github.com/smallest-cock/RL-Custom-Quickchat/assets/48503773/9ccc127d-c148-463a-8992-cbc14e33e19a)

In order to find out which values to use for each button, run `button_value_tester.py` and press each button you want to test. It will give you the correct values.

### Autoclicker isn't working correctly

#### If you get this error: `PyAutoGUI was unable to import pyscreeze ...`

- Run this command: `pip install -U Pillow` to update the Pillow module to the latest version

#### Other errors:

The autoclicker (and supplied .png images) were made based on a 1080p screen. If your screen resolution is higher than 1080p then the bakkesmod UI may look different or be positioned differently than what's depicted in the images, which can prevent the autoclicker from finding a match. You can try any of these fixes:

- Take your own screenshots and replace the supplied .png images
  - Make sure to crop them similarly and give them the same name
- Delete the `region=( ... )` parameter inside the `clickThing` function for whatever button isn't being found

  ![gif_demo](https://github.com/smallest-cock/RL-Custom-Quickchat/assets/48503773/ba8bf2a7-edb1-472f-8275-5d610b75f3e4)

  - This will make the autoclicker search the entire screen (rather than a specific region), which is slower but should give better chances at finding the button

- If you want a better (more performant) fix, you can edit the `region=( ... )` parameter yourself, to search a specific region where you know the button will be on your screen.
  - The structure is `region=(topLeftX, topLeftY, width, height)` where each value would be a number (in pixels)
  - A smaller region generally means a faster search, but make sure the region is large enough to contain the whole .png image

## Support

[Drop a tip 🙏](https://cash.app/$naptime559) <3
