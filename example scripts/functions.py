import time
import keyboard
import pyautogui
from random import sample
import speech_recognition as sr
import pygame



# ---------------------------------------- functions available to user (wrappers) -------------------------------------------


def toggleMacros(button: str):
    controllerObj.toggleMacros(button)

def combine(*buttons) -> bool:
    return controllerObj.combine(*buttons)

def sequence(b1: str, b2: str) -> bool:
    return controllerObj.sequence(b1, b2)

def quickchat(chat: str, chatMode: str = 'lobby', spamCount: int = 1, **effect):
    chatObj.quickchat(chat, chatMode, spamCount, **effect)

def variation(variationListName: str) -> str:
    return chatObj.variation(variationListName)

def speechToText() -> str | None:
    return chatObj.speechToText()

def enableBallTexture():
    autoclickerObj.enableBallTexture()

def toggleFastMode():
    autoclickerObj.toggleFastMode()


# ---------------------------------------- access class instances from main script ------------------------------------------

controllerObj = None
autoclickerObj = None
chatObj = None

def syncData(autoclicker, chat, controller=None):
    global controllerObj, autoclickerObj, chatObj
    if controller:
        controllerObj = controller
    autoclickerObj = autoclicker
    chatObj = chat



# ------------------------------------------  KBM specific functions ----------------------------------------------------------------------

kbmMacrosOn = True

def press(button):
    return keyboard.is_pressed(button)

def macrosAreOn():
    return kbmMacrosOn

def toggleKbmMacros(button):
    if keyboard.is_pressed(button):
        global kbmMacrosOn
        kbmMacrosOn = not kbmMacrosOn
        print(f'---------- macros toggled {"on" if kbmMacrosOn else "off"} ----------\n')
        time.sleep(.2)



# ------------------------------------------  Controller class  ---------------------------------------------------------------------------


class Controller:
    def __init__(self, buttons: dict, timeWindow: float = 1.1) -> None:
        pygame.init()
        pygame.event.set_blocked(None)  # first block all event types
        pygame.event.set_allowed([pygame.JOYBUTTONDOWN, pygame.JOYHATMOTION, pygame.JOYDEVICEADDED, pygame.JOYDEVICEREMOVED])  # then allow only specific event types
        self.buttons: dict = buttons
        self.macroTimeWindow: float = timeWindow
        self.pygameJoystick = None
        self.numHats: int = 0
        self.name: str = ""
        self.macrosOn: bool = True
        self.pressedButtons: list = []
        self.firstButtonPressed: dict = {
            'button': None,
            'time': 420
        }

    def getPygameEvent(self):
        return pygame.event.wait()
    
    def clearPygameEventQueue(self):
        pygame.event.clear()

    def handlePygameEvent(self, event) -> bool:     # returns whether or not the event was a button press
        if event.type == pygame.JOYDEVICEREMOVED:
            print('*** Controller disconnected ***\n')
            self.pygameJoystick.quit()
            return False
        elif event.type == pygame.JOYDEVICEADDED:
            print('*** Controller connected ***')
            pygame.joystick.init()
            self.pygameJoystick = pygame.joystick.Joystick(0)
            self.numHats = self.pygameJoystick.get_numhats()
            self.name = self.pygameJoystick.get_name()
            print("\nController hats:", self.numHats)     # easy way to determine if buttons dict needs tuple values
            if self.pygameJoystick.get_init():
                print(f"\n\n~~~~~~ {self.name} detected ~~~~~~\n\nwaiting for quickchat inputs....\n\n")
            return False
        else:
            self.readPressedButtons()
            return True

    # determine if a specific button is pressed
    def isPressed(self, button: str) -> bool:
        val = self.buttons[button]
        try:
            if type(val) is int:
                if self.pygameJoystick.get_button(val):
                    return True
            elif type(val) is tuple:
                if self.numHats > 0:
                    for i in range(self.numHats):
                        if self.pygameJoystick.get_hat(i) == val:
                            return True
        except Exception:
            return False
        return False

    # update list of all buttons pressed
    def readPressedButtons(self):
        pressedButtons = []
        for buttonName in self.buttons:
            if self.isPressed(buttonName):
                pressedButtons.append(buttonName)
        # if pressedButtons:                                      # <---- uncomment these 2 lines to test if your button mappings are valid
        #     print("pressedButtons:", pressedButtons)
        self.pressedButtons = pressedButtons

    def resetFirstButtonPressed(self):
        self.firstButtonPressed = {
            'button': None,
            'time': 420
        }
    
    def toggleMacros(self, button):
        if button in self.pressedButtons:
            self.macrosOn = not self.macrosOn
            print(f'---------- macros toggled {"on" if self.macrosOn else "off"} ----------\n')
            self.clearPygameEventQueue()
            time.sleep(.2)

    def combine(self, *buttons) -> bool:
        for button in buttons:
            if button not in self.pressedButtons:
                return False
        self.resetFirstButtonPressed()
        self.clearPygameEventQueue()
        return True

    def sequence(self, button1, button2) -> bool:
        button1Pressed = button1 in self.pressedButtons
        button2Pressed = button2 in self.pressedButtons
        if button1Pressed or button2Pressed:
            functionCallTime = time.time()
            if self.firstButtonPressed['button'] == None:
                if button1Pressed:
                    self.firstButtonPressed['time'] = functionCallTime
                    self.firstButtonPressed['button'] = button1
            else:
                if functionCallTime > (self.firstButtonPressed['time'] + self.macroTimeWindow):   # if button was pressed after (outside) the macro time window
                    if button1Pressed:
                        self.firstButtonPressed['time'] = functionCallTime
                        self.firstButtonPressed['button'] = button1
                    else:
                        self.resetFirstButtonPressed()
                else:                                                                   # if button was pressed within the macro time window
                    if button2Pressed:
                        if button1 == self.firstButtonPressed['button']:
                            if (functionCallTime > (self.firstButtonPressed['time'] + 0.05)):
                                self.resetFirstButtonPressed()
                                self.clearPygameEventQueue()
                                return True
        return False



