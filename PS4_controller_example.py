import time
import os
import pyautogui
import pygame
from random import sample
import speech_recognition as sr


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

# PNG images for autoclicker
disableSafeModeButtonImage = 'dsm.png'
cosmeticsTabImage = 'cosmetics_tab.png'
ballTextureDropdownImage = 'ball_texture_dropdown.png'
ballSelectionImage = 'ball_selection.png'

# Adjusts chat typing speed (seconds per character) ...
typingDelay = .002          # 0 makes chats type out instantly (but will cut off long chats)
                            # .001 will allow long chats (but occasionally goes too fast for RL, causing typos)
                            # .002 seems to be slow enough for the RL chat box to reliably keep up (no typos)

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

macrosOn = True

def resetFirstButtonPressed():
    firstButtonPressed['button'] = None     
    firstButtonPressed['time'] = 420

# detects simultaneous button presses
def combine(button1, button2):
    for i in range(numJoysticks):
        if joysticks[i].get_button(buttons[button1]) and joysticks[i].get_button(buttons[button2]):
            resetFirstButtonPressed()
            return True
        else: return False

# detects successive button presses (buttons pressed in a specific order)
def sequence(button1, button2):
    global firstButtonPressed
    functionCallTime = time.time()
    for i in range(numJoysticks):
        if firstButtonPressed['button'] == None:
            if joysticks[i].get_button(buttons[button1]):
                firstButtonPressed['time'] = functionCallTime
                firstButtonPressed['button'] = button1
                return False
            else: return False
        else:
            if functionCallTime > (firstButtonPressed['time'] + macroTimeWindow):
                if joysticks[i].get_button(buttons[button1]):
                    firstButtonPressed['time'] = functionCallTime
                    firstButtonPressed['button'] = button1
                    return False
                else:
                    resetFirstButtonPressed()
                    return False
            else:
                if joysticks[i].get_button(buttons[button2]):
                    if button1 == firstButtonPressed['button']:
                        if (functionCallTime > (firstButtonPressed['time'] + 0.05)):
                            resetFirstButtonPressed()
                            return True
                        else: return False
                    else: return False   
                else: return False

def quickchat(thing, chatMode='lobby', spamCount=1):
    if not thing: 
        print('quickchat failed.. (there was nothing to quickchat)\n')
        return
    try:
        for i in range(spamCount):
            pyautogui.press(chatKeys[chatMode])
            pyautogui.write(thing, interval=typingDelay)
            pyautogui.press('enter')
            print(f'[{chatMode}]    {thing}\n')
            time.sleep(chatSpamInterval)
    except Exception as e:
        print(e)

def toggleMacros(button):
    for i in range(numJoysticks):
        if joysticks[i].get_button(buttons[button]):
            global macrosOn
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

def speechToText(microphone):
    try:
        with microphone as source:
            print('speak now...\n')
            audio = r.listen(source, timeout=5)
    except sr.WaitTimeoutError:
        print(' -- Listening timed out while waiting for phrase to start -- (you didnt speak within 5s, or your mic is muted)')
        return None

    startInterpretationTime = time.time()
    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": 'my speech recognition failed :(',
        "interpretation time": None
    }

    try:
        response["transcription"] = r.recognize_google(audio)
        response["interpretation time"] = time.time() - startInterpretationTime
        print(f'({round(response["interpretation time"], 2)}s interpretation)\n')
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
        print(response)
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"
        print(response)
    except Exception as e:
        print(e)
        return

    return response['transcription'].lower()

