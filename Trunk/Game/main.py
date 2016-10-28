import fighters, gear, fileSystem, player, tiles, augmentFunctions,\
       spriteHelper, draw, gameControl
import pygame, sys, time, math

##TED: change this line to go to the image:
PIGMANWALKINGLOCATION = "./data/images/Pigman.bmp"
SPACELOCATION = "./data/images/Space.bmp"
CONEOFFIRE = "./data/images/ConeOFire.png"
BEAMIMAGE = "./data/images/Beam.png"

def spritePath(t):
    return 225+100*math.cos(t/1000.0),\
            225+100*math.sin(t/1000.0)
##    try:
##        if t> spritePath.prevT:
##            
##            spritePath.prevLoc[t] = [(pygame.mouse.get_pos()[i]-25+1000\
##                               *spritePath.prevLoc[spritePath.prevT][i])/1001.0\
##                                for i in range(2)]
##            spritePath.prevT = t
##    except AttributeError:
##        spritePath.prevLoc = dict()
##        spritePath.prevLoc[0.0] = [0,0]
##        spritePath.prevLoc[t] = [pygame.mouse.get_pos()[i]\
##                                     for i in range(2)]
##        spritePath.prevT = 0
##    for times in [i for i in spritePath.prevLoc.iterkeys()]:
##            if t - times>.1:
##                spritePath.prevLoc.pop(times)
##    try:
##        return spritePath.prevLoc[t]
##    except KeyError:
##        spritePath.prevLoc[t] = [pygame.mouse.get_pos()[i]\
##                                     for i in range(2)]
##        return spritePath.prevLoc[t]
##
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
    coneImage = pygame.image.load(CONEOFFIRE)
    beamImage = pygame.image.load(BEAMIMAGE)
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
    sprite = spriteHelper.fighterSprite(images)
    window = pygame.display.set_mode((500, 500))
    bgSurface = pygame.image.load(SPACELOCATION)
##    bgSurface = pygame.surface.Surface((500, 500))
##    bgSurface.fill((255,0,0))
    window.blit(bgSurface, (0, 0))
    pygame.display.flip()
    timeOffset=0
    prevRect = pygame.rect.Rect(500, 500, 0, 0)
    prevLineRects = [pygame.rect.Rect(0, 0, 0, 0)]*2
    startTime = pygame.time.get_ticks()
    
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
            curTime = pygame.time.get_ticks()
            window.blit(bgSurface, (0, 0))
            clearRects = [prevRect]+ prevLineRects
            prevRect = draw.\
                       drawSpriteInPath(spritePath, startTime,\
                                        curTime, prevRect,\
                                        window, bgSurface,\
                                        sprite, False)
            prevLineRects = draw.drawGunAim((prevRect[0]+25, prevRect[1]+25)\
                                           +pygame.mouse.get_pos(),\
                            (255, 0,0), window, coneImage,\
                                            1, 1.5)
##            prevLineRects = draw.drawBeamAim((prevRect[0]+25, prevRect[1]+25)\
##                                             +pygame.mouse.get_pos(),\
##                                             window, beamImage)
            pygame.display.update(clearRects)
            for row in images:
                for i in range(len(row)):
                    row[i].set_palette_at(keyColor,\
                                          ((1+math.sin(curTime/1000.0))*.5*255,\
                                           (1+math.sin(2*curTime/1000.0))*.5*255,\
                                           (1+math.sin(curTime*7/1000.0))*.5*255))
            prevTime = curTime
            if pygame.event.peek(pygame.QUIT):
                 exitNow = True
            
    finally: pygame.quit()

if __name__ == "__main__": main()

