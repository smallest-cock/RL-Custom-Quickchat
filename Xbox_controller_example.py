import time
import pyautogui
import pygame

# Change/add/remove these as you wish... but make sure any changes are reflected in the edit section below
quickchats = [
    'noice',
    'dont lose this kickoff',
    'interesting bounce',
    'thx daddy',
    'im gay',
    'tell me how you really feel...',
    'let me cook',
    'ur mom',
    'mitochondria is the powerhouse of the cell',
    'hacker',
    'im lagging',
    'it be like that'
]

# Time window given to read successive button presses (1.1 seconds).... you can change this as you please
macroTimeWindow = 1.1

# Time interval between spammed chats (0.2 seconds).... change as you please
chatSpamInterval = .2

# Edit these if necessary
chatKeys = {
    'lobby': 't',
    'team': 'y',
    'party': 'u'
}

# Xbox controller button mappings for pygame.... these may wrong because I dont own an Xbox controller :(     (refer to https://www.pygame.org/docs/ref/joystick.html)
buttons = {
    'a': 0,
    'b': 1,
    'x': 2,
    'y': 3,
    'LB': 4,
    'RB': 5,
    'back': 6, 
    'start': 7,
    'up': (0, 1), 
    'down': (0, -1), 
    'left': (-1, 0), 
    'right': (1, 0) 
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

# Should detect simultaneous button/hat presses
def combine(button1, button2):
    if ((joysticks[0].get_button(buttons[button1]) or (joysticks[0].get_hat(0) == buttons[button1]))
        and (joysticks[0].get_button(buttons[button2]) or (joysticks[0].get_hat(0) == buttons[button2]))):
        resetFirstButtonPressed()
        return True
    else:
        return False

# Should detect successive button/hat presses (buttons pressed in a specific order)
def successive(button1, button2):
    global firstButtonPressed
    functionCallTime = time.time()

    if firstButtonPressed['button'] == None:
        if (joysticks[0].get_button(buttons[button1]) or (joysticks[0].get_hat(0) == buttons[button1])):
            firstButtonPressed['time'] = functionCallTime
            firstButtonPressed['button'] = button1
            return False
        else:
            return False
    else:
        if functionCallTime > (firstButtonPressed['time'] + macroTimeWindow):
            if (joysticks[0].get_button(buttons[button1]) or (joysticks[0].get_hat(0) == buttons[button1])):
                firstButtonPressed['time'] = functionCallTime
                firstButtonPressed['button'] = button1
                return False
            else:
                resetFirstButtonPressed()
                return False
        else:
            if (joysticks[0].get_button(buttons[button2]) or (joysticks[0].get_hat(0) == buttons[button2])):
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
            if (event.type == pygame.JOYBUTTONDOWN) or (event.type == pygame.JOYHATMOTION):

# ---------- Edit the code below to change macros, spam amounts, or if you made changes to the length/order of the quickchats list above -----------------------

                # on X + up, types 1st chat in quickchats list
                if combine('x', 'up'):
                    quickchat(quickchats[0])
                    break
                
                # on X + left, types 2nd chat in quickchats list (spamming 2 times)
                elif combine('x', 'left'):
                    quickchat(quickchats[1], spamCount=2)  # <-- the '2' parameter is how many times the chat will be spammed.. the max you can put is 3 (before RL gives a chat timeout)
                    break

                # on X + down, types 3rd chat in quickchats list
                elif combine('x', 'down'):
                    quickchat(quickchats[2])
                    break
                               
                # on X + right, types 4th chat in quickchats list
                elif combine('x', 'right'):
                    quickchat(quickchats[3])
                    break
                
                # on B + up, types 5th chat in quickchats list (using team chat)
                elif combine('b', 'up'):
                    quickchat(quickchats[4], chatMode='team')
                    break
                
                # on B + left, types 6th chat in quickchats list
                elif combine('b', 'left'):
                    quickchat(quickchats[5])
                    break

                # on B + down, types 7th chat in quickchats list
                elif combine('b', 'down'):
                    quickchat(quickchats[6])
                    break
                
                # on B + down, types 8th chat in quickchats list  ...... you get the pattern
                elif combine('b', 'right'):
                    quickchat(quickchats[7])
                    break

                # on up -> up, types 9th chat in quickchats list
                elif successive('up', 'up'):
                    quickchat(quickchats[8])
                    break
                
                # on up -> right, types 10th chat in quickchats list (using party chat, spamming 2 times)
                elif successive('up', 'right'):
                    quickchat(quickchats[9], chatMode='party', spamCount=2)
                
                # on up -> up, types 11th chat in quickchats list
                elif successive('up', 'up'):
                    quickchat(quickchats[10], chatMode='team')
                    break

                # on down -> left, types 12th chat in quickchats list
                elif successive('down', 'left'):
                    quickchat(quickchats[11])
                    break
                    
    except Exception as e:
        print(e)
        break