# ------------------------------------------  Autoclicker class  --------------------------------------------------------------------------


class Autoclicker:
    def __init__(self, images: dict, fastMode: bool = True, attempts: int = 20) -> None:
        self.images = images
        self.fastModeEnabled = fastMode
        self.attemptsPerImage = attempts
        self.foundButtonCoords = {}
        self.screenWidth, self.screenHeight = pyautogui.size()
        pyautogui.FAILSAFE = False
        pyautogui.MINIMUM_DURATION = 0

    def enableBallTexture(self):
        startTime = time.perf_counter()
        pyautogui.sleep(.4)
        pyautogui.move(50, 50)
        try:
            if self.foundButtonCoords and self.fastModeEnabled:
                success = self.autoclickUsingCoords(startTime)
                if not success: 
                    self.cleanUpFailedJob(startTime)
                    self.foundButtonCoords = {}
            else:
                self.autoclickUsingImages(startTime)
        except Exception as e:
            print('Error:', e)

    def autoclickUsingImages(self, startTime: float):

        # find and click 'disable safe mode' button
        dsmCoords = self.clickImage(self.images["disableSafeMode"])
        pyautogui.sleep(.2)

        # find and click cosmetics tab
        # (using search region starting 175px above located 'disable safe mode' button, looking in a 150px region beneath)
        cosmeticsTabCoords = self.clickImage(self.images["cosmeticsTab"], confidence=0.8, region=(self.getRegion('cosmeticsTab', dsmCoords)))

        # find and click ball texture dropdown
        # (using search region starting 100px below located cosmetics tab, looking in a 250px region beneath)
        dropdownCoords = self.clickImage(self.images["ballTextureDropdown"], region=(self.getRegion('ballTextureDropdown', cosmeticsTabCoords)))

        # find and click ball texture
        # (using search region starting 15px below located dropdown menu (to avoid false positive in dropdown menu), looking in a 275px region beneath)
        ballSelectionCoords = self.clickImage(self.images["ballSelection"], region=(self.getRegion('ballSelection', dropdownCoords)))

        # find and click 'x' button to exit
        # (using search region starting 250px above located ball texture, looking in a 150px region beneath)
        xButtonCoords = self.clickImage(self.images["xButton"], region=(self.getRegion('xButton', ballSelectionCoords)))

        self.foundButtonCoords['disableSafeMode'] = dsmCoords
        self.foundButtonCoords['cosmeticsTab'] = cosmeticsTabCoords
        self.foundButtonCoords['ballTextureDropdown'] = dropdownCoords
        self.foundButtonCoords['ballSelection'] = ballSelectionCoords
        self.foundButtonCoords['xButton'] = xButtonCoords

        print(f'\n<<<<<  Enabled ball texture in {round((time.perf_counter() - startTime), 2)}s  >>>>>\n')

    def autoclickUsingCoords(self, startTime: float) -> bool:
        for button, coords in self.foundButtonCoords.items():
            if button == 'disableSafeMode':
                self.clickCoord(coords)
                pyautogui.sleep(.3)
            else:
                self.clickCoord(coords)
        endTime = time.perf_counter() - startTime

        # check work by searching for x button on screen
        pyautogui.move(50, 50)
        xButtonFound = False
        for i in range(2):      # 2 passes to weed out any chance of opencv error not finding xButton when it's actually there
            try:
                pyautogui.locateCenterOnScreen(self.images["xButton"], confidence=.8, grayscale=True)
                xButtonFound = True
                break
            except pyautogui.ImageNotFoundException:
                pass
            pyautogui.sleep(.1)
        if xButtonFound:
            return False
        print(f'\n<<<<<  Enabled ball texture in {round((endTime), 2)}s  (fast mode)  >>>>>\n')
        return True
    
    # finish failed autoclick job using reliable image search method
    def cleanUpFailedJob(self, startTime: float):
        leftOff =  {
            "image": None,
            "coords": None
        }
        for key, val in self.images.items():
            try:
                leftOff["coords"] = pyautogui.locateCenterOnScreen(val, confidence=.8, grayscale=True)
                leftOff["image"] = key
                break
            except Exception as e:
                print(e)
        shouldProceed = False
        foundImageCoords = leftOff["coords"]
        if foundImageCoords:
            for key, val in self.images.items():
                if key == leftOff["image"]:
                    shouldProceed = True
                try:
                    if shouldProceed:
                        if key == 'disableSafeMode' or not foundImageCoords:
                            foundImageCoords = self.clickImage(val)
                            pyautogui.sleep(.2)
                        else:
                            foundImageCoords = self.clickImage(val, confidence=.8, region=self.getRegion(key, foundImageCoords))
                except Exception as e:
                    print(e)
        print(f'\n<<<<<  Enabled ball texture in {round((time.perf_counter() - startTime), 2)}s  (fast mode failed... probably bc position/size of AlphaConsole menu changed)  >>>>>\n')
    
    def clickImage(self, image: str, confidence: float = 0.9, grayscale: bool = True, region=None):
        noRegion = not region
        lastResort = round(0.3 * self.attemptsPerImage)      # last resort will kick in after 30% of attempts have failed
        for i in range(self.attemptsPerImage):
            try:
                imageCoords = pyautogui.locateCenterOnScreen(image, confidence=confidence, grayscale=grayscale) \
                    if (noRegion) else pyautogui.locateCenterOnScreen(image, confidence=confidence, grayscale=grayscale, region=region)
                pyautogui.mouseDown(imageCoords[0], imageCoords[1])
                # pyautogui.sleep(.05)      # uncomment this line if autoclicker clicks dont register correctly
                pyautogui.mouseUp()
                return imageCoords
            except Exception as e:
                print(e)
                imageName = image.split('/')[1]     # used specifically for image file paths declared in main script ... this line should change if those filepaths change
                if (i >= lastResort and i < self.attemptsPerImage - 1):
                    print(f'\n[attempt {i+1}] ... couldn\'t find "{imageName}" by searching entire screen (slower)')
                    noRegion = True
                elif (i < lastResort and i < self.attemptsPerImage - 1):
                    if noRegion:
                        print(f'\n[attempt {i+1}] ... couldn\'t find "{imageName}" by searching entire screen (slower)')
                    else:
                        print(f'\n[attempt {i+1}] ... couldn\'t find "{imageName}" in region {region}')
                else:
                    print(f'\n[attempt {i+1}] couldn\'t locate "{imageName}" on screen :(')
                    print(f'\nCheck this guide for a potential fix:\nhttps://github.com/smallest-cock/RL-Custom-Quickchat/#autoclicker-not-working-correctly\n')
            pyautogui.sleep(.1)
    
    def clickCoord(self, coordTuple):
        pyautogui.mouseDown(coordTuple[0], coordTuple[1])
        pyautogui.mouseUp()

    def getRegion(self, image, prevImageCoords):
        def checkWithinScreenBounds(top, height):
            return ((top >= 0) and (top <= self.screenHeight)) and ((top + height >= 0) and (top + height <= self.screenHeight))
        match image:
            case 'cosmeticsTab':
                return (0, prevImageCoords[1] - 175, self.screenWidth, 150) if checkWithinScreenBounds(prevImageCoords[1] - 175, 150) else None
            case 'ballTextureDropdown':
                return (0, prevImageCoords[1] + 100, self.screenWidth, 250) if checkWithinScreenBounds(prevImageCoords[1] + 100, 250) else None
            case 'ballSelection':
                return (0, prevImageCoords[1] + 15, self.screenWidth, 275) if checkWithinScreenBounds(prevImageCoords[1] + 15, 275) else None
            case 'xButton':
                return (0, prevImageCoords[1] - 250, self.screenWidth, 150) if checkWithinScreenBounds(prevImageCoords[1] - 250, 150) else None
            
    def toggleFastMode(self):
        self.fastModeEnabled = not self.fastModeEnabled
        print(f'-------- autoclicker fast mode toggled {"on" if self.fastModeEnabled else "off"} --------\n')
           


