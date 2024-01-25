import time
import keyboard
import pyautogui
from random import sample
import speech_recognition as sr



# ------------------------------------------  KBM specific  -------------------------------------------------------------------------------
    

def press(button):
    return keyboard.is_pressed(button)

def toggleKbmMacros(button):
    if keyboard.is_pressed(button):
        global macrosOn
        macrosOn = not macrosOn
        print(f'---------- macros toggled {"on" if macrosOn else "off"} ----------\n')
        time.sleep(.2)


# ------------------------------------------  controller specific  ------------------------------------------------------------------------


# determine if a button combination has been pressed
def combine(*buttons):
    for button in buttons:
        if not (button in pressedButtons):
            return False
    return True

# determine if a button sequence has been pressed ... limited to a 2 button sequence at the moment
def sequence(button1, button2):
    button1Pressed = button1 in pressedButtons
    button2Pressed = button2 in pressedButtons
    if button1Pressed or button2Pressed:
        global firstButtonPressed
        functionCallTime = time.time()
        if firstButtonPressed['button'] == None:
            if button1Pressed:
                firstButtonPressed['time'] = functionCallTime
                firstButtonPressed['button'] = button1
        else:
            if functionCallTime > (firstButtonPressed['time'] + mainScriptData["timeWindow"]):   # if the button was pressed after (outside) the macro time window
                if button1Pressed:
                    firstButtonPressed['time'] = functionCallTime
                    firstButtonPressed['button'] = button1
                else:
                    resetFirstButtonPressed()
            else:                                                                   # if the button was pressed within the macro time window
                if button2Pressed:
                    if button1 == firstButtonPressed['button']:
                        if (functionCallTime > (firstButtonPressed['time'] + 0.05)):
                            resetFirstButtonPressed()
                            return True
    return False

# determine if a specific button is pressed
def isPressed(button):
    val = mainScriptData["buttons"][button]
    if type(val) is int:
        try:
            if controller.get_button(val):
                return True
        except Exception:
            return False
    elif type(val) is tuple:
        if numHatsOnController > 0:
            try:
                for i in range(numHatsOnController):
                    if controller.get_hat(i) == val:
                        return True
            except Exception:
                return False
    return False

# return a list of all buttons pressed
def getAllButtonsPressed():
    pressedButtons = []
    for buttonName in mainScriptData["buttons"]:
        if isPressed(buttonName):
            pressedButtons.append(buttonName)
    # if pressedButtons:                                      # <---- uncomment these 2 lines to test if your button mappings are valid
    #     print("pressedButtons:", pressedButtons)
    return pressedButtons

def toggleMacros(button):
    if button in pressedButtons:
        global macrosOn
        macrosOn = not macrosOn
        print(f'---------- macros toggled {"on" if macrosOn else "off"} ----------\n')
        time.sleep(.2)

def getPressedButtonsList():
    return pressedButtons

def updatePressedButtons(pressedList: list):
    global pressedButtons
    pressedButtons = pressedList

def updateController(mainScriptController, numHats: int):
    global controller
    global numHatsOnController
    controller = mainScriptController
    numHatsOnController = numHats

def resetFirstButtonPressed():
    global firstButtonPressed
    firstButtonPressed["button"] = None
    firstButtonPressed['time'] = 420


# ------------------------------------------  autoclicker functions  ----------------------------------------------------------------------


