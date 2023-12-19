import time
import os
import pyautogui
import keyboard
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

# Edit these if necessary
chatKeys = {
    'lobby': 't',
    'team': 'y',
    'party': 'u'
}

macrosOn = True

def press(button):
    return keyboard.is_pressed(button)

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
    if keyboard.is_pressed(button):
        global macrosOn
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

print(f"\n\n~~~~~~~~~~~~~~ KBM version ~~~~~~~~~~~~~~\n\nwaiting for quickchat inputs....\n\n")

# speech recognition init
r = sr.Recognizer()
mic = sr.Microphone()
with mic as source:
    r.adjust_for_ambient_noise(source) # <--- adjusts mic sensitvity for background noise based on a 1s sample of mic audio

while True:

    # blocks loop until a keyboard event happens (drastically reduces CPU usage)
    keyboard.read_key()
    
    try:



# -------------------------------------    Edit the code below to change quickchats, macros, spam amounts, chat modes, variations, etc.    --------------------------------------------------


      # ------------    Testing these macros via the terminal may cause the script to exit prematurely (due to auto typing), but it wont happen if another app is in focus    ---------------
       

        toggleMacros('home')

        if macrosOn:

            # When R + 4 is pressed, types "I pressed R and 4 at the same time."
            if press('r+4'):
                quickchat('I pressed R and 4 at the same time.')
                continue
    
            # When ctrl is pressed, types "I just pressed the control button" (spamming 2 times)
            elif press('ctrl'):
                quickchat('I just pressed the control button', spamCount=2)
                continue
                        
            # When Shift + up is pressed, types "I just pressed shift + up" (in team chat)
            elif press('shift+up'):
                quickchat('I just pressed shift + up', chatMode='team')
                continue
            
            # When down is pressed, types "that goal was [compliment]"  ......  where [compliment] is a random word from the 'compliment' variation list above
            elif press('down'):
                quickchat('that goal was ' + variation('compliment'))
                continue
            
            # When up is pressed, types "[compliment] pass [friend]"
            elif press('up'):
                quickchat(variation('compliment') + ' pass ' + variation('friend'))
                continue

            # When Delete is pressed, types a random cat fact from the 'cat fact' variation list above
            elif press('delete'):
                quickchat(variation('cat fact'))
                continue

            # When End is pressed, starts listening for speech-to-text (lobby chat)
            elif press('end'):
                quickchat(speechToText(mic))
                continue
              
            # When PgDn is pressed, starts listening for speech-to-text (team chat)
            elif press('pagedown'): 
                quickchat(speechToText(mic), chatMode='team')
                continue

            # autoclick things in AlphaConsole menu to enable ball texture
            elif press('pageup'):
                enableBallTexture()
                continue
        

    except Exception as e:
        print(e)
        break