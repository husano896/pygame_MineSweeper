import sys
sys.path.insert(0,'./System')
sys.path.insert(0,'./Scene')

import os
os.environ['SDL_VIDEO_CENTERED'] = '1'

from Game_System import *
from pygame.locals import *
from Scene.Intro import Scene_Intro

#Game name
GAMENAME = "MMMineSweeper"

startup_Scene = Scene_Intro()
frame = 0

#Add support for console if needed (experiment)
#import Game_Console
import Game_Debug

def showFPS():
    global FPSCLOCK
    pygame.display.set_caption("%s (%d)" % (GAMENAME, int(FPSCLOCK.get_fps())))

def main():
    global FPSCLOCK, sleeping
    FPSCLOCK = pygame.time.Clock()
    cur_x, cur_y = 0, 0

    pygame.pgSys.ChangeScene(startup_Scene)
    sleeping = False
    
    while True:

        if (pygame.pgSys.Handle_Events_InMain):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    break
                    
                if (SDL2):
                    if event.type == pygame.APP_WILLENTERBACKGROUND:
                        sleeping = True
                    #App is awake from background, reinit the display
                    elif event.type == pygame.APP_DIDENTERFOREGROUND:
                        sleeping = False
                        pygame.pgSys.InitDisplay()

        if (not sleeping):
            if (pygame.pgSys.RenderEnabled):
                pygame.pgSys.Renderer.clear(pygame.pgSys.BGColor)
            else:
                pygame.pgSys.Screen.fill(pygame.pgSys.BGColor)

            if (pygame.pgSys.Scene):
                pygame.pgSys.Scene.update()
                pygame.pgSys.Scene.graphicsUpdate()
            
            showFPS()
            
            if (pygame.pgSys.RenderEnabled):
                pygame.pgSys.Renderer.render_present()
            else:
                pygame.display.flip()
            
        FPSCLOCK.tick(FPS)
        
if __name__ == '__main__':
    main()
