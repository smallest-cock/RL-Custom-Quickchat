import time
import keyboard
import pyautogui
from random import sample
import speech_recognition as sr
import pygame
import json
import cv2



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

def lastChat() -> str | None:
    return lobbyInfoObj.lastChat()

def blastRanks() -> str | None :
    return lobbyInfoObj.blastRanks()

def blastRank(playlist: str) -> str | None:
    return lobbyInfoObj.blastRank(playlist)

def toggleFastMode():
    autoclickerObj.toggleFastMode()


# ---------------------------------------- access class instances from main script ------------------------------------------

controllerObj = None
autoclickerObj = None
lobbyInfoObj = None
chatObj = None

def syncData(autoclicker, lobbyInfo, chat, controller=None):
    global controllerObj, autoclickerObj, lobbyInfoObj, chatObj
    if controller:
        controllerObj = controller
    autoclickerObj = autoclicker
    lobbyInfoObj = lobbyInfo
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

    class Image:
        def __init__(self, name, path) -> None:
            self.name = name
            self.path = path
            img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            height, width, channels = img.shape
            self.height = height
            self.width = width
            self.searchRegion = None
            self.lastFoundCoords = None


    def __init__(self, images: dict, fastModeEnabled: bool = True, attempts: int = 20) -> None:
        self.images = {}
        self.fastMode = False
        self.fastModeEnabled = fastModeEnabled
        self.attemptsPerImage = attempts
        self.screenWidth, self.screenHeight = pyautogui.size()
        pyautogui.FAILSAFE = False
        pyautogui.MINIMUM_DURATION = 0
        for imgName, imgPath in images.items():
            self.images[imgName] = self.Image(imgName, imgPath)
            

    def enableBallTexture(self):
        startTime = time.perf_counter()
        pyautogui.sleep(.4)
        pyautogui.move(50, 50)
        try:
            if self.fastModeEnabled and self.fastMode:
                success = self.autoclickFastMode(startTime)
                if not success: 
                    print('fast mode failed :(\n')
                    self.clearLocatedImageData()
                    self.cleanUpFailedJob(startTime)
            else:
                self.autoclickRegular(startTime)
        except Exception as e:
            print('Error:', e)

        # to prevent RL from getting stuck in KBM input mode, which lowers FPS (left clicking mouse seems to get it unstuck for some reason?)
        pyautogui.move(10, 10)
        pyautogui.leftClick(duration=.1)


    def autoclickRegular(self, startTime: float):
        # find and click 'disable safe mode' button
        dsmCoords = self.clickImage(self.images['disableSafeMode'].path, region=self.getSearchRegion('disableSafeMode'))
        if dsmCoords:
            pyautogui.sleep(.2)
            # find and click cosmetics tab
            cosmeticsTabCoords = self.clickImage(self.images['cosmeticsTab'].path, confidence=0.8, region=self.getSearchRegion('cosmeticsTab', dsmCoords))
            if cosmeticsTabCoords:
                # find and click ball texture dropdown
                dropdownCoords = self.clickImage(self.images['ballTextureDropdown'].path, region=self.getSearchRegion('ballTextureDropdown', cosmeticsTabCoords))
                if dropdownCoords:
                    # find and click ball texture
                    ballSelectionCoords = self.clickImage(self.images['ballSelection'].path, grayscale=False, region=self.getSearchRegion('ballSelection', dropdownCoords))
                    if ballSelectionCoords:
                        # find and click 'x' button to exit
                        xButtonCoords = self.clickImage(self.images['xButton'].path, region=self.getSearchRegion('xButton', ballSelectionCoords))
                        if xButtonCoords:
                            # save button coordinates
                            self.images['disableSafeMode'].lastFoundCoords = dsmCoords
                            self.images['cosmeticsTab'].lastFoundCoords = cosmeticsTabCoords
                            self.images['ballTextureDropdown'].lastFoundCoords = dropdownCoords
                            self.images['ballSelection'].lastFoundCoords = ballSelectionCoords
                            self.images['xButton'].lastFoundCoords = xButtonCoords

                            self.fineTuneSearchRegions()
                            self.fastMode = True
                            print(f'\n<<<<<  Enabled ball texture in {round((time.perf_counter() - startTime), 2)}s  >>>>>\n')
    

    def autoclickFastMode(self, startTime: float) -> bool:
        dsmButtonClicked = self.clickImage(self.images['disableSafeMode'].path, region=self.getSearchRegion('disableSafeMode'))
        if dsmButtonClicked:
            pyautogui.sleep(.2)
            self.clickCoord(self.images['cosmeticsTab'].lastFoundCoords)
            self.clickCoord(self.images['ballTextureDropdown'].lastFoundCoords)
            self.clickCoord(self.images['ballSelection'].lastFoundCoords)
            self.clickCoord(self.images['xButton'].lastFoundCoords)
            endTime = time.perf_counter() - startTime

            # check work by searching for first and last buttons on screen (disable safe mode & x)
            pyautogui.move(50, 50)
            if self.searchForImage(self.images['disableSafeMode'].path):
                return False
            for _ in range(2):      # 2 passes to weed out any chance of opencv error of not finding xButton when it's actually there
                xButtonOnScreen = self.searchForImage(self.images['xButton'].path)
                if xButtonOnScreen:
                    return False
                pyautogui.sleep(.1)

            print(f'\n<<<<<  Enabled ball texture in {round((endTime), 2)}s  (fast mode)  >>>>>\n')
            return True


    def getSearchRegion(self, imageName, prevImageCoords=None):
        if self.images[imageName].searchRegion:
            return self.images[imageName].searchRegion
        else:
            if prevImageCoords:
                return self.getRelativeSearchRegion(imageName, prevImageCoords)
            else: 
                return None


    def fineTuneSearchRegions(self):
        for img in self.images.values():
            if img.lastFoundCoords:
                img.searchRegion = self.checkWithinScreenBounds((img.lastFoundCoords[0] - img.width, img.lastFoundCoords[1] - img.height, img.width * 2, img.height * 2))


    def clearLocatedImageData(self):
        self.fastMode = False
        for img in self.images.values():
            img.lastFoundCoords = None
            img.searchRegion = None

    
    def cleanUpFailedJob(self, startTime: float):
        foundImage = self.findWhereLeftOff()
        if foundImage:
            clickedCoords = None
            for imageName, imageObj in self.images.items():
                if (imageName == foundImage["name"]) or clickedCoords:
                    try:
                        clickedCoords = self.clickImage(imageObj.path)
                        if imageName == 'disableSafeMode':
                            pyautogui.sleep(.2)
                    except Exception as e:
                        print(e)
            print(f'\n<<<<<  Enabled ball texture in {round((time.perf_counter() - startTime), 2)}s  (fast mode failed... probably bc position/size of AlphaConsole menu changed)  >>>>>\n')
            print('(if you didn\'t touch the AlphaConole menu, consider changing \'enableAutoclickerFastMode\' to False in your script to avoid future issues)\n')
        else:
            print("\nAutoclicker didn\'t finish successfully :(\n")
    
    def findWhereLeftOff(self):
        for imageName, imageObj in self.images.items():
            try:
                coords = pyautogui.locateCenterOnScreen(imageObj.path, confidence=.9, grayscale=True)
                return {"coords": coords, "name": imageName}
            except pyautogui.ImageNotFoundException:
                continue
        return None
    

    # checks if image is on found screen... if yes, returns Point tuple.. if not, returns False
    def searchForImage(self, image, confidence=.8, grayscale=True, region=None):
        try:
            point = pyautogui.locateCenterOnScreen(image, confidence=confidence, grayscale=grayscale, region=region)
            return point
        except pyautogui.ImageNotFoundException:
            return False


    def clickImage(self, image: str, confidence: float = 0.9, grayscale: bool = True, region=None, clickDuration=None):
        lastResort = round(0.1 * self.attemptsPerImage)     # last resort will kick in after 10% of attempts have failed
        for i in range(self.attemptsPerImage):
            attempt = i + 1
            try:
                imageCoords = pyautogui.locateCenterOnScreen(image, confidence=confidence, grayscale=grayscale, region=region)
                pyautogui.mouseDown(imageCoords[0], imageCoords[1])
                if clickDuration:
                    pyautogui.sleep(clickDuration)
                pyautogui.mouseUp()
                return imageCoords
            except pyautogui.ImageNotFoundException:
                imageName = image.split('/')[1]     # used specifically for image file paths declared in main script ... this line should change if those filepaths change
                if (attempt < lastResort and attempt < self.attemptsPerImage):    # if last resort isn't active
                    if not region:
                        print(f'\n[attempt {attempt}] ... couldn\'t find "{imageName}" by searching entire screen (slower)')
                    else:
                        print(f'\n[attempt {attempt}] ... couldn\'t find "{imageName}" in region {region}')
                elif (attempt == lastResort and attempt < self.attemptsPerImage):     # if should activate last resort (disable region)
                    if not region:
                        print(f'\n[attempt {attempt}] ... couldn\'t find "{imageName}" by searching entire screen (slower)')
                    else:
                        print(f'\n[attempt {attempt}] ... couldn\'t find "{imageName}" in region {region}')
                        region = None
                elif (attempt > lastResort and attempt < self.attemptsPerImage):    # if last resort is active
                    print(f'\n[attempt {attempt}] ... couldn\'t find "{imageName}" by searching entire screen (slower)')
                else:       # after last attempt
                    print(f'\n[attempt {attempt}] couldn\'t locate "{imageName}" on screen :(')
                    print(f'\nCheck this guide for a potential fix:\nhttps://github.com/smallest-cock/RL-Custom-Quickchat/blob/main/Troubleshooting.md\n')
            except Exception as e:
                print(e)
            pyautogui.sleep(.1)
    

    def clickCoord(self, coordTuple, clickDuration=None):
        pyautogui.mouseDown(coordTuple[0], coordTuple[1])
        if clickDuration:
            pyautogui.sleep(clickDuration)
        pyautogui.mouseUp()


    def getRelativeSearchRegion(self, image, prevImageCoords):
        match image:
            case 'cosmeticsTab':
                region = (0, prevImageCoords[1] - 175, self.screenWidth, 150)
                return region if self.checkWithinScreenBounds(region) else None
            case 'ballTextureDropdown':
                region = (0, prevImageCoords[1] + 100, self.screenWidth, 250)
                return region if self.checkWithinScreenBounds(region) else None
            case 'ballSelection':
                region = (0, prevImageCoords[1] + 15, self.screenWidth, 275)
                return region if self.checkWithinScreenBounds(region) else None
            case 'xButton':
                region = (0, prevImageCoords[1] - 250, self.screenWidth, 150)
                return region if self.checkWithinScreenBounds(region) else None


    def checkWithinScreenBounds(self, regionTuple):     # <--- regionTuple has the format: (topLeftX, topLeftY, width, height)
            xValid = ((regionTuple[0] >= 0) and (regionTuple[0] <= self.screenWidth)) and ((regionTuple[0] + regionTuple[2] >= 0) and (regionTuple[0] + regionTuple[2] <= self.screenWidth))
            yValid = ((regionTuple[1] >= 0) and (regionTuple[1] <= self.screenHeight)) and ((regionTuple[1] + regionTuple[3] >= 0) and (regionTuple[1] + regionTuple[3] <= self.screenHeight))
            return regionTuple if xValid and yValid else None
                

    def toggleFastMode(self):
        self.fastModeEnabled = not self.fastModeEnabled
        print(f'-------- autoclicker fast mode toggled {"on" if self.fastModeEnabled else "off"} --------\n')
           


