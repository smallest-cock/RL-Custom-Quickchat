import time
import pyautogui
import pygame

# Change/add/remove these as you wish... but make sure any changes are reflected in the edit section below
quickchats = [
    'noice',
    'dont lose this kickoff',
    'that was totally a fake',
    'thx brother',
    'im gay',
    'tell me how you really feel...',
    'let me cook',
    'What a tryhard!',
    'okay buddy',
    'im lagging',
    'mitochondria is the powerhouse of the cell',
    'brb uninstalling...'
]

# Time window given for button sequence macros (1.1 seconds).... you can change this as you please
macroTimeWindow = 1.1

# Time interval between spammed chats (0.2 seconds).... change as you please
chatSpamInterval = .2

# Edit these if necessary
chatKeys = {
    'lobby': 't',
    'team': 'y',
    'party': 'u'
}

# PS4 controller button mappings for pygame.... these may change if using a different controller (refer to https://www.pygame.org/docs/ref/joystick.html)
buttons = {
    'x': 0,
    'circle': 1,
    'square': 2,
    'triangle': 3,
    'share': 4, 
    'ps': 5,
    'options': 6,
    'L1': 9,
    'R1': 10,
    'up': 11, 
    'down': 12, 
    'left': 13, 
    'right': 14
}

firstButtonPressed = {
    'button': None,
    'time': 420
}

def resetFirstButtonPressed():
    firstButtonPressed['button'] = None     
    firstButtonPressed['time'] = 420

pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

# detects simultaneous button presses
def combine(button1, button2):
    if joysticks[0].get_button(buttons[button1]) and joysticks[0].get_button(buttons[button2]):
        resetFirstButtonPressed()
        return True
    else:
        return False

# detects successive button presses (buttons pressed in a specific order)
def successive(button1, button2):
    global firstButtonPressed
    functionCallTime = time.time()

    if firstButtonPressed['button'] == None:
        if joysticks[0].get_button(buttons[button1]):
            firstButtonPressed['time'] = functionCallTime
            firstButtonPressed['button'] = button1
            return False
        else:
            return False
    else:
        if functionCallTime > (firstButtonPressed['time'] + macroTimeWindow):
            if joysticks[0].get_button(buttons[button1]):
                firstButtonPressed['time'] = functionCallTime
                firstButtonPressed['button'] = button1
                return False
            else:
                resetFirstButtonPressed()
                return False
        else:
            if joysticks[0].get_button(buttons[button2]):
                if button1 == firstButtonPressed['button']:
                    if (functionCallTime > (firstButtonPressed['time'] + 0.05)):
                        resetFirstButtonPressed()
                        return True
                else:
                    return False   
            else: 
                return False

def quickchat(thing, chatMode='lobby', spamCount=1):
    for i in range(spamCount):
        pyautogui.press(chatKeys[chatMode])
        pyautogui.write(thing, interval=0.001)  # <-- the "interval" parameter is required if your chat is longer than one line... you can remove this if your chat isnt long, to make it type out instantly
        pyautogui.press('enter')
        print(f'[{chatMode}]    {thing}\n')
        time.sleep(chatSpamInterval)

for controller in joysticks:
    if controller.get_init() == True:
        print(f"\n\n~~~~~~ {controller.get_name()} detected ~~~~~~\n\nwaiting for quickchat inputs....\n\n")

while True:
    try:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:

# ------------ Edit the code below to change macros, spam amounts, or if you made changes to the length/order of the quickchats list above -----------------------

                # on square + up, types 1st chat in quickchats list
                if combine('square', 'up'):
                    quickchat(quickchats[0])
                    break
                
                # on square + left, types 2nd chat in quickchats list (spamming 2 times)
                elif combine('square', 'left'):
                    quickchat(quickchats[1], spamCount=2)  # <-- the '2' parameter is how many times the chat will be spammed.. the max you can put is 3 (before RL gives a chat timeout)
                    break

                # on square + down, types 3rd chat in quickchats list
                elif combine('square', 'down'):
                    quickchat(quickchats[2])
                    break
                
                # on square + right, types 4th chat in quickchats list
                elif combine('square', 'right'):
                    quickchat(quickchats[3])
                    break
                
                # on circle + up, types 5th chat in quickchats list (using team chat)
                elif combine('circle', 'up'):
                    quickchat(quickchats[4], chatMode='team')
                    break
                
                # on circle + left, types 6th chat in quickchats list
                elif combine('circle', 'left'):
                    quickchat(quickchats[5])
                    break
                
                # on circle + down, types 7th chat in quickchats list
                elif combine('circle', 'down'):
                    quickchat(quickchats[6])
                    break
                
                # on circle + down, types 8th chat in quickchats list  ...... you get the pattern
                elif combine('circle', 'right'):
                    quickchat(quickchats[7])
                    break
                
                # on left -> left, types 9th chat in quickchats list
                elif successive('left', 'left'):
                    quickchat(quickchats[8])
                    break

                # on up -> up, types 10th chat in quickchats list (using team chat, spamming 2 times)
                elif successive('up', 'up'):
                    quickchat(quickchats[9], chatMode='team', spamCount=2)
                    break
                
                # on up -> right, types 11th chat in quickchats list (using party chat)
                elif successive('up', 'right'):
                    quickchat(quickchats[10], chatMode='party')
                    break

                # on down -> left, types 12th chat in quickchats list
                elif successive('down', 'left'):
                    quickchat(quickchats[11])
                    break

    except Exception as e:
        print(e)
        break
