## Autoclicker not working correctly

>[!IMPORTANT]
>See [Autoclicker Usage](./Autoclicker.md) for info about how the autoclicker works (and how to customize it)


### If you have multiple displays:

- Make sure RL is running on the **primary** monitor

- PyAutoGUI (the autoclicker) only works on the primary monitor. So make sure your "main display" is set correctly in Windows display settings (or just make sure to play RL on the main display)

### If your screen resolution is higher than 1080p:

The supplied .png images were made using screenshots of a 1080p screen. If your screen resolution is above 1080p the bakkesmod UI may look different or be positioned differently than what's depicted in the images, which can prevent the autoclicker from finding a match. You can try any of these fixes:

- Take your own screenshots and replace the supplied .png images
  - Make sure to crop them similarly and give them the same name

- In `functions.py` find `class Autoclicker` → `def getRelativeSearchRegion(...):` → `match "whateverImageIsntBeingFound":` → `region = (...)` and edit or delete the search region (defined by the 4 values in parentheses)
  - Editing the region will make it search a different part of the screen; deleting the region will make it search the *entire* screen
  - **To delete the region:** change the whole `return region if ...` line to `return None`
  - **To edit the region:** the structure is `(topLeftX, topLeftY, width, height)` where each value is a number (in pixels)
    - Make sure the new search region is large enough to contain the whole .png image
  
### If "fast mode" fails

This usually happens when you change the position or size of the AlphaConsole settings window (causing previous mouse click positions to no longer be valid). If you didn't touch the AlphaConsole settings window and you still see this message, you can just disable "fast mode" altogether to avoid issues:

- At the top of your script, change the value of `enableAutoclickerFastMode` to `False`
- Alternatively, you can create a macro which triggers the function `toggleFastMode()`. This will give you the ability to toggle fast mode at any time without having to edit/restart your script

### If you get this error: 

`PyAutoGUI was unable to import pyscreeze ...`

- Run this command: `pip install -U Pillow` to update the Pillow module to the latest version

## Macros not being detected

If the script isn't detecting your button presses properly, you may need to edit the `buttons` dictionary:

<img src="https://github.com/smallest-cock/RL-Custom-Quickchat/assets/48503773/9ccc127d-c148-463a-8992-cbc14e33e19a" alt="drawing" width="500"/>

In order to find the right values, run `controller_button_tester.py` and press each button you want to test. It will give you the correct values.