import threading
import pygame
import sys

def console_window():
    print("Game Initalized")
    Running = True
    try:
        while Running:
            argv = input().split(" ")
            
            if (not pygame.display.get_init()):
                Running = False
                print("Main thread has ended, exit.")
                break
            
            if (len(argv) == 0):
                break

            if (argv[0] == "exit"):
                Running = False
            elif (argv[0] == "BGColor"):
                print(pygame.pgSys.BGColor)
            else:
                print(argv, end=' is not defined\n')
    except KeyboardInterrupt:
        pygame.quit()
        
    #Quitting with thread is not safe, post quit event for main thread instead
    pygame.event.post(pygame.event.Event(pygame.QUIT)) 
    
console_thread = threading.Thread(target = console_window)
console_thread.start()
