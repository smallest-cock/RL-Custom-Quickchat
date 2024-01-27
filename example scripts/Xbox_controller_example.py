import os
import pygame
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

enableAutoclickerFastMode = True
autoclickAttemptsPerImage = 20

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

# Xbox 360 controller button mappings for pygame.... these may change if using a different controller (refer to https://www.pygame.org/docs/ref/joystick.html)
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

# --------------------------------------------------------------------------------------------------------

data = {
    "variations": variations,
    "typingDelay": typingDelay,
    "chatSpamInterval": chatSpamInterval,
    "timeWindow": macroTimeWindow,
    "autoclickerImages": autoclickerImages,
    "enableAutoclickerFastMode": enableAutoclickerFastMode,
    "autoclickAttemptsPerImage": autoclickAttemptsPerImage,
    "buttons": buttons,
    "chatKeys": chatKeys
}

syncData(data)
shuffleVariations()

# change working directory to script directory (so .png files are easily located)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()
clock = pygame.time.Clock()

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
                numHatsOnController = controller.get_numhats()
                updateController(controller, numHatsOnController)
                print("\nController hats:", numHatsOnController)     # easy way to determine if buttons dict needs tuple values
                if controller.get_init():
                    print(f"\n\n~~~~~~ {controller.get_name()} detected ~~~~~~\n\nwaiting for quickchat inputs....\n\n")
            elif (event.type == pygame.JOYBUTTONDOWN) or (event.type == pygame.JOYHATMOTION):
                updatePressedButtons(getAllButtonsPressed())



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    Edit the code below to change quickchats, macros, spam amounts, chat modes, variations, etc.    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



                toggleMacros('back') # <-- 'back' is the button used to toggle on/off macros (Xbox back button)..... change as you please

                if macrosAreOn():
                    
                    # on X + up + RB, types "noice"
                    if combine('x', 'up', 'RB'):    # <--- combine(...) can take any amount of buttons :)
                        quickchat('noice')
                        break
                        
                    # on up → left, types "let me cook"
                    elif sequence('up', 'left'):    # <--- sequence(...) can only take 2 buttons!
                        quickchat('let me cook')
                        break
                    
                    # on X + left, types "dont lose this kickoff" (spamming 2 times)
                    elif combine('x', 'left'):
                        quickchat('dont lose this kickoff', spamCount=2)  # <-- the '2' is how many times the chat will be spammed.. the max you can put is 3 (before RL gives a chat timeout)
                        break
                    
                    # on B + X, types "tell me how you really feel..." (using team chat)
                    elif combine('b', 'x'):
                        quickchat('tell me how you really feel...', chatMode='team')
                        break
                    
                    # on A → B, types "im lagging" (using team chat, spamming 3 times)
                    elif sequence('a', 'b'):
                        quickchat('im lagging', chatMode='team', spamCount=3)
                        break
                    
                    # on up → right, types "im gay" (using party chat)
                    elif sequence('up', 'right'):
                        quickchat('im gay', chatMode='party')
                        break

                    # on left → left, types "Word variations are [compliment]!"  ..... where [compliment] is a random word from the 'compliment' variations list above
                    elif sequence('left', 'left'):
                        quickchat(f'Word variations are {variation("compliment")}!')    # <-- One way to include word variations in your chats (notice the 'f' at the beginning of the string)
                        break

                    # on down → left, types "ok [foe]!!!"  ..... where [foe] is a random word from the 'foe' variations list above
                    elif sequence('down', 'left'):
                        quickchat('ok ' + variation('foe') + '!!!')    # <-- Another way to format word variations in your chats
                        break
                    
                    # on LB + up + X, types "Wassup [friend]! Nice to see you again."
                    elif combine('LB', 'up', 'x'):                              # <---- combine(...) can take any number of buttons :)
                        quickchat('Wassup %s! Nice to see you again.' % variation('friend'))    # <-- Yet another way to format word variations in your chats
                        break
                    
                    # on down → up, types a random cat fact (from the list of 'cat fact' variations above)
                    elif sequence('down', 'up'):
                        quickchat(variation('cat fact'))
                        break

                    # on A + up, starts listening for speech-to-text (lobby chat)
                    elif combine('a', 'up'): 
                        quickchat(speechToText())
                        break
                    
                    # on A + left, starts listening for speech-to-text (team chat)
                    elif combine('a', 'left'): 
                        quickchat(speechToText(), chatMode='team')
                        break

                    elif combine('y', 'left'):
                        enableBallTexture()     # <--- autoclick things in AlphaConsole menu to enable ball texture
                        break


    except Exception as e:
        print(e)
        break

    # limit pygame refresh rate to "25 FPS" ... reduces CPU usage :)
    clock.tick(25)