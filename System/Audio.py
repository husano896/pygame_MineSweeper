import pygame

####https://www.pygame.org/docs/ref/music.html

def init():
    result = True
    try:
        pygame.mixer.pre_init(44100, 16, 2, 2048)
        pygame.mixer.init()
    except Exception as e:
        result = False
        print(e)
    try:
        pygame.mixer.quit()
        pygame.mixer.init(44100, 16, 2, 2048)
    except Exception as e:
        result = False
        print(e)
    if (result):
        print("Successfully initalized mixer.")

def loadBGM(filename):
    if (not pygame.mixer.get_init()):
        return

    pygame.mixer.music.load(filename)
    
def playBGM(filename, loops=-1, pos=0.0, event=None):
    
    if (not pygame.mixer.get_init()):
        return

    pygame.mixer.music.load("Audio/BGM/%s" % filename)
        
    pygame.mixer.music.play(loops, pos)

    if (event != None):
        pygame.mixer.music.set_endevent(event)

def stopBGM():
    pygame.mixer.music.stop()
    pygame.mixer.music.set_endevent()

def fadeoutBGM(t):
    pygame.mixer.music.fadeout(t)

class Sound(pygame.mixer.Sound):

    def __init__(self, n):
        if (pygame.mixer.get_init()):
            super().__init__("Audio/SE/%s" % n)
        
    def play(self, loops=0, maxtime=0, fade_ms=0):
        if (pygame.mixer.get_init()):
            super().play(loops, maxtime, fade_ms)

    def stop(self):
        if (pygame.mixer.get_init()):
            super().stop()
