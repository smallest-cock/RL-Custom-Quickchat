## Macros not being detected

If the script isn't detecting your button presses properly, you may need to edit the `buttons` dictionary:

<img src="https://github.com/smallest-cock/RL-Custom-Quickchat/assets/48503773/9ccc127d-c148-463a-8992-cbc14e33e19a" alt="drawing" width="500"/>

In order to find the right values, run `controller_button_tester.py` and press each button you want to test. It will give you the correct values.

## Chats are triggered randomly

Make sure to delete any unused/unwanted macros in your example script

Also make sure you're not creating macros that will get triggered during your normal gameplay/mechanics (i.e. creating quickchat macros for the same buttons you use to air dribble)