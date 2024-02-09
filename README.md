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
- Expose people's ranks in chat *\*\**
- Parrot people's chats (with optional added effects, such as sArCAsM tExT or "as a quote" - something) *\*\**
- KBM version
- Create button combination macros (Circle + Up) or button sequence macros (Left → Down)
  - Button combo macros will work with any amount of buttons (e.g. L1 + Up + Square + R1)
- Choose how many times to spam a chat
  - Customize spam interval (in seconds)
- Specify chat mode (lobby/team/party)
- Add word variations to spice up your chats
  - "thx [friend]" .... where [friend] is a random word like "homie", "blud", "bro", "my guy", etc.
  - Easily customize with word lists
- Toggle all macros on/off with one press of a button
   
<br>

*\*\** Requires the [Lobby Info bakkesmod plugin](https://github.com/smallest-cock/LobbyInfo/releases/tag/latest) 

## How to install:

### Installation video guide:

https://youtu.be/qdeey4lyZo0

[![installation tutorial](https://i.imgur.com/Cg4CHke.png)](https://youtu.be/qdeey4lyZo0)

1. Download & install [python](https://www.python.org/getit/). Make sure to check "**Add python.exe to PATH**" and click "**Install Now**"

2. [Download the code](https://github.com/smallest-cock/RL-Custom-Quickchat/archive/refs/heads/main.zip), extract the zip file, and run `install.bat`
   - This will install the python packages used by the script, and create an installation folder called `Quickchats Script` on your desktop
   - If you encounter any errors, try running as Administrator 
   - If you want to rename the example .py file, do it before step 3

3. Store the `Quickchats Script` folder wherever you want on your PC → Open it → Right-click the example script → Create shortcut

4. Right-click the shortcut → Properties → Target: → add the word `python` to the beginning, with a space, so it looks like: `python "C:\Users\....."`. Click Apply.
   - Even better, you can add `cmd /k python` instead of just `python` to have the terminal window stay open, even if the script exits/crashes
     - This will allow you to easily read any error messages related to a crash
   - You can also change Run: → Minimized to have it start minimized

5. Leave the script running any time you want to use it :)
   - Edit the example script to customize quick chats, macros, etc.

## Troubleshooting / Errors:

### Autoclicker not working correctly

#### If you have multiple displays:

- Make sure RL is running on the **primary** monitor

- PyAutoGUI (the autoclicker) only works on the primary monitor. So make sure your "main display" is set correctly in Windows display settings (or just make sure to play RL on the main display)

#### If your screen resolution is higher than 1080p:

The supplied .png images were made using screenshots of a 1080p screen. If your screen resolution is above 1080p the bakkesmod UI may look different or be positioned differently than what's depicted in the images, which can prevent the autoclicker from finding a match. You can try any of these fixes:

- Take your own screenshots and replace the supplied .png images
  - Make sure to crop them similarly and give them the same name

- In `functions.py` find `def getRegion(...):` → `match "whateverImageIsntBeingFound":` → `return ...` and edit or delete the search region (the 4 values in parentheses)
  - Editing the region will make it search a different part of the screen; deleting the region will make it search the *entire* screen
  - To delete the region: change the whole line to `return None`
  - To edit the region: the structure is `(topLeftX, topLeftY, width, height)` where each value is a number (in pixels)
    - Also update `checkWithinScreenBounds(topLeftY, height)` on the same line
    - Make sure the new region is large enough to contain the whole .png image
  
#### If "fast mode" fails

This usually happens when you change the position or size of the AlphaConsole settings window (causing previous mouse click positions to no longer be valid). If you didn't touch the AlphaConsole settings window and you still see this message, you can just disable "fast mode" altogether to avoid issues:

- At the top of your script, change the value of `enableAutoclickerFastMode` to `False`
- Alternatively, you can create a macro which triggers the function `toggleFastMode()`. This will give you the ability to toggle fast mode at any time without having to edit/restart your script

#### If you get this error: `PyAutoGUI was unable to import pyscreeze ...`

- Run this command: `pip install -U Pillow` to update the Pillow module to the latest version

### Macros not being detected

If the script isn't detecting your button presses properly, you may need to edit the `buttons` dictionary:

<img src="https://github.com/smallest-cock/RL-Custom-Quickchat/assets/48503773/9ccc127d-c148-463a-8992-cbc14e33e19a" alt="drawing" width="500"/>

In order to find the right values, run `controller_button_tester.py` and press each button you want to test. It will give you the correct values.

## Support

[Drop a tip <3](https://cash.app/$naptime559)