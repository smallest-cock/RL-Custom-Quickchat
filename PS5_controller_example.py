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
xButton = 'x.png'

autoclickAttemptsPerImage = 20

# Adjusts chat typing speed (seconds per character) ...
typingDelay = .002          # 0 makes chats type out instantly (but will cut off long chats)
                            # .001 will allow long chats (but occasionally goes too fast for RL, causing typos)
                            # .002 seems to be slow enough for the RL chat box to reliably keep up (no typos)

# Time interval between spammed chats (0.2 seconds).... change as you please
chatSpamInterval = .2

# Time window given to read button sequence macros (1.1 seconds).... you can change this as you please
macroTimeWindow = 1.1

# Edit these if necessary
chatKeys = {
    'lobby': 't',
    'team': 'y',
    'party': 'u'
}

# PS5 controller button mappings for pygame.... these may be incorrect because I dont own a PS5 controller  (refer to https://www.pygame.org/docs/ref/joystick.html)
buttons = {
    'x': 0,
    'circle': 1,
    'square': 2,
    'triangle': 3,
    'L1': 4,
    'R1': 5,
    'share': 8, 
    'options': 9,
    'ps': 10,
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
    for key in buttons:
        buttonVal = buttons[key]
        if controllerHasHats:
            if buttonPressedIsHat:
                if type(buttonVal) is tuple:
                    if controller.get_hat(0) == buttonVal:
                        for otherKey in buttons:
                            if not (otherKey == key):
                                otherButtonVal = buttons[otherKey]
                                if type(otherButtonVal) is tuple:
                                    if controller.get_hat(0) == otherButtonVal:
                                        return [buttonVal, otherButtonVal]
                                else:
                                    if controller.get_button(otherButtonVal):
                                        return [buttonVal, otherButtonVal]
                        return buttonVal
                    else: continue
                else: continue
            else:
                if type(buttonVal) is int:
                    if controller.get_button(buttonVal):
                        for otherKey in buttons:
                            if not (otherKey == key):
                                otherButtonVal = buttons[otherKey]
                                if type(otherButtonVal) is tuple:
                                    if controller.get_hat(0) == otherButtonVal:
                                        return [buttonVal, otherButtonVal]
                                else:
                                    if controller.get_button(otherButtonVal):
                                        return [buttonVal, otherButtonVal]
                        return buttonVal
                    else: continue
                else: continue
        else:
            if not type(buttonVal) is tuple:
                if controller.get_button(buttonVal):
                    for otherKey in buttons:
                        if not (otherKey == key):
                            otherButtonVal = buttons[otherKey]
                            if not type(otherButtonVal) is tuple:
                                if controller.get_button(otherButtonVal):
                                    return [buttonVal, otherButtonVal]                                    
                    return buttonVal
    return None 

def resetFirstButtonPressed():
    firstButtonPressed['button'] = None     
    firstButtonPressed['time'] = 420

def checkIfPressedButtonIsHat(event):
    if event.type == pygame.JOYHATMOTION:
        return True
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
    global macrosOn
    if not type(buttonPressed) is list:
        buttonValue = buttons[button]
        if buttonValue == buttonPressed:
            macrosOn = not macrosOn
            if macrosOn:
                print('---------- macros toggled on ----------\n')
            else:
                print('---------- macros toggled off ----------\n')
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

def clickThing(image, confidence=0.9, grayscale=True, region=None):
    noRegion = not region
    lastResort = round(0.6 * autoclickAttemptsPerImage) # last resort will start after 60% of attempts have failed
    for i in range(autoclickAttemptsPerImage):
        try:
            imageCoords = pyautogui.locateCenterOnScreen(image, confidence=confidence, grayscale=grayscale) \
                if (noRegion) else pyautogui.locateCenterOnScreen(image, confidence=confidence, grayscale=grayscale, region=region)
            pyautogui.moveTo(imageCoords[0], imageCoords[1])
            pyautogui.mouseDown()
            time.sleep(.05)
            pyautogui.mouseUp()
            return imageCoords
        except Exception as e:
            print(e)
            if (i >= lastResort and i < autoclickAttemptsPerImage - 1):
                print(f'\n[attempt {i+1}] ... couldn\'t find "{image}" by searching entire screen (slower)')
                noRegion = True
            elif (i < lastResort and i < autoclickAttemptsPerImage - 1):
                if noRegion:
                    print(f'\n[attempt {i+1}] ... couldn\'t find "{image}" by searching entire screen (slower)')
                else:
                    print(f'\n[attempt {i+1}] ... couldn\'t find "{image}" in specified region')
            else:
                print(f'\n[attempt {i+1}] couldn\'t locate "{image}" on screen :(')
                print(f'\nCheck this guide for a potential fix:\nhttps://github.com/smallest-cock/RL-Custom-Quickchat/#autoclicker-isnt-working-correctly\n')

def enableBallTexture():
    startTime = time.time()
    time.sleep(.4)
    pyautogui.move(50, 50)
    try:
        # find and click 'disable safe mode' button
        disableSafeModeButtonCoords = clickThing(disableSafeModeButtonImage)
        time.sleep(.2)

        # find and click cosmetics tab
        # (start searching 175px above located 'disable safe mode' button, looking in a 150px region beneath)
        cosmeticsTabCoords = clickThing(cosmeticsTabImage, confidence=0.8, region=(0, disableSafeModeButtonCoords[1] - 175, screenWidth, 150))

        # find and click ball texture dropdown
        # (start searching 100px below located cosmetics tab, looking in a 250px region beneath)
        dropdownCoords = clickThing(ballTextureDropdownImage, region=(0, cosmeticsTabCoords[1] + 100, screenWidth, 250))

        # find and click ball texture 
        # (start searching 15px below located dropdown menu (to avoid false positive in dropdown menu), looking in a 275px region beneath)
        ballSelectionCoords = clickThing(ballSelectionImage, region=(0, dropdownCoords[1] + 15, screenWidth, 275))

        # find and click 'x' button to exit
        # (start searching 250px above located ball texture, looking in a 150px region beneath)
        clickThing(xButton, region=(0, ballSelectionCoords[1] - 250, screenWidth, 150))
    
        print(f'\n<<<<<  Enabled ball texture in {round((time.time() - startTime), 2)}s  >>>>>\n')
    except TypeError:
        return
    except Exception as e:
        print('Error:', e)

# change working directory to script directory (so .png files are easily located)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

screenWidth, screenHeight = pyautogui.size()
shuffledVariations = variations.copy()
shuffleVariations()
pygame.init()
clock = pygame.time.Clock()
controllerHasHats = False

# speech recognition init
r = sr.Recognizer()
mic = sr.Microphone()
with mic as source:
    r.adjust_for_ambient_noise(source) # <--- adjusts mic sensitvity for background noise based on a 1s sample of mic audio

while True:
    try:
        for event in pygame.event.get():
            if event.type == pygame.JOYDEVICEREMOVED:
                print('*** Controller disconnected ***\n')
                controller.quit()
            elif event.type == pygame.JOYDEVICEADDED:
                print('*** Controller connected ***')
                pygame.joystick.init()
                controller = pygame.joystick.Joystick(0)
                if controller.get_numhats() > 0:
                    controllerHasHats = True
                if controller.get_init() == True:
                    print(
                        f"\n\n~~~~~~ {controller.get_name()} detected ~~~~~~\n\nwaiting for quickchat inputs....\n\n")
            elif (event.type == pygame.JOYBUTTONDOWN) or (event.type == pygame.JOYHATMOTION):
                buttonPressedIsHat = checkIfPressedButtonIsHat(event)
                buttonPressed = detectButtonPressed()



# ---------------------------------    Edit the code below to change quickchats, macros, spam amounts, chat modes, variations, etc.    --------------------------------------------------



                toggleMacros('triangle') # <-- 'triangle' is the button used to toggle on/off macros..... change as you please

                if macrosOn:
                    
                    # on square + x, types "let me cook"
                    if combine('square', 'x'):
                        quickchat('let me cook')
                        break
                
                    # on square + left, types "dont lose this kickoff" (spamming 2 times)
                    elif combine('square', 'left'):
                        quickchat('dont lose this kickoff', spamCount=2)  # <-- the '2' parameter is how many times the chat will be spammed.. the max you can put is 3 (before RL gives a chat timeout)
                        break
                    
                    # on circle + square, types "tell me how you really feel..." (using team chat)
                    elif combine('circle', 'square'):
                        quickchat('tell me how you really feel...', chatMode='team')
                        break
                    
                    # on x -> circle, types "im lagging" (using team chat, spamming 3 times)
                    elif sequence('x', 'circle'):
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

                    # autoclick things in AlphaConsole menu to enable ball texture
                    elif combine('triangle', 'left'):
                        enableBallTexture()
                        break
                    

    except Exception as e:
        print(e)
        break

    # limit pygame refresh rate to "30 FPS" (drastically reduces CPU usage)
    clock.tick(30)