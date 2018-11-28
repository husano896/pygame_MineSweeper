#Customization for pygame_sdl2 feature
SDL2 = False
RenderEnabled = True and SDL2
FreeType = False
if (SDL2):
    try:
        import pygame_sdl2
        pygame_sdl2.import_as_pygame()
        import pygame.render
    except ImportError:
        print("pygame_sdl2 importing failed! Disabled SDL2")
        SDL2 = False
        RenderEnabled = False
        
import pygame
if (not SDL2):
    import pygame.freetype
import System.Audio
from Scene.__Changer__ import Scene_Changer
#### Initalize

#Framerate
FPS = 60

#Resolution
WINDOWWIDTH,WINDOWHEIGHT = 800, 600

class Game_System():
    def __init__(self):
        global SDL2, RenderEnabled
        pygame.init()
        
        self.WINDOWWIDTH, self.WINDOWHEIGHT = WINDOWWIDTH, WINDOWHEIGHT
        self.BGColor = (0, 0, 0)
        self.Screen = pygame.display.set_mode((self.WINDOWWIDTH,self.WINDOWHEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
        
        self.Scene = None
        self.Audio = System.Audio
        self.Audio.init()
        self.SDL2 = SDL2

        #New
        #if (SDL2):
            #Old
        self.Font = pygame.font.Font("Fonts/NotoSansCJKtc-Regular.otf", 14)
        #else:
        #    self.Font = pygame.freetype.Font("Fonts/NotoSansCJKtc-Regular.otf", 14)

        self.RenderEnabled = RenderEnabled
        self.Handle_Events_InMain = True
        
        if (SDL2):
            try:
                self.Renderer = pygame.render.Renderer(vsync=True)
            except ImportError:
                print("render importing failed!")
                self.RenderEnabled = False
                
    def ChangeScene(self, nextScene):
        self.Scene = Scene_Changer(nextScene)

    def InitDisplay(self):
        self.Screen = pygame.display.set_mode((self.WINDOWWIDTH,self.WINDOWHEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
        
#Inject into pygame
pygame.pgSys = Game_System()
