import fighters, gear, fileSystem, player, tiles, augmentFunctions,\
       spriteHelper, draw
import pygame, sys, time, math

##TED: change this line to go to the image:
PIGMANWALKINGLOCATION = "./data/images/PigmanFrontRefinedAnimation.bmp"
SPACELOCATION = "./data/images/Space.bmp"

def spritePath(t):
##    return 225+100*math.cos(t),\
##            225+100*math.sin(t)
    try:
        if t> spritePath.prevT:
            
            spritePath.prevLoc[t] = [(pygame.mouse.get_pos()[i]-25+1000\
                               *spritePath.prevLoc[spritePath.prevT][i])/1001.0\
                                for i in range(2)]
            spritePath.prevT = t
    except AttributeError:
        spritePath.prevLoc = dict()
        spritePath.prevLoc[0.0] = [0,0]
        spritePath.prevLoc[t] = [pygame.mouse.get_pos()[i]\
                                     for i in range(2)]
        spritePath.prevT = 0
    for times in [i for i in spritePath.prevLoc.iterkeys()]:
            if t - times>.1:
                spritePath.prevLoc.pop(times)
    try:
        return spritePath.prevLoc[t]
    except KeyError:
        spritePath.prevLoc[t] = [pygame.mouse.get_pos()[i]\
                                     for i in range(2)]
        return spritePath.prevLoc[t]

##def draw(t, prev_t, exitNow, window, sprite):
##    
##    window.fill((0, 0, 0))
##    coverRect = (225+100*math.cos((prev_t)/1000),\
##                 225+100*math.sin((prev_t)/1000),50,50)
##    pygame.draw.rect(window, (0,0,0), coverRect)
##    updateRect = window.blit(sprite.image, (225+100*math.cos(t/1000),\
##                                           225+100*math.sin(t/1000)))
##    pygame.display.update([coverRect, updateRect])
##    sprite.update(t)
##    return exitNow

def main():
    exitNow = False
    pygame.init()
    images = spriteHelper.load_sprite_sequence(\
        50, 50, PIGMANWALKINGLOCATION)
    keyColor = images[0][0].map_rgb(fighters.PURPLE)
    for row in images:
        for i in range(len(row)):
##            k = pygame.pixelarray.PixelArray(row[i])
####            k.replace(\
####                fighters.PURPLE, row[i].map_rgb((255,0 , 0)))
####            for krow in range(len(k)):
####                for kcol in range(len(k[0])):
####                    if k[krow][kcol] == row[i].map_rgb((255, 255, 255)):
####                        k[krow][kcol] = (255, 0, 0)
##            row[i] = k.make_surface()
            row[i].set_colorkey((0, 255, 255))
            row[i].set_palette_at(keyColor,\
                                  (255, 255, 255))
    sprite = spriteHelper.animatedSprite(images)
    window = pygame.display.set_mode((500, 500))
    bgSurface = pygame.image.load(SPACELOCATION)
##    bgSurface = pygame.surface.Surface((500, 500))
##    bgSurface.fill((255,0,0))
    window.blit(bgSurface, (0, 0))
    pygame.display.flip()
    timeOffset=0
    prevRect = pygame.rect.Rect(500, 500, 0, 0)
    startTime = time.clock()
    
    try:
        while(not exitNow):
##            if (pygame.event.peek(pygame.MOUSEBUTTONDOWN)):
##                pygame.event.clear()
##                while(True):
##                    if pygame.event.peek(pygame.MOUSEBUTTONUP):
##                        break
##                window = pygame.display.set_mode((500, 500))
##            else:
            pygame.event.clear()
            curTime = time.clock()
            prevRect = draw.\
                       drawSpriteInPath(spritePath, startTime,\
                                        curTime, prevRect,\
                                        window, bgSurface,\
                                        sprite)
            for row in images:
                for i in range(len(row)):
                    row[i].set_palette_at(keyColor,\
                                          ((1+math.sin(curTime))*.5*255,\
                                           (1+math.sin(2*curTime))*.5*255,\
                                           (1+math.sin(curTime*7))*.5*255))
            prevTime = curTime
            if pygame.event.peek(pygame.QUIT):
                 exitNow = True
            
    finally: pygame.quit()

if __name__ == "__main__": main()

