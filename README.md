# RL-Custom-Quickchat

Enables custom quick chats (and more) in Rocket League using button macros

## Video Overview

https://youtu.be/G0Lperc-UU0

<a href='https://youtu.be/G0Lperc-UU0'>
  <img src='https://i.imgur.com/U83sQM9.png' alt="overview" width="500"/>
</a>

## Features

- Custom quick chats
- Custom ball textures in online matches
  - [Video tutorial](https://youtu.be/qjvJxKlpNx0)
- Speech-to-text chats
  - [Video demo](https://youtu.be/cqEdJQ-X7X4)
- KBM version
- Create button combination macros (Circle + Up) or button sequence macros (Left → Down)
  - Can use any amount of buttons in button combination macros (e.g. L1 + Up + Square)
- Choose how many times to spam a chat
  - Customize spam interval (in seconds)
- Specify chat mode (lobby/team/party)
- Add word variations to spice up your chats
  - "thx [friend]" ........... where [friend] is a random word from a list containing "homie", "bro", "blud", "my guy", "foo" etc.
  - Easily customize the word lists
- Toggle all macros on/off with one press of a button

## How to install (for beginners):

### Installation video guide:

https://youtu.be/Epbn-Oste64

[![installation tutorial](https://i.imgur.com/b9ZTJFl_d.webp?maxwidth=760&fidelity=grand)](https://youtu.be/Epbn-Oste64)

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

### Autoclicker isn't working correctly

#### If you have multiple displays:

- Make sure RL is running on the **primary** monitor

- PyAutoGUI (the autoclicker) only works on the primary monitor. So make sure your "main display" is set correctly in Windows display settings (or just make sure to play RL on the main display)

#### If your screen resolution is higher than 1080p:

The supplied .png images were made using screenshots of a 1080p screen. If your screen resolution is above 1080p the bakkesmod UI may look different or be positioned differently than what's depicted in the images, which can prevent the autoclicker from finding a match. You can try any of these fixes:

- Take your own screenshots and replace the supplied .png images
  - Make sure to crop them similarly and give them the same name
- Delete the `region=( ... )` argument in the `clickThing` function for whatever image isn't being found

  ![gif_demo](https://github.com/smallest-cock/RL-Custom-Quickchat/assets/48503773/ba8bf2a7-edb1-472f-8275-5d610b75f3e4)

  - This will make the autoclicker search the entire screen (rather than a specific region), which is slower but should give better chances at finding the image

- If you want a better (more performant) fix you can edit the `region=( ... )` argument yourself, to search a specific region on your screen where you know the image will be.
  - The structure is `region=(topLeftX, topLeftY, width, height)` where each value is a number (in pixels)
  - A smaller region generally means a faster search, but make sure the region is large enough to contain the whole .png image

#### If you get this error: `PyAutoGUI was unable to import pyscreeze ...`

- Run this command: `pip install -U Pillow` to update the Pillow module to the latest version

### Macros not being detected

If the script isn't detecting your button presses properly, you may need to edit the `buttons` dictionary:

<img src="https://github.com/smallest-cock/RL-Custom-Quickchat/assets/48503773/9ccc127d-c148-463a-8992-cbc14e33e19a" alt="drawing" width="500"/>

In order to find the right values, run `button_value_tester.py` and press each button you want to test. It will give you the correct values.

## Support

[Drop a tip <3](https://cash.app/$naptime559)