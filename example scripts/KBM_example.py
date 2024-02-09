import os
import keyboard
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

# Time interval between spammed chats (0.2 seconds).... change as you please
chatSpamInterval = .2

# Edit these if necessary
chatKeys = {
    'lobby': 't',
    'team': 'y',
    'party': 'u'
}


# ----------------------------------  only touch this stuff if you know what you're doing  -----------------------------------------

lobbyInfo = LobbyInfo(lobbyInfoFolderPath)
autoclicker = Autoclicker(autoclickerImages, enableAutoclickerFastMode, autoclickAttemptsPerImage)
chat = Chat(chatKeys, typingDelay, chatSpamInterval, speechToTextEnabled, variations)
chat.shuffleVariations()
syncData(autoclicker, lobbyInfo, chat)

# change working directory to script directory (so .png files are easily located)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print(f"\n\n~~~~~~~~~~~~~~ KBM version ~~~~~~~~~~~~~~\n\nwaiting for quickchat inputs....\n\n")

while True:

    # blocks loop until a keyboard event happens ... reduces CPU usage :)
    keyboard.read_key()
    
    try:



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    Edit the code below to change quickchats, macros, spam amounts, chat modes, variations, etc.    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



        # -------  Testing these macros via the terminal may cause the script to exit prematurely (due to auto typing), but wont happen if another app is in focus  -------
       

        toggleKbmMacros('home')

        if macrosAreOn():

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
                quickchat(speechToText())
                continue
              
            # When PgDn is pressed, starts listening for speech-to-text (team chat)
            elif press('pagedown'): 
                quickchat(speechToText(), chatMode='team')
                continue

            elif press('pageup'):
                enableBallTexture()         # <--- autoclick things in AlphaConsole menu to enable ball texture
                continue


    # --------  to use the features below: install the 'Lobby Info' bakkesmod plugin (see above) & edit 'lobbyInfoFolderPath' appropriately (see above)  ---------

            
            # expose the last chatter's ranks
            elif press('insert'):
                quickchat(blastRanks())
                continue
            
            # expose last chatter's 2v2 rank and # of games played this season
            elif press('alt+down'):
                quickchat(blastRank('2v2'))     # <----- can also use '1v1', '3v3' or 'casual'
                continue
            
            # repeat the last chat aS sArCAsM tExT
            elif press('backspace'):
                quickchat(lastChat(), sarcasm=True)
                continue
            
            # repeat the last chat "as a quote" - sweaty gamer
            elif press('k+7'):
                quickchat(lastChat(), quotedAs='sweaty gamer')
                continue


    except Exception as e:
        print(e)
        break