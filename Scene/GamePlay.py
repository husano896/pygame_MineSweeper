from Game_System import *
from Scene.__Base__ import __Base__
from Scene.Title import Scene_Title
import random
import time

class Scene_GamePlay(__Base__):
    
    def __init__(self):
            
        #if (pygame.pgSys.RenderEnabled):
        #else:

        #Box settings
        self.Box_Size = 30
        self.font = pygame.font.SysFont("Calibri", 24)
        self.Box_Border = 3
        self.Box_Size_Rect = (self.Box_Size, self.Box_Size)
        self.Box_Center_Rect = (self.Box_Border, self.Box_Border, self.Box_Size - self.Box_Border*2, self.Box_Size - self.Box_Border*2)

        #Field settings
        self.Field = [] #0~8 = minecount, 10 = mine
        self.FieldCovered = [] #0 = uncovered, 1 = covered, 2 = flagged
        self.FieldSize = (30,16)
        self.MineCount = 99
        self.BoxLeft = self.FieldSize[0]*self.FieldSize[1]


        #Colors based on windows version
        FontColors = [  [0, 0, 200]    ,[0 , 200, 0]  ,[200, 0, 0],
                        [200, 0, 200]  ,[200, 100, 50],[0, 200, 200],
                        [200, 200, 200],[100,100,100]
                     ]
        
        #Images Initalize
        self.Image_Uncovered_Items = []
        self.Image_Covered = pygame.Surface(self.Box_Size_Rect, pygame.HWSURFACE)
        self.Image_Pressed = pygame.Surface(self.Box_Size_Rect, pygame.HWSURFACE)
        self.Image_Marked = pygame.Surface(self.Box_Size_Rect, pygame.HWSURFACE)

        #For empty item and number 1~8
        for i in range(0,9):
            surf = pygame.Surface(self.Box_Size_Rect)
            surf.fill((127,127,127))
            #We don't need to draw number if no mine is around
            if (i > 0):
                img_number = self.font.render(str(i), 1, FontColors[i-1])
                surf.blit(img_number, ((self.Box_Size - img_number.get_width())/2,(self.Box_Size-img_number.get_height())/2 ))
            self.Image_Uncovered_Items.append(surf)

        #Image - Mine
        surf = pygame.Surface(self.Box_Size_Rect)
        surf.fill((127,0,0))
        mine = self.font.render("X", 1, (255,255,255))
        surf.blit(mine, ((self.Box_Size-mine.get_width())/2,(self.Box_Size-mine.get_height())/2))
        self.Image_Uncovered_Items.append(surf)

        #Image - Box
        self.Image_Covered.fill((127,127,127))
        self.Image_Covered.fill((192,192,192), pygame.Rect( (self.Box_Border,self.Box_Border), (self.Box_Size-self.Box_Border*2,self.Box_Size-self.Box_Border*2)))

        #Image - Box - Pressed
        self.Image_Pressed.fill((127,127,127))
        self.Image_Pressed.fill((64,64,64), pygame.Rect(5,5,10,10))

        #Image - Marked
        self.Image_Marked.fill((255,63,63))
        marked = self.font.render("!", 1, (255,255,255))
        self.Image_Marked.blit(marked, ((self.Box_Size-marked.get_width())/2,(self.Box_Size-marked.get_height())/2))

        #Image - PlayField
        field_rect = (self.FieldSize[0] * self.Box_Size , self.FieldSize[1] * self.Box_Size)
        self.Image_PlayField = pygame.Surface(field_rect, pygame.HWSURFACE)
        self.Image_PlayFieldCovered = pygame.Surface(field_rect, pygame.HWSURFACE | pygame.SRCALPHA)
        self.Image_PlayFieldGrid = pygame.Surface(field_rect, pygame.HWSURFACE | pygame.SRCALPHA)

        #Sound Effects
        self.Sound_FlagIn = pygame.pgSys.Audio.Sound("FlagIn.wav")
        self.Sound_FlagOut = pygame.pgSys.Audio.Sound("FlagOut.wav")
        self.Sound_Lose = pygame.pgSys.Audio.Sound("Lose.wav")
        self.Sound_Win = pygame.pgSys.Audio.Sound("Win.wav")
        self.Sound_WrongFlag = pygame.pgSys.Audio.Sound("Wrong.wav")

        #Background Musics
        self.BGM = ["BGM_1.ogg","BGM_2.ogg","BGM_3.ogg","BGM_5.ogg"]
        self.BGM_Sequence = random.randint(0, len(self.BGM))
        self.BGM_EVENT = pygame.USEREVENT + 2

        #Background Images
        self.Backgrounds = [ pygame.image.load("Graphics/Backgrounds/1.jpg").convert(), pygame.image.load("Graphics/Backgrounds/2.jpg").convert(),
                             pygame.image.load("Graphics/Backgrounds/3.jpg").convert(), pygame.image.load("Graphics/Backgrounds/4.jpg").convert() ]
        
        self.CurrentBackground = self.Backgrounds[random.randint(0, len(self.Backgrounds)-1)]
        
        #etc
        self.GameOver = False
        self.DoubleButton = False
        self.GameStart = False        

        #Game Stat
        self.StartTime = 0
        self.EndTime = 0
        
        #Field Initalize
        self.Field_Initalize()

    def playBGM(self):
        #Randomly pick a background
        self.CurrentBackground = self.Backgrounds[random.randint(0, len(self.Backgrounds)-1)]

        #Play BGM by sequence
        if (len(self.BGM) > 0):
            self.BGM_Sequence = (self.BGM_Sequence+1)%len(self.BGM)
            pygame.pgSys.Audio.playBGM(self.BGM[self.BGM_Sequence], 0, 0.0, self.BGM_EVENT)
            
    def borderCheck(self, x, y, x_offset, y_offset):
        
        if (x_offset == 0 and y_offset == 0):
            return True
        if (x + x_offset < 0 or x + x_offset >= self.FieldSize[0] or y + y_offset < 0 or y + y_offset >= self.FieldSize[1]):
            return True

        return False
    
    def Field_Initalize(self, pos = None):
        #Reset list everytime incase of field size change
        #I don't even know lists can work like this
        self.Field = [[0 for w in range(self.FieldSize[0])] for h in range(self.FieldSize[1])]
        self.FieldCovered = [[1 for w in range(self.FieldSize[0])] for h in range(self.FieldSize[1])]
        self.GameStart = False
        self.BoxLeft = self.FieldSize[0]*self.FieldSize[1]

        #Setup mines
        i = self.MineCount
        while (i > 0):
            x, y = random.randint(0, self.FieldSize[0]-1), random.randint(0, self.FieldSize[1]-1)
            if (not self.Field[y][x]):
                if (pos == None or (pos != (x,y))):
                    self.Field[y][x] = 10
                    i -=1

        #Draw base playfield
        self.Image_PlayField.fill((0,0,0))
        for y in range(self.FieldSize[1]):
            for x in range(self.FieldSize[0]):
                rect_pos = (x*self.Box_Size, y*self.Box_Size)
                if (self.Field[y][x] == 10):
                    #Draw mine
                    self.Image_PlayField.blit(self.Image_Uncovered_Items[9], rect_pos)
                else:
                    #Count mine around
                    mineRound = 0
                    
                    for y_offset in range(-1,2):
                        for x_offset in range(-1,2):
                            
                            if (self.borderCheck(x,y,x_offset,y_offset)):
                                continue
                            
                            if (self.Field[y + y_offset][x + x_offset] == 10):
                                mineRound += 1
                                
                    self.Image_PlayField.blit(self.Image_Uncovered_Items[mineRound], rect_pos)
                    self.Field[y][x] = mineRound

                #Draw mine count
                self.Image_PlayFieldCovered.blit(self.Image_Covered, rect_pos)

        #Draw grid
        for y in range(self.FieldSize[1]):
            pygame.draw.line(self.Image_PlayFieldGrid, (0,0,0), (0, y*self.Box_Size), (self.FieldSize[0]*self.Box_Size, y*self.Box_Size))
        for x in range(self.FieldSize[0]):
            pygame.draw.line(self.Image_PlayFieldGrid, (0,0,0), (x*self.Box_Size, 0), (x*self.Box_Size, self.FieldSize[0]*self.Box_Size))

    def OpenEmptySpaces(self, x, y):
      
        #Open
        if (self.FieldCovered[y][x] == 0):
            return

        self.Image_PlayFieldCovered.fill((255,255,255,0), pygame.Rect(x*self.Box_Size,y*self.Box_Size, self.Box_Size, self.Box_Size))
        
        self.FieldCovered[y][x] = 0
        self.BoxLeft -=1
        if (not self.GameOver):
            self.CheckWin()
        #Mines are around, which is dangerous :O
        if (self.Field[y][x] > 0):
            return

        #Open boxes around by recursion
        for y_offset in range(-1,2):
            for x_offset in range(-1,2):

                if (self.borderCheck(x,y,x_offset,y_offset)):
                    continue
                            
                self.OpenEmptySpaces(x + x_offset, y + y_offset)

    def CheckWin(self):
        if (self.GameOver):
            return
        if (self.BoxLeft == self.MineCount):
            print("You Win!")
            self.Sound_Win.play()
            self.GameOver = True
            self.EndTime = time.time() - self.StartTime
        elif (self.BoxLeft < self.MineCount):
            #thIs Is ssHould not hAppEn
            print("Wait waht")
        #print(self.BoxLeft)

    def SetLose(self):
        self.GameOver = True
        self.Sound_Lose.play()
        self.EndTime = time.time() - self.StartTime
        
    def OpenByFlag(self,x,y):
        Flags = 0
        Num = self.Field[y][x]

        for y_offset in range(-1,2):
            for x_offset in range(-1,2):
                if (self.borderCheck(x,y,x_offset,y_offset)):
                    continue

                nx = x + x_offset
                ny = y + y_offset

                if (self.FieldCovered[ny][nx] == 2):
                    Flags += 1

        #Matched flag count, try opening boxes around
        if (Flags == Num):
            for y_offset in range(-1,2):
                for x_offset in range(-1,2):
                    
                    if (self.borderCheck(x,y,x_offset,y_offset)):
                        continue

                    nx = x + x_offset
                    ny = y + y_offset
                 
                    if (self.FieldCovered[ny][nx] == 1):
                        self.Image_PlayFieldCovered.fill((255,255,255,0), pygame.Rect( (nx*self.Box_Size,ny*self.Box_Size), self.Box_Size_Rect)  )
                        #Wrong flag!
                        if (self.Field[ny][nx] == 10):
                            self.SetLose()
                            self.Sound_WrongFlag.play()
                        else:
                            self.OpenEmptySpaces(nx,ny)

        if (not self.GameOver):
            self.CheckWin()
            
    def onChange(self):
        pass

    def onChangeDone(self):
        #We are handling events in our scene
        pygame.pgSys.Handle_Events_InMain = False
        self.playBGM()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                break
            elif event.type == self.BGM_EVENT:
                #When BGM ends
                self.playBGM()
                
            elif (SDL2):
                if event.type == pygame.APP_WILLENTERBACKGROUND:
                    sleeping = True
                #App is awake from background, reinit the display
                elif event.type == pygame.APP_DIDENTERFOREGROUND:
                    sleeping = False
                    pygame.pgSys.InitDisplay()
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                btn1, btn2, btn3 = pygame.mouse.get_pressed()

                #Double button check
                if (btn1 and btn3):
                    self.DoubleButton = True

                #Mouse pos with border check
                x, y = event.pos
                x= int(x/self.Box_Size)
                y= int(y/self.Box_Size)
                
                if (x < 0 or y < 0 or x >= self.FieldSize[0] or y >= self.FieldSize[1]):
                    continue
                
                self.last_x, self.last_y = x, y

                 #Buttons Check
                if event.button == 4:
                    #Roll Down
                    pass
                elif event.button == 5: 
                    #Roll Up
                    pass
                elif event.button == 1:
                    if (self.GameOver):
                        self.GameOver = False
                        self.Field_Initalize()
                        return
                elif not self.DoubleButton and event.button == 3:
                    if (self.FieldCovered[y][x] == 0):
                        continue

                    if (self.FieldCovered[y][x] == 1):
                        self.FieldCovered[y][x] = 2
                        self.Sound_FlagIn.play()
                        self.Image_PlayFieldCovered.blit(self.Image_Marked, (x*self.Box_Size,y*self.Box_Size))
                    else:        
                        self.Sound_FlagOut.play()
                        self.FieldCovered[y][x] = 1
                        self.Image_PlayFieldCovered.blit(self.Image_Covered, (x*self.Box_Size,y*self.Box_Size))
                        
                    #Right Click
                    pass
            elif event.type == pygame.MOUSEBUTTONUP:
                #Mouse pos with border check
                x, y = event.pos
                x= int(x/self.Box_Size)
                y= int(y/self.Box_Size)
                
                if (x < 0 or y < 0 or x >= self.FieldSize[0] or y >= self.FieldSize[1]):
                    continue
                
                #Only do work if mouse pos is not moved away
                if (self.last_x == x and self.last_y == y):

                    #Double button check
                    if (self.DoubleButton):
                        self.OpenByFlag(x,y)
                        
                    elif event.button == 1:
                        #Game reset
                        if (self.GameOver):
                            self.GameOver = False
                            self.Field_Initalize()
                            return

                        #Flagged box
                        if (self.FieldCovered[y][x] == 2):
                            continue

                        #Booom :(
                        if (self.Field[y][x] == 10):
                            #First click shouldn't boom >:(
                            if (self.GameStart):
                                self.SetLose()
                            else:
                                #print("*Something wrong* happened, reset field.")
                                self.Field_Initalize((x,y))
                            return
                        else:
                            self.OpenEmptySpaces(x,y)
                            if (not self.GameStart):
                                self.StartTime = time.time()
                            self.GameStart = True

                            
                self.DoubleButton = False
            
    def graphicsUpdate(self):

        if (pygame.pgSys.RenderEnabled):
            #TODO: pygame_sdl2 or Render support
            pass
        else:
            pygame.pgSys.Screen.blit(self.CurrentBackground, (0,0))
            pygame.pgSys.Screen.fill((192,192,192,63), None, pygame.BLEND_RGBA_MULT)
            
            pygame.pgSys.Screen.blit(self.Image_PlayField, (0,0))
            if (not self.GameOver):
                pygame.pgSys.Screen.blit(self.Image_PlayFieldCovered, (0,0))
            pygame.pgSys.Screen.blit(self.Image_PlayFieldGrid, (0,0))

            #UI Stat
            if (self.GameStart):
                if (self.GameOver):
                    currenttime = int(self.EndTime)
                else:
                    currenttime = int(time.time() - self.StartTime)
            else:
                currenttime = 0

            image_time = pygame.pgSys.FontLarge.render("TIME :%d" % currenttime, 1, (0,255,0))
            pygame.pgSys.Screen.blit(image_time, (0,self.Image_PlayField.get_height()))

            #Game set text
            if (self.GameOver):

                if (self.BoxLeft == self.MineCount):
                    image_result = pygame.pgSys.FontLarge.render("YOU WIN!", 1, (0,255,255))
                else:
                    image_result = pygame.pgSys.FontLarge.render("YOU LOSE.", 1, (255,0,0))

                pygame.pgSys.Screen.blit(image_result, (int((pygame.pgSys.WINDOWWIDTH - image_result.get_width()) /2),self.Image_PlayField.get_height()))
