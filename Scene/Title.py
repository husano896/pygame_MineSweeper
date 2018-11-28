from Game_System import *
from Scene.__Base__ import __Base__

class Scene_Title(__Base__):
    
    def __init__(self):
        if (pygame.pgSys.SDL2):
            #Old Font
            img1 = pygame.pgSys.Font.render("Hello pygame!", 1, (255,255,255), (0,0,0))
        else:
            img1 = pygame.pgSys.Font.render("Hello pygame!", (255,255,255))[0]
        if (pygame.pgSys.RenderEnabled):
            self.Image1 = pygame.render.Sprite(pygame.pgSys.Renderer.load_texture(img1))
        else:
            self.Image1 = img1

        self.Image1_rect = img1.get_rect()
    def onChange(self):
        pass

    def onChangeDone(self):
        pass
    
    def update(self):
        pass

    def graphicsUpdate(self):
        pos = (pygame.pgSys.WINDOWWIDTH/2 - self.Image1_rect.w/2,pygame.pgSys.WINDOWHEIGHT/2 - self.Image1_rect.h/2)
        if (pygame.pgSys.RenderEnabled):
            self.Image1.render(pos)
        else:
            pygame.pgSys.Screen.blit(self.Image1,pos)
