import time
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
    for i in range(spamCount):
        pyautogui.press(chatKeys[chatMode])
        pyautogui.write(thing, interval=typingDelay)
        pyautogui.press('enter')
        print(f'[{chatMode}]    {thing}\n')
        time.sleep(chatSpamInterval)

def toggleMacros(button):
    if keyboard.is_pressed(button):
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
    with microphone as source:
        # r.adjust_for_ambient_noise(source)
        print('speak now...\n')
        audio = r.listen(source, timeout=5)
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
    return response['transcription'].lower()
        
shuffledVariations = variations.copy()
shuffleVariations()

print(f"\n\n~~~~~~~~~~~~~~ KBM version ~~~~~~~~~~~~~~\n\nwaiting for quickchat inputs....\n\n")

# speech recognition init
r = sr.Recognizer()
mic = sr.Microphone()
with mic as source:
    r.adjust_for_ambient_noise(source) # <--- adjusts mic sensitvity for background noise based on a 1s sample of mic audio

while True:
    try:



# ---------------------------------    Edit the code below to change quickchats, macros, spam amounts, chat modes, variations, etc.    --------------------------------------------------



        toggleMacros('home')

        if macrosOn:

            # When r + 4 is pressed, types "I pressed R and 4 at the same time."
            if press('r+4'):
                quickchat('I pressed R and 4 at the same time.')
                continue
    
            # When ctrl is pressed, types "I just pressed the control button" (spamming 2 times)
            elif press('ctrl'):
                quickchat('I just pressed the control button', spamCount=2)
                continue
                        
            # When shift + up is pressed, types "I just pressed shift + up" (in team chat)
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

            # When delete is pressed, types a random cat fact from the 'cat fact' variation list above
            elif press('delete'):
                quickchat(variation('cat fact'))
                continue

            # on ctrl + up, starts listening for speech-to-text (lobby chat)
            elif press('ctrl+up'):
                quickchat(speechToText(mic))
                break
              
            # on ctrl + left, starts listening for speech-to-text (team chat)
            elif press('ctrl+left'): 
                quickchat(speechToText(mic), chatMode='team')
                break
        

    except Exception as e:
        print(e)
        break
