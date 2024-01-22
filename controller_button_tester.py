import pygame

pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

for controller in joysticks:
    if controller.get_init():
        print(f"\n\n~~~~~~ {controller.get_name()} detected ~~~~~~\n\npress a button to get the input value....\n\n")

while True:
    try:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                print(f'button value: {event.button}')
            if event.type == pygame.JOYHATMOTION:
                if not event.value == (0, 0):
                    print(f'hat value: {event.value}')
    except Exception as e:
        print(e)
