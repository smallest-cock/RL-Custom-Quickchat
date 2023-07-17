import time
import pyautogui
import pygame
from random import sample



# -----------------------    Warning: this Xbox version of the script is entirely experimental and may not work properly... I don't yet have an Xbox controller to test on :(    ----------------------



# -------------------------------------------    Go to the "edit" section below to edit quickchats, macros, etc.    -----------------------------------------------------------



# Create your own word variations and format them like this (see examples on how to use them in the "edit" section below)
variations = {
    'friend': ['homie', 'blood', 'cuh', 'dawg', 'my guy', 'my man', 'nibba', 'my dude', 'comrade', 'playa', 'fellow gamer', 'brother', 'bro', 'bruh', 'buddy', 'blud', 'fellow human', 'foo', 'lad', 'broski', 'mate'],
    'foe': ['clown', 'nerd', 'loser', 'bozo', 'small-peen', 'tard', 'cringelord', 'idiot', 'bitch', 'crayon eater', 'dork', 'mouth breather', 'dumbass', 'virgin', 'fruitcake', 'weirdo', 'NPC', 'dipshit'],
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

# Xbox 360 controller button mappings for pygame.... these may be incorrect because I dont own an Xbox controller  (refer to https://www.pygame.org/docs/ref/joystick.html)
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

macrosOn = True
buttonPressed = None
buttonPressedIsHat = None

# Triggers on simultaneous button/hat presses
def combine(button1, button2):
    if type(buttonPressed) is list:
        button1Value = buttons[button1]
        button2Value = buttons[button2]
        if (button1Value in buttonPressed) and (button2Value in buttonPressed):
            return True
        else: return False
    else: return False

# Triggers on successive button/hat presses (buttons pressed in a specific order)
def sequence(button1, button2):
    if not type(buttonPressed) is list:
        global firstButtonPressed
        functionCallTime = time.time()
        for i in range(numJoysticks):
            if firstButtonPressed['button'] == None:
                if buttonPressed == buttons[button1]:
                    firstButtonPressed['time'] = functionCallTime
                    firstButtonPressed['button'] = button1
                    return False
                else: return False
            else:
                if functionCallTime > (firstButtonPressed['time'] + macroTimeWindow):
                    if buttonPressed == buttons[button1]:
                        firstButtonPressed['time'] = functionCallTime
                        firstButtonPressed['button'] = button1
                        return False
                    else:
                        resetFirstButtonPressed()
                        return False
                else:
                    if buttonPressed == buttons[button2]:
                        if button1 == firstButtonPressed['button']:
                            if (functionCallTime > (firstButtonPressed['time'] + 0.05)):
                                resetFirstButtonPressed()
                                return True
                            else: return False
                        else: return False   
                    else: return False
    else: return False

# Reads button presses
def detectButtonPressed():
    for i in range(numJoysticks):
        for key in buttons:
            buttonVal = buttons[key]
            if controllerHasHats:
                if buttonPressedIsHat:
                    if type(buttonVal) is tuple:
                        if joysticks[i].get_hat(0) == buttonVal:
                            for otherKey in buttons:
                                if not (otherKey == key):
                                    otherButtonVal = buttons[otherKey]
                                    if type(otherButtonVal) is tuple:
                                        if joysticks[i].get_hat(0) == otherButtonVal:
                                            return [buttonVal, otherButtonVal]
                                    else:
                                        if joysticks[i].get_button(otherButtonVal):
                                            return [buttonVal, otherButtonVal]
                            return buttonVal
                        else: continue
                    else: continue
                else:
                    if type(buttonVal) is int:
                        if joysticks[i].get_button(buttonVal):
                            for otherKey in buttons:
                                if not (otherKey == key):
                                    otherButtonVal = buttons[otherKey]
                                    if type(otherButtonVal) is tuple:
                                        if joysticks[i].get_hat(0) == otherButtonVal:
                                            return [buttonVal, otherButtonVal]
                                    else:
                                        if joysticks[i].get_button(otherButtonVal):
                                            return [buttonVal, otherButtonVal]
                            return buttonVal
                        else: continue
                    else: continue
            else:
                if not type(buttonVal) is tuple:
                    if joysticks[i].get_button(buttonVal):
                        for otherKey in buttons:
                            if not (otherKey == key):
                                otherButtonVal = buttons[otherKey]
                                if not type(otherButtonVal) is tuple:
                                    if joysticks[i].get_button(otherButtonVal):
                                        return [buttonVal, otherButtonVal]                                    
                        return buttonVal
    return None 

def resetFirstButtonPressed():
    firstButtonPressed['button'] = None     
    firstButtonPressed['time'] = 420

def checkIfPressedButtonIsHat(event):
    if event.type == pygame.JOYBUTTONDOWN:
        return False
    elif event.type == pygame.JOYHATMOTION:
        return True

def quickchat(thing, chatMode='lobby', spamCount=1):
    for i in range(spamCount):
        pyautogui.press(chatKeys[chatMode])
        pyautogui.write(thing, interval=0.001)  # <-- the "interval" parameter is required if your chat is longer than one line... you can remove this if your chat isnt long, to make it type out instantly
        pyautogui.press('enter')
        print(f'[{chatMode}]    {thing}\n')
        time.sleep(chatSpamInterval)

def toggleMacros(button):
    global macrosOn
    if not type(buttonPressed) is list:
        buttonValue = buttons[button]
        if buttonValue == buttonPressed:
            macrosOn = not macrosOn
            if macrosOn:
                print('----- quickchat macros toggled on -----\n')
            else:
                print('----- quickchat macros toggled off -----\n')
            time.sleep(.2)

def shuffleVariations(key=''):
    if not (key == ''):
         lastWordUsed = shuffledVariations[key]['randomizedList'][len(variations[key]) - 1]
         secondLastWordUsed = shuffledVariations[key]['randomizedList'][len(variations[key]) - 2]
         while True:
            shuffledList = sample(variations[key], len(variations[key]))
            if not (shuffledList[0] == lastWordUsed) and (shuffledList[1] == secondLastWordUsed):
                shuffledVariations[key]['randomizedList'] = shuffledList
                shuffledVariations[key]['nextUsableIndex'] = 0
                break
    else:
        for key in variations:
            shuffledVariations[key] = {
                'randomizedList': sample(variations[key], len(variations[key])),
                'nextUsableIndex': 0
            }

def variation(key):
    global variations
    global shuffledVariations
    index = shuffledVariations[key]['nextUsableIndex']
    if not len(variations[key]) > 2:
        print(f'The "{key}" variation list has less than 3 items..... it cannot be used properly!! Please add more items (words/phrases)')
        return '-- "' + key + '" variation list needs more items --'
    else:
        if index < (len(variations[key])):
            randWord = shuffledVariations[key]['randomizedList'][index]
            shuffledVariations[key]['nextUsableIndex'] += 1
            return randWord
        else:
            shuffleVariations(key)
            randWord = shuffledVariations[key]['randomizedList'][0]
            shuffledVariations[key]['nextUsableIndex'] += 1
            return randWord

shuffledVariations = variations.copy()
shuffleVariations()
pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
controllerHasHats = False

for controller in joysticks:
    if controller.get_numhats() > 0:
        controllerHasHats = True
    if controller.get_init() == True:
        print(f"\n\n~~~~~~ {controller.get_name()} detected ~~~~~~\n\nwaiting for quickchat inputs....\n\n")

while True:
    try:
        for event in pygame.event.get():
            if (event.type == pygame.JOYBUTTONDOWN) or (event.type == pygame.JOYHATMOTION):
                buttonPressedIsHat = checkIfPressedButtonIsHat(event)
                numJoysticks = pygame.joystick.get_count()
                buttonPressed = detectButtonPressed()



# ---------------------------------    Edit the code below to change quickchats, macros, spam amounts, chat modes, variations, etc.    --------------------------------------------------



                toggleMacros('y') # <-- 'y' is the button used to toggle on/off quick chat macros (Xbox Y button)..... change as you please

                if macrosOn:
                    
                    # on X + A, types "let me cook"
                    if combine('x', 'a'):
                        quickchat('let me cook')
                        break
                
                    # on X + left, types "dont lose this kickoff" (spamming 2 times)
                    elif combine('x', 'left'):
                        quickchat('dont lose this kickoff', spamCount=2)  # <-- the '2' parameter is how many times the chat will be spammed.. the max you can put is 3 (before RL gives a chat timeout)
                        break
                    
                    # on B + X, types "tell me how you really feel..." (using team chat)
                    elif combine('b', 'x'):
                        quickchat('tell me how you really feel...', chatMode='team')
                        break
                    
                    # on A -> A, types "im lagging" (using team chat, spamming 3 times)
                    elif sequence('a', 'a'):
                        quickchat('im lagging', chatMode='team', spamCount=3)
                        break
                    
                    # on up -> left, types "im gay" (using party chat)
                    elif sequence('up', 'left'):
                        quickchat('im gay', chatMode='party')
                        break

                    # on left -> left, types "Word variations are [compliment]!"  ..... where [compliment] is a random word from the 'compliment' variations list above
                    elif sequence('left', 'left'):
                        quickchat(f'Word variations are {variation("compliment")}!')    # <-- One way to include word variations in your chats (notice the 'f' at the beginning of the string)
                        break

                    # on down -> left, types "ok [foe]!!!"  ..... where [foe] is a random word from the 'foe' variations list above
                    elif sequence('down', 'left'):
                        quickchat('ok ' + variation('foe') + '!!!')    # <-- Another way to format word variations in your chats
                        break
                    
                    # on LB + right, types "Wassup [friend]! Nice to see you again."
                    elif combine('LB', 'right'):
                        quickchat('Wassup %s! Nice to see you again.' % variation('friend'))    # <-- Yet another way to format word variations in your chats
                        break
                    
                    # on down -> up, types a random cat fact (from the list of 'cat fact' variations above)
                    elif sequence('down', 'up'):
                        quickchat(variation('cat fact'))
                        break
                    


    except Exception as e:
        print(e)
        break
