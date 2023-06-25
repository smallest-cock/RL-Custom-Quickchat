import time
import pyautogui
import pygame
from random import randint

# Change/add/remove these as you wish (or dont use this list at all.... see examples below) Make sure any changes are reflected in the "edit" section below
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

# Time window given to read button sequence macros (1.1 seconds).... you can change this as you please
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

lastUsedVariations = {}
macrosOn = True

def resetFirstButtonPressed():
    firstButtonPressed['button'] = None     
    firstButtonPressed['time'] = 420

# Should detect simultaneous button/hat presses
def combine(button1, button2):
    if ((joysticks[0].get_button(buttons[button1]) or (joysticks[0].get_hat(0) == buttons[button1]))
        and (joysticks[0].get_button(buttons[button2]) or (joysticks[0].get_hat(0) == buttons[button2]))):
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
    if (joysticks[0].get_button(buttons[button]) or (joysticks[0].get_hat(0) == buttons[button])):
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
            if (event.type == pygame.JOYBUTTONDOWN) or (event.type == pygame.JOYHATMOTION):


# --------------------------- Edit the code below to change macros, spam amounts, chat modes, or if you made changes to the length/order of the quickchats list above -----------------------


                toggleMacros('back') # <-- 'back' is the button used to toggle on/off quick chat macros (Xbox back button)..... change as you please

                if macrosOn:

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

                    # on B + down, types "You dont need to use the quickchats list"
                    elif combine('b', 'down'):
                        quickchat('You dont need to use the quickchats list')   # <-- You can write your quick chat here if preferred (as opposed to using the quickchats list above)
                        break
                    
                    # on B + down, types 8th chat in quickchats list  ...... you get the pattern
                    elif combine('b', 'right'):
                        quickchat(quickchats[7])
                        break

                    # on left -> left, types "Word variations are [compliment]!"  ..... where [compliment] is a random word from the 'compliment' variations list above
                    elif sequence('left', 'left'):
                        quickchat(f'Word variations are {variation("compliment")}!')    # <-- One way to include word variations in your chats (notice the 'f' at the beginning of the string)
                        break
                    
                    # on up -> right, types 10th chat in quickchats list (using party chat, spamming 2 times)
                    elif sequence('up', 'right'):
                        quickchat(quickchats[9], chatMode='party', spamCount=2)
                    
                    # on up -> up, types 11th chat in quickchats list (using team chat)
                    elif sequence('up', 'up'):
                        quickchat(quickchats[10], chatMode='team')
                        break

                    # on down -> left, types "ok [foe]!!!"  ..... where [foe] is a random word from the 'foe' variations list above
                    elif sequence('down', 'left'):
                        quickchat('ok ' + variation('foe') + '!!!')    # <-- Another way to format word variations in your chats
                        break

                    # on RB + right, types "Wassup [friend]! Nice to see you again."
                    elif combine('rb', 'right'):
                        quickchat('Wassup %s! Nice to see you again.' % variation('friend'))    # <-- Yet another way to format word variations in your chats
                        break

                    # on down -> up, types a random cat fact (from the 'cat fact' variations list above)
                    elif sequence('down', 'up'):
                        quickchat(variation('cat fact'))
                        break
                    
    except Exception as e:
        print(e)
        break