# ------------------------------------------  LobbyInfo class  ---------------------------------------------------------------------------- 


class LobbyInfo():
    def __init__(self, folderPath: str) -> None:
        self.chatsJsonFile = folderPath + r"\Chats.json"
        self.ranksJsonFile = folderPath + r"\Ranks.json"

    def lastChat(self) -> str | None:
        try:
            with open(self.chatsJsonFile, encoding='utf8') as f:
                jsonData = json.load(f)
                return jsonData["chatMessages"][-1]["chat"]
        except IndexError:
            print(f"JSON file at '{self.chatsJsonFile}' has no chats ...")
        except Exception as e:
            print(e)

    def findLastChatterRanks(self) -> dict | None:
        try:
            # get last chatter name
            lastChatterName = None
            with open(self.chatsJsonFile, encoding='utf8') as f:
                jsonData = json.load(f)
                lastChatterName = jsonData["chatMessages"][-1]["playerName"]
        except IndexError:
            print(f"JSON file at '{self.chatsJsonFile}' has no chats ...")
            return
        except Exception as e:
            print(e)
            return
        try:
            # get last chatter ranks based on name
            lastChattersRanks = { 'name': lastChatterName }
            with open(self.ranksJsonFile, encoding='utf8') as g:
                jsonData = json.load(g)
                lastChattersRanks['ranks'] = jsonData['lobbyRanks'][lastChatterName]
        except KeyError:
            print(f"{lastChatterName} wasn't found in '{self.ranksJsonFile}'")
            return
        except Exception as e:
            print(e)
            return
        return lastChattersRanks

    def blastRanks(self) -> str | None:
        ranksDict = self.findLastChatterRanks()
        if not ranksDict:
            return

        # filter out playlists that haven't been played this season
        def getRankStr(rankDictForPlaylist: dict):
            matchesPlayed = rankDictForPlaylist['matches']
            tier = rankDictForPlaylist['rank']['tier']
            div = rankDictForPlaylist['rank']['div']
            if (matchesPlayed == 0) or (tier == 'n/a') or (div == 'n/a'):
                return '--'
            return f'{tier}..div{div}'
    
        return (f'''{ranksDict["name"]}: [1s] {getRankStr(ranksDict["ranks"]["1v1"])} \
[2s] {getRankStr(ranksDict["ranks"]["2v2"])} \
[3s] {getRankStr(ranksDict["ranks"]["3v3"])}''')

    def blastRank(self, playlist: str) -> str | None:
        ranksDict = self.findLastChatterRanks()      
        if not ranksDict:
            return
        try:
            matches = ranksDict['ranks'][playlist]['matches']
            if playlist != 'casual':
                tier = ranksDict['ranks'][playlist]['rank']['tier']
                div = ranksDict['ranks'][playlist]['rank']['div']
                if (tier != 'n/a') and (div != 'n/a'):
                    if matches != 0:
                        return f'{ranksDict["name"]} [{playlist}] ** {tier} div{div} ** ({matches} matches)'
                    else:
                        return f'{ranksDict["name"]} [{playlist}] ** {tier} div{div} ** (prev season MMR)'
                else:
                    return f'{ranksDict["name"]} [{playlist}] ** doesnt play ** ({matches} matches)'
            else:
                return f'{ranksDict["name"]} [{playlist}] ** {matches} matches played **'
        except Exception as e:
            print("blastRank error:", e)



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
    