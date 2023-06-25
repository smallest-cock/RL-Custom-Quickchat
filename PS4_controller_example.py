import time
import pyautogui
import pygame
from random import randint

# Change/add/remove these as you wish (or dont use this list at all.... see examples below) Make sure any changes are reflected in the "edit" section below
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

# Create your own word variations and format them like this (see examples on how to use them in the "edit" section below)
variations = {
    'friend': ['homie', 'blood', 'cuh', 'dawg', 'my guy', 'my man', 'nibba', 'my dude', 'comrade', 'playa', 'fellow gamer', 'brother', 'bro', 'bruh', 'buddy', 'bud', 'fellow human'],
    'foe': ['clown', 'nerd', 'loser', 'bozo', 'small peen', 'tard', 'cringelord', 'idiot', 'bitch', 'autist', 'dork', 'mouth breather', 'dumbass', 'virgin', 'fruitcake', 'weirdo', 'NPC'],
    'compliment': ['noice', 'awesome', 'dank', 'fire', 'impressive', 'crispy', 'beautiful', 'sexy', 'clean', 'excellent', 'superb', 'lovely', 'delightful', 'splendid', 'bussin', 'bust-worthy'],
    'cat fact': ['Cats are believed to be the only mammals who don\'t taste sweetness.',   # <-- always put a backslash ( " \ " ) before any apostrophe (to avoid the program crashing)
                  'Cats can jump up to six times their length.',
                  'Cats have 230 bones, while humans only have 206.',
                  "Cats' rough tongues can lick a bone clean of any shred of meat.",    # <-- or just wrap the chat in double quotes ( "..." ) if it contains an apostrophe
                  'Cats live longer when they stay indoors.',
                  'Meowing is a behavior that cats developed exclusively to communicate with people.'],
    'taste': ['sweet', 'sour', 'bitter', 'salty', 'rich', 'spicy', 'savory']
}

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

lastUsedVariations = {}
macrosOn = True

def resetFirstButtonPressed():
    firstButtonPressed['button'] = None     
    firstButtonPressed['time'] = 420

# detects simultaneous button presses
def combine(button1, button2):
    if joysticks[0].get_button(buttons[button1]) and joysticks[0].get_button(buttons[button2]):
        resetFirstButtonPressed()
        return True
    else: return False

# detects successive button presses (buttons pressed in a specific order)
def sequence(button1, button2):
    global firstButtonPressed
    functionCallTime = time.time()

    if firstButtonPressed['button'] == None:
        if joysticks[0].get_button(buttons[button1]):
            firstButtonPressed['time'] = functionCallTime
            firstButtonPressed['button'] = button1
            return False
        else: return False
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
                    else: return False
                else: return False   
            else: return False

def quickchat(thing, chatMode='lobby', spamCount=1):
    for i in range(spamCount):
        pyautogui.press(chatKeys[chatMode])
        pyautogui.write(thing, interval=0.001)  # <-- the "interval" parameter is required if your chat is longer than one line... you can remove this if your chat isnt long, to make it type out instantly
        pyautogui.press('enter')
        print(f'[{chatMode}]    {thing}\n')
        time.sleep(chatSpamInterval)

def toggleMacros(button):
    if joysticks[0].get_button(buttons[button]):
        global macrosOn
        macrosOn = not macrosOn
        if macrosOn:
            print('----- quickchat macros toggled on -----\n')
        else:
            print('----- quickchat macros toggled off -----\n')
        time.sleep(.2)

def resetLastUsedVariations(key=''):
    if not (key == ''):
        lastUsedVariations[key] = []
    else:
        for key in lastUsedVariations:
            lastUsedVariations[key] = []

def variation(key):
    global variations
    global lastUsedVariations
    if len(variations[key]) > 1:
        while True:
            randomVariation = variations[key][randint(0, (len(variations[key]) - 1))]
            if not (randomVariation in lastUsedVariations[key]):
                if len(lastUsedVariations[key]) < (len(variations[key]) - 1):
                    lastUsedVariations[key].append(randomVariation)
                    return randomVariation
                else:
                    resetLastUsedVariations(key)
                    lastUsedVariations[key].append(randomVariation)
                    return randomVariation                    
    else:
        print(f'The "{key}" variation list has less than 2 items..... it cannot be used properly!! Please add more items (words/phrases)')
        return '-- "' + key + '" variation list needs more items --'

lastUsedVariations = variations.copy()
resetLastUsedVariations()

pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

for controller in joysticks:
    if controller.get_init() == True:
        print(f"\n\n~~~~~~ {controller.get_name()} detected ~~~~~~\n\nwaiting for quickchat inputs....\n\n")

while True:
    try:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:

                
# --------------------------- Edit the code below to change macros, spam amounts, chat modes, or if you made changes to the length/order of the quickchats list above -----------------------

                
                toggleMacros('ps') # <-- 'ps' is the button used to toggle on/off quick chat macros (PlayStation button)..... change as you please

                if macrosOn:

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
                    
                    # on circle + down, types "You dont need to use the quickchats list"
                    elif combine('circle', 'down'):
                        quickchat('You dont need to use the quickchats list')   # <-- You can write your quick chat here if preferred (as opposed to using the quickchats list above)
                        break
                    
                    # on circle + down, types 8th chat in quickchats list  ...... you get the pattern
                    elif combine('circle', 'right'):
                        quickchat(quickchats[7])
                        break
                    
                    # on left -> left, types "Word variations are [compliment]!"  ..... where [compliment] is a random word from the 'compliment' variations list above
                    elif sequence('left', 'left'):
                        quickchat(f'Word variations are {variation("compliment")}!')    # <-- One way to include word variations in your chats (notice the 'f' at the beginning of the string)
                        break

                    # on up -> up, types 10th chat in quickchats list (using team chat, spamming 2 times)
                    elif sequence('up', 'up'):
                        quickchat(quickchats[9], chatMode='team', spamCount=2)
                        break
                    
                    # on up -> right, types 11th chat in quickchats list (using party chat)
                    elif sequence('up', 'right'):
                        quickchat(quickchats[10], chatMode='party')
                        break

                    # on down -> left, types "ok [foe]!!!"  ..... where [foe] is a random word from the 'foe' variations list above
                    elif sequence('down', 'left'):
                        quickchat('ok ' + variation('foe') + '!!!')    # <-- Another way to format word variations in your chats
                        break
                    
                    # on L1 + right, types "Wassup [friend]! Nice to see you again."
                    elif combine('L1', 'right'):
                        quickchat('Wassup %s! Nice to see you again.' % variation('friend'))    # <-- Yet another way to format word variations in your chats
                        break
                    
                    # on down -> up, types a random cat fact (from the 'cat fact' variations list above)
                    elif sequence('down', 'up'):
                        quickchat(variation('cat fact'))
                        break

    except Exception as e:
        print(e)
        break