# ------------------------------------------  Chat class  --------------------------------------------------------------------------------- 


class Chat():
    def __init__(self, chatKeys: dict, typingDelay: float, chatSpamInterval: float, sttEnabled: bool, variations: dict) -> None:
        self.chatKeys = chatKeys
        self.typingDelay = typingDelay
        self.chatSpamInterval = chatSpamInterval
        self.speechToTextEnabled = sttEnabled
        self.variations = variations
        self.shuffledVariations = {}

        # speech recognition init
        if self.speechToTextEnabled:
            try:
                print('\nAdjusting mic sensitivity for ambient noise ...\n')
                self.recognizer = sr.Recognizer()
                self.mic = sr.Microphone()
                with self.mic as source:
                    self.recognizer.adjust_for_ambient_noise(source)
            except OSError:
                print("No mic detected! Speech-to-text will be disabled.\n")
                self.speechToTextEnabled = False
            except Exception as e:
                print(e)
                self.speechToTextEnabled = False


    def quickchat(self, chat: str, chatMode='lobby', spamCount=1, **effect):
        if not chat:
            print('quickchat failed\t(there was nothing to quickchat)\n')
            return
    
        # add text effects
        if effect:    
            for effectName, value in effect.items():
                if effectName == 'sarcasm' and value:
                    chat = self.sarcasticText(chat)
                elif effectName == 'inQuotes' and value:
                    chat = self.wrapInQuotes(chat)
                elif effectName == 'quotedAs' and value:
                    chat = self.quotedAs(chat, value)                

        try:
            for i in range(spamCount):
                pyautogui.press(self.chatKeys[chatMode])
                pyautogui.write(chat, interval=self.typingDelay)
                pyautogui.press('enter')
                print(f'[{chatMode}]    {chat}\n')
                pyautogui.sleep(self.chatSpamInterval)
        except Exception as e:
            print(e)

    def variation(self, variationListName: str) -> str:
        index = self.shuffledVariations[variationListName]['nextUsableIndex']
        if not len(self.shuffledVariations[variationListName]['randomizedList']) > 2:
            print(f'The "{variationListName}" variation list has less than 3 items... it cannot be used properly!! Please add more items (words/phrases)')
            return f'My "{variationListName}" word variation list needs more words :('
        else:
            if index < (len(self.shuffledVariations[variationListName]['randomizedList'])):
                randWord = self.shuffledVariations[variationListName]['randomizedList'][index]
                self.shuffledVariations[variationListName]['nextUsableIndex'] += 1
                return randWord
            else:
                self.shuffleVariations(variationListName)
                randWord = self.shuffledVariations[variationListName]['randomizedList'][0]
                self.shuffledVariations[variationListName]['nextUsableIndex'] += 1
                return randWord
            
    def shuffleVariations(self, key=''):
        if not (key == ''):
            lastWordUsed = self.shuffledVariations[key]['randomizedList'][len(self.variations[key]) - 1]
            secondLastWordUsed = self.shuffledVariations[key]['randomizedList'][len(self.variations[key]) - 2]
            while True:
                shuffledList = sample(self.variations[key], len(self.variations[key]))
                if not (shuffledList[0] == lastWordUsed) and (shuffledList[1] == secondLastWordUsed):
                    self.shuffledVariations[key]['randomizedList'] = shuffledList
                    self.shuffledVariations[key]['nextUsableIndex'] = 0
                    break
        else:
            for key in self.variations:
                self.shuffledVariations[key] = {
                    'randomizedList': sample(self.variations[key], len(self.variations[key])),
                    'nextUsableIndex': 0
                }

    def speechToText(self) -> str | None:
        if self.speechToTextEnabled:
            try:
                with self.mic as source:
                    print('speak now...\n')
                    audio = self.recognizer.listen(source, timeout=5)
            except sr.WaitTimeoutError:
                print('Error: Listening timed out while waiting for speech\t(you didnt speak within 5s, or your mic is muted)\n')
                return None
            startInterpretationTime = time.perf_counter()
            transcription: str | None = None
            try:
                transcription = self.recognizer.recognize_google(audio)
                interpretationTime = time.perf_counter() - startInterpretationTime
                print(f'({round(interpretationTime, 2)}s interpretation)\n')
            except sr.RequestError:
                # API was unreachable or unresponsive
                print("Error: Speech-to-text API is unavailable\n")
            except sr.UnknownValueError:
                # speech was unintelligible
                print("Error: Unable to recognize speech ...\n")
            except Exception as e:
                print("Error:", e)
            return transcription.lower() if transcription else None
        else:
            print("*** Speech-to-text is disabled ***\n")
    
    # ------------------------------------------  text effects  ------------------------------------------

    def sarcasticText(self, str: str) -> str:
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
            
    def wrapInQuotes(self, str: str) -> str:
        return f'"{str}"'

    def quotedAs(self, str: str, quoteAuthor: str) -> str:
        return f'"{str}" - {quoteAuthor}'
    