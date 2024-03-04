import os
from functions import *



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    Go to the "edit" section below to edit quickchats, macros, etc.    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# Create your own word variations and format them like this (see examples on how to use them in the "edit" section below)
variations = {
    'friend': ['homie', 'blood', 'cuh', 'dawg', 'my guy', 'my man', 'my dude', 'comrade', 'playa', 'fellow gamer', 'brother', 'bro', 'bruh', 'buddy', 'blud', 'fellow human', 'foo', 'lad', 'broski', 'mate', 'fam', 'bby'],
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
autoclickerImages = {
    "disableSafeMode": 'autoclicker images/dsm.png',
    "cosmeticsTab": 'autoclicker images/cosmetics_tab.png',
    "ballTextureDropdown": 'autoclicker images/ball_texture_dropdown.png',
    "ballSelection": 'autoclicker images/ball_selection.png',
    "xButton": 'autoclicker images/x.png'
}

# Your 'Lobby Info' folder path (found in your bakkesmod data folder)... created when you install the 'Lobby Info' plugin here: https://github.com/smallest-cock/LobbyInfo/releases/tag/latest
lobbyInfoFolderPath = r'C:\Users\<your user account name here>\AppData\Roaming\bakkesmod\bakkesmod\data\Lobby Info'   # <---- edit <your user account name here>

speechToTextEnabled = True

enableAutoclickerFastMode = True
autoclickAttemptsPerImage = 20

# Adjusts chat typing speed (seconds per character)
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

# PS4 controller button mappings for pygame... these may change if using a different controller (refer to https://www.pygame.org/docs/ref/joystick.html#playstation-4-controller-pygame-2-x)
buttons = {
    'x': 0,
    'circle': 1,
    'square': 2,
    'triangle': 3,
    'share': 4, 
    'ps': 5,
    'options': 6,
    'left stick': 7,
    'right stick': 8,
    'L1': 9,
    'R1': 10,
    'up': 11, 
    'down': 12, 
    'left': 13, 
    'right': 14,
    'touchpad': 15
}


# ----------------------------------  only touch this stuff if you know what you're doing  -----------------------------------------

# change working directory to script directory (so .png files are easily located)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

lobbyInfo = LobbyInfo(lobbyInfoFolderPath)
controller = Controller(buttons, macroTimeWindow)
autoclicker = Autoclicker(autoclickerImages, enableAutoclickerFastMode, autoclickAttemptsPerImage)
chat = Chat(chatKeys, typingDelay, chatSpamInterval, speechToTextEnabled, variations)
chat.shuffleVariations()
syncData(autoclicker=autoclicker, lobbyInfo=lobbyInfo, chat=chat, controller=controller)

while True:
    try:
        event = controller.getPygameEvent()
        isButtonEvent = controller.handlePygameEvent(event)
        if isButtonEvent:



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    Edit the code below to change quickchats, macros, spam amounts, chat modes, variations, etc.    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


                
            toggleMacros('ps') # <-- 'ps' is the button used to toggle on/off macros (PlayStation button)..... change as you please

            if controller.macrosOn:

                # on square + up + R1, types "noice"
                if combine('square', 'up', 'R1'):   # <--- combine(...) can take any amount of buttons :)
                    quickchat('noice')
                    continue
                
                # on up → left, types "let me cook"
                elif sequence('up', 'left'):        # <--- sequence(...) can only take 2 buttons!
                    quickchat('let me cook')
                    continue

                # on square + left, types "dont lose this kickoff" (spamming 2 times)
                elif combine('square', 'left'):
                    quickchat('dont lose this kickoff', spamCount=2)  # <-- the '2' is how many times the chat will be spammed.. the max you can put is 3 (before RL gives a chat timeout)
                    continue
                
                # on circle + up, types "tell me how you really feel..." (using team chat)
                elif combine('circle', 'up'):
                    quickchat('tell me how you really feel...', chatMode='team')
                    continue
                
                # on x → circle, types "im lagging" (using team chat, spamming 3 times)
                elif sequence('x', 'circle'):
                    quickchat('im lagging', chatMode='team', spamCount=3)
                    continue
                
                # on left → left, types "im gay" (using party chat)
                elif sequence('left', 'left'):
                    quickchat('im gay', chatMode='party')
                    continue

                # on down → left, types "Word variations are [compliment]!" ... where [compliment] is a random word from the 'compliment' variations list above
                elif sequence('down', 'left'):
                    quickchat(f'Word variations are {variation("compliment")}!')    # <-- One way to include word variations in your chats (notice the 'f' at the beginning of the string)
                    continue

                # on L1 + up + square, types "ok [foe]!!!" ... where [foe] is a random word from the 'foe' variations list above
                elif combine('L1', 'up', 'square'):
                    quickchat('ok ' + variation('foe') + '!!!')    # <-- Another way to format word variations in your chats
                    continue
                
                # on L1 + right, types "Wassup [friend]! Nice to see you again."
                elif combine('L1', 'right'):
                    quickchat('Wassup %s! Nice to see you again.' % variation('friend'))    # <-- Yet another way to format word variations in your chats
                    continue
                
                # on down → up, types a random cat fact (from the list of 'cat fact' variations above)
                elif sequence('down', 'up'):
                    quickchat(variation('cat fact'))
                    continue
                    
                # on x + up, starts listening for speech-to-text (lobby chat)
                elif combine('x', 'up'): 
                    quickchat(speechToText())
                    continue
                
                # on x + left, starts listening for speech-to-text (team chat)
                elif combine('x', 'left'): 
                    quickchat(speechToText(), chatMode='team')
                    continue
                
                elif combine('triangle', 'left'):
                    enableBallTexture()     # <--- autoclick things in AlphaConsole menu to enable ball texture
                    continue
                

    # --------  to use the features below: install the 'Lobby Info' bakkesmod plugin (see above) & edit 'lobbyInfoFolderPath' appropriately (see above)  ---------


                # expose the last chatter's ranks
                elif combine('touchpad'):
                    quickchat(blastRanks())
                    continue
                
                # expose last chatter's 2v2 rank and # of games played this season
                elif sequence('right', 'right'):
                    quickchat(blastRank('2v2'))     # <----- can also use '1v1', '3v3' or 'casual'
                    continue
                
                # repeat the last chat aS sArCAsM tExT
                elif sequence('right', 'down'):
                    quickchat(lastChat(), sarcasm=True)
                    continue
                
                # repeat the last chat "as a quote" - sweaty gamer
                elif sequence('right', 'up'):
                    quickchat(lastChat(), quotedAs='sweaty gamer')
                    continue


    except Exception as e:
        print(e)
        continue