def clickImage(image: str, confidence=0.9, grayscale=True, region=None):
    noRegion = not region
    attempts = mainScriptData["autoclickAttemptsPerImage"]
    lastResort = round(0.3 * attempts)      # last resort will kick in after 30% of attempts have failed
    for i in range(attempts):
        try:
            imageCoords = pyautogui.locateCenterOnScreen(image, confidence=confidence, grayscale=grayscale) \
                if (noRegion) else pyautogui.locateCenterOnScreen(image, confidence=confidence, grayscale=grayscale, region=region)
            pyautogui.mouseDown(imageCoords[0], imageCoords[1])
            pyautogui.sleep(.05)
            pyautogui.mouseUp()
            return imageCoords
        except Exception as e:
            print(e)
            imageName = image.split('/')[1]
            if (i >= lastResort and i < attempts - 1):
                print(f'\n[attempt {i+1}] ... couldn\'t find "{imageName}" by searching entire screen (slower)')
                noRegion = True
            elif (i < lastResort and i < attempts - 1):
                if noRegion:
                    print(f'\n[attempt {i+1}] ... couldn\'t find "{imageName}" by searching entire screen (slower)')
                else:
                    print(f'\n[attempt {i+1}] ... couldn\'t find "{imageName}" in region {region}')
            else:
                print(f'\n[attempt {i+1}] couldn\'t locate "{imageName}" on screen :(')
                print(f'\nCheck this guide for a potential fix:\nhttps://github.com/smallest-cock/RL-Custom-Quickchat/#autoclicker-not-working-correctly\n')
        pyautogui.sleep(.1)

def clickCoord(coordTuple):
    pyautogui.mouseDown(coordTuple[0], coordTuple[1])
    pyautogui.sleep(.05)
    pyautogui.mouseUp()

def checkWithinScreenBounds(top, height):
    return ((top >= 0) and (top <= screenHeight)) and ((top + height >= 0) and (top + height <= screenHeight))

def getRegion(image, prevImageCoords):
    match image:
        case 'cosmeticsTab':
            return (0, prevImageCoords[1] - 175, screenWidth, 150) if checkWithinScreenBounds(prevImageCoords[1] - 175, 150) else None
        case 'ballTextureDropdown':
            return (0, prevImageCoords[1] + 100, screenWidth, 250) if checkWithinScreenBounds(prevImageCoords[1] + 100, 250) else None
        case 'ballSelection':
            return (0, prevImageCoords[1] + 15, screenWidth, 275) if checkWithinScreenBounds(prevImageCoords[1] + 15, 275) else None
        case 'xButton':
            return (0, prevImageCoords[1] - 250, screenWidth, 150) if checkWithinScreenBounds(prevImageCoords[1] - 250, 150) else None

def findWhereAutoclickerLeftOff():
    leftOff =  {
        "image": None,
        "coords": None
    }
    for key, val in mainScriptData["autoclickerImages"].items():
        try:
            leftOff["coords"] = pyautogui.locateCenterOnScreen(val, confidence=.8, grayscale=True)
            leftOff["image"] = key
            break
        except Exception as e:
            print(e)
    return leftOff

# finish a failed autoclick job using reliable image search method
def cleanUpFailedAutoclickJob(startTime):
    leftOff = findWhereAutoclickerLeftOff()
    shouldProceed = False
    foundImageCoords = leftOff["coords"]
    if foundImageCoords:
        for key, val in mainScriptData["autoclickerImages"].items():
            if key == leftOff["image"]:
                shouldProceed = True
            try:
                if shouldProceed:
                    if key == 'disableSafeMode' or not foundImageCoords:
                        foundImageCoords = clickImage(val)
                        pyautogui.sleep(.2)
                    else:
                        foundImageCoords = clickImage(val, confidence=.8, region=getRegion(key, foundImageCoords))
            except Exception as e:
                print(e)
    print(f'\n<<<<<  Enabled ball texture in {round((time.perf_counter() - startTime), 2)}s  (fast method failed... probably bc position/size of AlphaConsole menu changed)  >>>>>\n')

def autoclickUsingCoordList(foundButtonCoords: dict, startTime):
    for button, coords in foundButtonCoords.items():
        if button == 'disableSafeMode':
            clickCoord(coords)
            pyautogui.sleep(.2)
        else:
            clickCoord(coords)
    endTime = time.perf_counter() - startTime


    # check work by searching for x button on screen
    pyautogui.move(50, 50)
    xButtonFound = False
    for i in range(2):      # 2 passes to weed out any chance of opencv error not finding xButton when it's actually there
        try:
            pyautogui.locateCenterOnScreen(mainScriptData["autoclickerImages"]["xButton"], confidence=.8, grayscale=True)
            xButtonFound = True
            break
        except pyautogui.ImageNotFoundException:
            pass
        pyautogui.sleep(.1)
    if xButtonFound:
        return False
    print(f'\n<<<<<  Enabled ball texture in {round((endTime), 2)}s  (fast method)  >>>>>\n')
    return True
    