# Auto click things in AlphaConsole menu to enable ball texture
def enableBallTexture():
    time.sleep(1)
    pyautogui.move(50, 50)
    try:
        # find and click disable safemode button
        disableSafeModeButtonCoords = pyautogui.locateCenterOnScreen(disableSafeModeButtonImage, confidence=0.9, grayscale=True)
        pyautogui.moveTo(disableSafeModeButtonCoords[0], disableSafeModeButtonCoords[1])
        pyautogui.mouseDown()
        time.sleep(.1)
        pyautogui.mouseUp()
        time.sleep(.3)

        # find and click cosmetics tab
        cosmeticsTabCoords = pyautogui.locateCenterOnScreen(cosmeticsTabImage, confidence=0.8, grayscale=True)
        pyautogui.moveTo(cosmeticsTabCoords[0], cosmeticsTabCoords[1])
        pyautogui.mouseDown()
        time.sleep(.1)
        pyautogui.mouseUp()

        # find and click ball texture dropdown
        dropdownCoords = pyautogui.locateCenterOnScreen(ballTextureDropdownImage, confidence=0.9, grayscale=True)
        pyautogui.moveTo(dropdownCoords[0], dropdownCoords[1])
        pyautogui.mouseDown()
        time.sleep(.1)
        pyautogui.mouseUp()

        # find and click ball texture
        ballSelectionCoords = pyautogui.locateCenterOnScreen(ballSelectionImage, confidence=0.99, grayscale=False)
        pyautogui.moveTo(ballSelectionCoords[0], ballSelectionCoords[1])
        pyautogui.mouseDown()
        time.sleep(.1)
        pyautogui.mouseUp()

    except Exception as e:
        print(e)

# change working directory to script directory (so .png files are easily located)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

shuffledVariations = variations.copy()
shuffleVariations()
pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

for controller in joysticks:
    if controller.get_init() == True:
        print(f"\n\n~~~~~~ {controller.get_name()} detected ~~~~~~\n\nwaiting for quickchat inputs....\n\n")

# speech recognition init
r = sr.Recognizer()
mic = sr.Microphone()
with mic as source:
    r.adjust_for_ambient_noise(source) # <--- adjusts mic sensitvity for background noise based on a 1s sample of mic audio

while True:
    try:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                numJoysticks = pygame.joystick.get_count()



# ---------------------------------    Edit the code below to change quickchats, macros, spam amounts, chat modes, variations, etc.    --------------------------------------------------


                
                toggleMacros('ps') # <-- 'ps' is the button used to toggle on/off quick chat macros (PlayStation button)..... change as you please

                if macrosOn:

                    # on square + up, types "noice"
                    if combine('square', 'up'):
                        quickchat('noice')
                        break
                    
                    # on square + left, types "dont lose this kickoff" (spamming 2 times)
                    elif combine('square', 'left'):
                        quickchat('dont lose this kickoff', spamCount=2)  # <-- the '2' parameter is how many times the chat will be spammed.. the max you can put is 3 (before RL gives a chat timeout)
                        break
                    
                    # on circle + up, types "tell me how you really feel..." (using team chat)
                    elif combine('circle', 'up'):
                        quickchat('tell me how you really feel...', chatMode='team')
                        break
                    
                    # on X + right, types "im lagging" (using team chat, spamming 3 times)
                    elif combine('x', 'right'):
                        quickchat('im lagging', chatMode='team', spamCount=3)
                        break

                    # on up -> right, types "let me cook"
                    elif sequence('up', 'right'):
                        quickchat('let me cook')
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
                    
                    # on L1 + right, types "Wassup [friend]! Nice to see you again."
                    elif combine('L1', 'right'):
                        quickchat('Wassup %s! Nice to see you again.' % variation('friend'))    # <-- Yet another way to format word variations in your chats
                        break
                    
                    # on down -> up, types a random cat fact (from the list of 'cat fact' variations above)
                    elif sequence('down', 'up'):
                        quickchat(variation('cat fact'))
                        break
                        
                    # on x + up, starts listening for speech-to-text (lobby chat)
                    elif combine('x', 'up'): 
                        quickchat(speechToText(mic))
                        break
                    
                    # on x + left, starts listening for speech-to-text (team chat)
                    elif combine('x', 'left'): 
                        quickchat(speechToText(mic), chatMode='team')
                        break
                    
                    # enable custom ball texture in a match
                    elif combine('triangle', 'left'):
                        enableBallTexture()
                        break

    
    except Exception as e:
        print(e)
        break
