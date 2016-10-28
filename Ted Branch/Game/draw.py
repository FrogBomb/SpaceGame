import pygame, math, tiles
"""This module provides several functions to help with drawing
the board and several actions on the board. This includes
modifying surfaces and motion."""

def drawSpriteInPath(pathFunction, start_path_time,\
                     time, prevRect, display, bgSurface, sprite, update = True):
    """Moves a sprite along a path, then returns the updated rect

        pathFunction should take a time (a number) and return coordinates.
        start_path_time is the time when the path was started.
        (This time is the time of the last frame of the previous path)
        time is the current time.
        prevRect is the rectangle that the sprite was in last
        display is the display object
        bgSurface is the surface behind the sprite
        sprite is the animatedSprite that will move along the path.

        """
    try:
        prev_time = drawSpriteInPath.prev_time
        drawSpriteInPath.curPathFunc
    except AttributeError:
        drawSpriteInPath.prev_time = start_path_time
        prev_time = start_path_time
        drawSpriteInPath.curPathFunc = pathFunction
    display.blit(bgSurface.subsurface(prevRect), (prevRect[0], prevRect[1]))
    curLoc = pathFunction(time-start_path_time)
    prevLoc = pathFunction(prev_time-start_path_time)
    sprite.update(time*1000, (curLoc[0]-prevLoc[0], curLoc[1]-prevLoc[1]),\
                    ((curLoc[0]-prevLoc[0])**2+(curLoc[1]-prevLoc[1])**2)**.5)
    updateRect = display.blit(sprite.image, \
                              (curLoc[0], curLoc[1]))
    if update:
        pygame.display.update([prevRect, updateRect])
    drawSpriteInPath.prev_time = time
    return updateRect

##def drawSpriteInPathWithSpeedPadding(pathFunction, start_path_time,\
##                     time, prev_time, prevRect, display, bgSurface, sprite):
##    """Moves a sprite along a path, then returns the updated rect
##
##        pathFunction should take a time (a number) and return coordinates.
##        start_path_t is the time when the path was started.
##        t is the current time.
##        prevRect is the rectangle that the sprite was in last
##        display is the display object
##        bgSurface is the surface behind the sprite
##        sprite is the animatedSprite that will move along the path.
##
##        """
##    display.blit(bgSurface.subsurface(prevRect), (prevRect[0], prevRect[1]))
##    curLoc = pathFunction(time-start_path_time)
##    prevLoc = pathFunction(prev_time-start_path_time)
##    sprite.update(time*1000, (curLoc[0]-prevLoc[0], curLoc[1]-prevLoc[1]),\
##                    ((((curLoc[0]-prevLoc[0])**2+(curLoc[1]-prevLoc[1])**2)**.5)\
##                  +sprite.getSpeed())/2.0)
##    updateRect = display.blit(sprite.image, \
##                              (curLoc[0], curLoc[1]))
##    pygame.display.update([prevRect, updateRect])
##    return updateRect

def drawGunAim(display, lineData, color):
    return

def drawBeam(time, display, beamSprite, lineData):
    return

def drawBulletPath(time, display, bulletSprite, lineData):
    return

def drawFighterPath(time, display, fighterSprite):
    return

def findWallHits(lineData):
    return

def getCurrentBoardSurface(board):
    return

def updateCurrentBoardSurface(boardSurface, board, updateRects=None):
    return

def drawBoardSurface(display, board, updateRects = None):
    return

def drawActiveStationaryFighter(time, fighterSprite):
    return

def drawFighterPath(time, fighterSprite):
    return

def changeTeamColors(fighterSprite):
    return