def autoclickUsingImages(startTime):
    global foundButtonCoords

    # find and click 'disable safe mode' button
    dsmCoords = clickImage(mainScriptData["autoclickerImages"]["disableSafeMode"])
    pyautogui.sleep(.2)

    # find and click cosmetics tab
    # (using search region starting 175px above located 'disable safe mode' button, looking in a 150px region beneath)
    cosmeticsTabCoords = clickImage(mainScriptData["autoclickerImages"]["cosmeticsTab"], confidence=0.8, region=(getRegion('cosmeticsTab', dsmCoords)))

    # find and click ball texture dropdown
    # (using search region starting 100px below located cosmetics tab, looking in a 250px region beneath)
    dropdownCoords = clickImage(mainScriptData["autoclickerImages"]["ballTextureDropdown"], region=(getRegion('ballTextureDropdown', cosmeticsTabCoords)))

    # find and click ball texture
    # (using search region starting 15px below located dropdown menu (to avoid false positive in dropdown menu), looking in a 275px region beneath)
    ballSelectionCoords = clickImage(mainScriptData["autoclickerImages"]["ballSelection"], region=(getRegion('ballSelection', dropdownCoords)))

    # find and click 'x' button to exit
    # (using search region starting 250px above located ball texture, looking in a 150px region beneath)
    xButtonCoords = clickImage(mainScriptData["autoclickerImages"]["xButton"], region=(getRegion('xButton', ballSelectionCoords)))

    foundButtonCoords = {
        'disableSafeMode': dsmCoords,
        'cosmeticsTab': cosmeticsTabCoords,
        'ballTextureDropdown': dropdownCoords,
        'ballSelection': ballSelectionCoords,
        'xButton': xButtonCoords
    }
    print(f'\n<<<<<  Enabled ball texture in {round((time.perf_counter() - startTime), 2)}s  >>>>>\n')

def enableBallTexture():
    global foundButtonCoords
    startTime = time.perf_counter()
    pyautogui.sleep(.4)
    pyautogui.move(50, 50)
    try:
        if foundButtonCoords:
            success = autoclickUsingCoordList(foundButtonCoords, startTime)
            if not success: 
                cleanUpFailedAutoclickJob(startTime)
                foundButtonCoords = None
        else:
            autoclickUsingImages(startTime)
    except Exception as e:
        print('Error:', e)


# ------------------------------------------  chatting functions  -------------------------------------------------------------------------


def speechToText():
    try:
        with mic as source:
            print('speak now...\n')
            audio = r.listen(source, timeout=5)
    except sr.WaitTimeoutError:
        print(' -- Listening timed out while waiting for phrase to start -- (you didnt speak within 5s, or your mic is muted)')
        return None
    startInterpretationTime = time.perf_counter()
    response = {
        "success": True,
        "error": None,
        "transcription": 'my speech recognition failed :(',
        "interpretation time": None
    }
    try:
        response["transcription"] = r.recognize_google(audio)
        response["interpretation time"] = time.perf_counter() - startInterpretationTime
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
    return response['transcription'].lower()

def quickchat(thing: str, chatMode='lobby', spamCount=1, **effect):
    if not thing:
        print('quickchat failed.. (there was nothing to quickchat)\n')
        return
    
    # add text effects
    if effect:    
        for effectName, value in effect.items():
            if effectName == 'sarcasm' and value:
                thing = sarcasticText(thing)
            elif effectName == 'inQuotes' and value:
                thing = wrapInQuotes(thing)
            elif effectName == 'quotedAs' and value:
                thing = quotedAs(thing, value)

    try:
        for i in range(spamCount):
            pyautogui.press(mainScriptData["chatKeys"][chatMode])
            pyautogui.write(thing, interval=mainScriptData["typingDelay"])
            pyautogui.press('enter')
            print(f'[{chatMode}]    {thing}\n')
            time.sleep(mainScriptData["chatSpamInterval"])
    except Exception as e:
        print(e)


