from Game_System import *
from Scene.__Base__ import __Base__
from Scene.Title import Scene_Title
from Scene.GamePlay import Scene_GamePlay
class Scene_Intro(__Base__):
    
    def __init__(self):
        
        img1 = pygame.pgSys.Font.render("xFly Studio", 0, (255,255,255), (0,0,0))
            
        if (pygame.pgSys.RenderEnabled):
            self.Image1 = pygame.render.Sprite(pygame.pgSys.Renderer.load_texture(img1))
        else:
            self.Image1 = img1

        self.Image1_rect = img1.get_rect()
        self.frame = 0
        
    def onChange(self):
        pass

    def onChangeDone(self):
        pass
    
    def update(self):
        
        self.frame += 1
        #Change scene after 384 frames
        if (self.frame > 384):
            pygame.pgSys.ChangeScene(Scene_GamePlay())
            return

        #Here shows how a simple "anim like" text works
        if (self.frame > 255):
            alpha = max(0, 767-int(self.frame*2))
        else:
            alpha = min(int(self.frame*2), 255)

        if (pygame.pgSys.RenderEnabled):
            self.Image1.alpha = alpha
        else:
            self.Image1.set_alpha(alpha)

    def graphicsUpdate(self):
        pos = (pygame.pgSys.WINDOWWIDTH/2 - self.Image1_rect.w/2,pygame.pgSys.WINDOWHEIGHT/2 - self.Image1_rect.h/2)
        if (pygame.pgSys.RenderEnabled):
            self.Image1.render(pos)
        else:
            pygame.pgSys.Screen.blit(self.Image1,pos)
