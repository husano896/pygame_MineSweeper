import pygame
cache_ImgDebugInfo = None

def showDebugInfo():
    global cache_ImgDebugInfo

    if (cache_ImgDebugInfo == None):
        SDLVersion = pygame.get_sdl_version()    
        surf = pygame.Surface((400, 120), pygame.HWSURFACE | pygame.SRCALPHA)
        if (pygame.pgSys.SDL2):
            #Old Font
            img1 = pygame.pgSys.Font.render("pygame version : %s" % pygame.version.ver, 1, (255,255,255))
            img2 = pygame.pgSys.Font.render("SDL version : %d.%d.%d" % (SDLVersion[0], SDLVersion[1], SDLVersion[2]), 1, (255,255,255))
            img3 = pygame.pgSys.Font.render("RendererEnabled : %s" % (pygame.pgSys.RenderEnabled), 1, (255,255,255))
        else:
            #FreeType
            img1 = pygame.pgSys.Font.render("pygame version : %s" % pygame.version.ver, (255,255,255))[0]
            img2 = pygame.pgSys.Font.render("SDL version : %d.%d.%d" % (SDLVersion[0], SDLVersion[1], SDLVersion[2]), (255,255,255))[0]
            img3 = pygame.pgSys.Font.render("RendererEnabled : %s" % (pygame.pgSys.RenderEnabled), (255,255,255))[0]            
        surf.blit(img1, (surf.get_width() - img1.get_width(),0))
        surf.blit(img2, (surf.get_width() - img2.get_width(),img1.get_height()+6))
        surf.blit(img3, (surf.get_width() - img3.get_width(),img1.get_height()+img2.get_height()+12))
        
        if (pygame.pgSys.RenderEnabled):
            cache_ImgDebugInfo = pygame.render.Sprite(pygame.pgSys.Renderer.load_texture(surf))
        else:
            cache_ImgDebugInfo = surf

    if (pygame.pgSys.RenderEnabled):
        cache_ImgDebugInfo.render((400,0))
    else:
        pygame.pgSys.Screen.blit(cache_ImgDebugInfo,(400,0))
