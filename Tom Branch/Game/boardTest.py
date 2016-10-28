from main import *
def main():
    pygame.init()
    window = pygame.display.set_mode((500, 500))
    board = tiles.board(50, 50, skinType = "Steel")
    bg = pygame.Surface((500, 500))
    bg.fill((255, 0, 0))
    vControl = gameControl.gameViewControl(window, board, bg)
    exitNow = False
    pygame.display.flip()
    curTime = time.clock()
    window = draw.blurSurf(window, 200)
    gII = gameControl.gameInputInterpreter(\
        0,0, vControl)
    try:
        while(not exitNow):
            curTime = pygame.time.get_ticks()
            gII.updateInput(curTime)
            pygame.display.flip()
            vControl.update(curTime, (curTime/1000)%10, curTime==0)
##            vControl.zoom(-.05)
##            vControl.move(1, 1)
            if pygame.event.peek(pygame.QUIT):
                 exitNow = True
    finally: pygame.quit()
if __name__=="__main__":
    main()