# ------------------------------------------  text effects  -------------------------------------------------------------------------------


def sarcasticText(str: str):
    wordList = str.lower().split(' ')
    sarcasticWordList = []
    for word in wordList:
        newWord = ''
        for i in range(len(word)):
            if word[i].lower() == 'i':
                newWord += 'i'
            elif word[i].lower() == 'l':
                newWord += 'L'
            else:
                if (i % 2 == 1):
                    newWord += word[i].upper()
                else:
                    newWord += word[i]
        sarcasticWordList.append(newWord)
    return ' '.join(sarcasticWordList)
        
def wrapInQuotes(str: str):
    return f'"{str}"'

def quotedAs(str: str, variationListName: str):
    if variationListName in mainScriptData["variations"].keys():
        return f'"{str}" - {variation(variationListName)}'
    else:
        return str


# ------------------------------------------  miscellaneous  ------------------------------------------------------------------------------


def syncData(data: dict):
    global mainScriptData
    global shuffledVariations
    mainScriptData = data.copy()
    shuffledVariations = mainScriptData["variations"].copy()

def macrosAreOn():
    return macrosOn

def shuffleVariations(key=''):
    global shuffledVariations
    if not (key == ''):
        lastWordUsed = shuffledVariations[key]['randomizedList'][len(
            mainScriptData["variations"][key]) - 1]
        secondLastWordUsed = shuffledVariations[key]['randomizedList'][len(
            mainScriptData["variations"][key]) - 2]
        while True:
            shuffledList = sample(mainScriptData["variations"][key], len(mainScriptData["variations"][key]))
            if not (shuffledList[0] == lastWordUsed) and (shuffledList[1] == secondLastWordUsed):
                shuffledVariations[key]['randomizedList'] = shuffledList
                shuffledVariations[key]['nextUsableIndex'] = 0
                break
    else:
        for key in mainScriptData["variations"]:
            shuffledVariations[key] = {
                'randomizedList': sample(mainScriptData["variations"][key], len(mainScriptData["variations"][key])),
                'nextUsableIndex': 0
            }

def variation(variationListName: str):
    global shuffledVariations
    index = shuffledVariations[variationListName]['nextUsableIndex']
    if not len(shuffledVariations[variationListName]['randomizedList']) > 2:
        print(f'The "{variationListName}" variation list has less than 3 items..... it cannot be used properly!! Please add more items (words/phrases)')
        return '-- "' + variationListName + '" variation list needs more items --'
    else:
        if index < (len(shuffledVariations[variationListName]['randomizedList'])):
            randWord = shuffledVariations[variationListName]['randomizedList'][index]
            shuffledVariations[variationListName]['nextUsableIndex'] += 1
            return randWord
        else:
            shuffleVariations(variationListName)
            randWord = shuffledVariations[variationListName]['randomizedList'][0]
            shuffledVariations[variationListName]['nextUsableIndex'] += 1
            return randWord


# ------------------------------------------  stuff to init on import  --------------------------------------------------------------------


# create global variables
mainScriptData: dict = {}
shuffledVariations: dict = {}

controller = None
numHatsOnController : int = 0
pressedButtons : list = []
macrosOn: bool = True

foundButtonCoords: dict | None = None

firstButtonPressed: dict = {
    'button': None,
    'time': 420
}

# pyautogui init
screenWidth, screenHeight = pyautogui.size()
pyautogui.FAILSAFE = False

# speech recognition init
print('\nadjusting mic sensitivity for ambient noise ...\n')
r = sr.Recognizer()
mic = sr.Microphone()
with mic as source:
    r.adjust_for_ambient_noise(source)