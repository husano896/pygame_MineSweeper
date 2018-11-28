from Scene.__Base__ import __Base__
from Game_System import *
class Scene_Changer(__Base__):

    def __init__(self, newscene, speed = 8):
        self.frame = 0
        self.speed = speed
        self.Img_LastScene = pygame.pgSys.Screen.copy()
        
        newscene.update()
        self.Img_NewScene = pygame.pgSys.Screen.copy()
        
        self.new_scene = newscene

        self.new_scene.onChange()
        
        pygame.pgSys.Scene = self
        
    def update(self):
        
        self.Img_NewScene.set_alpha(self.frame)

        pygame.pgSys.Screen.blit(self.Img_LastScene, (0,0))
        pygame.pgSys.Screen.blit(self.Img_NewScene, (0,0))
        self.frame+=self.speed
        
        if (self.frame >= 256):
            self.new_scene.onChangeDone()
            pygame.pgSys.Scene = self.new_scene
