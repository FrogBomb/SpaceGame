import pygame, math, tiles, sys
"""This module provides several functions to help with drawing
the board and several actions on the board. This includes
modifying surfaces and motion."""
class SurfaceLayersError(StandardError):
    pass

##class SurfaceLayers():
##    def __init__(self, background, layers, layerRects):
##        if len(layers) != len(layerRects):
##            raise SurfaceLayersError("layers and layerRects\
##                                        must be the same size.")
##        bgRect = background.get_rect()
##        self.bg = background
##        self.layers = [i for i in layers]
##        self.layerRects = layerRects
##        self.image = background
##        
##    def __getitem__(self, index):
##        return self.layers[index], self.layerRect[index]
##    
##    def __setitem__(self, index, value):
##        self.layers[index] = value[0]
##        self.layerRects[index] = value[1]
##        
##    def addLayer(self, index, layer, layerRect):
##        self.layers = self.layers[:index] + [layer] +\
##                      self.layers[index:]
##        self.layerRects = self.layerRects[:index] + [layerRect]\
##                          + self.layerRects[index:]
##        
##    def rmLayer(self, index):
##        self.layers.remove(index)
##        self.layerRects.remove(index)
##
##    def modLayerRect(self, index, layerRect):
##        self.layerRects[index] = layerRect
##
##    def modLayer(self, index, layer):
##        self.layers[index] = layer
##
##    def renderLayers(self, layerIndecies = None):
##        if layerIndecies == None:
##            layerIndecies = range(len(self.layers))
##        self.image.blit(self.bg, (0, 0))
##        for i in layerIndecies:
##            self.image.blit(self.layers[i], self.layerRects[i])
    
def blurSurf(surface, amt):
    """
    Blur the given surface by the given 'amount'.  Only values 1 and greater
    are valid.  Value 1 = no blur.
    """
    if amt < 1.0:
        raise ValueError("Arg 'amt' must be greater\
                        than 1.0, passed in value is %s"%amt)
    scale = 1.0/float(amt)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    return surf

    
def drawSpriteInPath(pathFunction, start_path_time,\
                     time, prevRect, surface, bgSurface, sprite, update = True):
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
    surface.blit(bgSurface.subsurface(prevRect), (prevRect[0], prevRect[1]))
    curLoc = pathFunction(time-start_path_time)
    prevLoc = pathFunction(prev_time-start_path_time)
    sprite.update(time, (curLoc[0]-prevLoc[0], curLoc[1]-prevLoc[1]),\
                    ((curLoc[0]-prevLoc[0])**2+(curLoc[1]-prevLoc[1])**2)**.5)
    updateRect = surface.blit(sprite.image, \
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
def rot_fixedPoint(image, angle, fixedPoint):
    """Rotate an image and return its shift fixing fixedPoint.
    fixedPoint is a vector from the center of the image.
    The translation also moves the fixed point to the top left of
    the original image."""
    theta = angle*math.pi/180
    orig_rect = image.get_rect()
    orig_center = orig_rect.center
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect()
    rot_center = rot_rect.center
    transCenter = [rot_center[i]-orig_center[i] for i in range(2)]
    transX = fixedPoint[0]*math.cos(theta) + fixedPoint[1]*math.sin(theta)
    transY = fixedPoint[1]*math.cos(theta) - fixedPoint[0]*math.sin(theta)
    return rot_image, (transX-transCenter[0]-orig_center[0],\
                       transY-transCenter[1]-orig_center[1])

def drawGunAim(rayData, color, surface, coneSurface, spread = 1,\
               strength = 1):
    """Draws the aim of a gun. returns the bounding rect.
        rayData is a 4-tuple, the first 2 coefficients are the
        starting point for the ray, and the last 2 coefficients
        are the coordinates of another point on the line.
        color is the color
        coneSurface is the surface of the cone.
        spread is the size of the cone.
        (basically determines likelihood to hit)
        strength is the intensity of the line drawn
        width is the width of the line drawn.

        This line should be an aaline. (pygame.draw.aaline)"""
##    if prevRect!= None:
##        surface.blit(bgSurface.subsurface(prevRect), (prevRect[0], prevRect[1]))
    surfRect = surface.get_rect()
    x0, y0, x1, y1 = rayData
    xV = x1-x0
    yV = y1-y0
    avgX = surfRect[0]+surfRect[2]*.5
    avgY = surfRect[1]+surfRect[3]*.5
    midDisX = surfRect[2]*.5
    midDisY = surfRect[3]*.5
    if xV==0 and yV==0:
        yV = 1
    ##Xs is the "x side" and Ys is the "y side"
    if xV<0:
        Xs = surfRect[0]
    else:
        Xs = surfRect[0]+surfRect[2]
    if yV<0:
        Ys = surfRect[1]
    else:
        Ys = surfRect[1]+surfRect[3]
    try:
        dontPassBy = True
        a = (Xs-x0)/float(xV)
    except ZeroDivisionError:
        dontPassBy = False
        a = sys.maxint
        x1 = x0
        y1 = Ys
    if abs(y0+yV*a-avgY)>midDisY and dontPassBy:
        try:
            a = (Ys - y0)/float(yV)
        except ZeroDivisionError:
            dontPassBy = False
            a = sys.maxint
            x1 = Xs
            y1 = y0
    if dontPassBy:
        x1 = x0+xV*a
        y1 = y0+yV*a
    if xV == 0:
        if yV<0:
            theta = math.pi/2
        if yV>0:
            theta = math.pi*3.0/2
    else:
        theta = math.atan(float(yV)/float(xV)) + math.pi
    if xV < 0:
        theta = math.pi + theta
    theta = theta*180/math.pi
    theta = 360-theta
    coneRect = coneSurface.get_rect()
    coneSurface = pygame.transform.smoothscale(coneSurface,\
                                         (int(coneRect[2]*spread),\
                                          int(coneRect[3]*strength)))
    coneRect = coneSurface.get_rect()
    coneSurface, transCoords = rot_fixedPoint(coneSurface, theta,\
                              (-coneRect[2]/2.0, 0))
    ret = [pygame.draw.aaline(surface, color, (x0, y0), (x1, y1))]
    ret += [surface.blit(coneSurface,(x0+transCoords[0], y0+transCoords[1]))]
    pygame.display.update(ret)
    return ret
    ##For now, this is just a ray. Will improve in the future.

def drawBeamAim(rayData, surface, beamSurface, strength=1, width=1):
    """Draws where the beam will shoot.
    Strength is the intensity of the radical
    width is the width of the radical."""
##    if prevRect!= None:
##        surface.blit(bgSurface.subsurface(prevRect), (prevRect[0], prevRect[1]))
    surfRect = surface.get_rect()
    x0, y0, x1, y1 = rayData
    xV = x1-x0
    yV = y1-y0
    avgX = surfRect[0]+surfRect[2]*.5
    avgY = surfRect[1]+surfRect[3]*.5
    midDisX = surfRect[2]*.5
    midDisY = surfRect[3]*.5
    if xV==0 and yV==0:
        yV = 1
    ##Xs is the "x side" and Ys is the "y side"
    if xV<0:
        Xs = surfRect[0]
    else:
        Xs = surfRect[0]+surfRect[2]
    if yV<0:
        Ys = surfRect[1]
    else:
        Ys = surfRect[1]+surfRect[3]
    try:
        dontPassBy = True
        a = (Xs-x0)/float(xV)
    except ZeroDivisionError:
        dontPassBy = False
        a = sys.maxint
        x1 = x0
        y1 = Ys
    if abs(y0+yV*a-avgY)>midDisY and dontPassBy:
        try:
            a = (Ys - y0)/float(yV)
        except ZeroDivisionError:
            dontPassBy = False
            a = sys.maxint
            x1 = Xs
            y1 = y0
    if dontPassBy:
        x1 = x0+xV*a
        y1 = y0+yV*a
    if xV == 0:
        if yV<0:
            theta = math.pi/2
        if yV>0:
            theta = math.pi*3.0/2
    else:
        theta = math.atan(float(yV)/float(xV)) + math.pi
    if xV < 0:
        theta = math.pi + theta
    theta = theta*180/math.pi
    theta = 360-theta
    beamRect = beamSurface.get_rect()
    beamSurface = pygame.transform.scale(beamSurface,\
                                         (int(((x1-x0)**2 + (y1-y0)**2)**.5\
                                        + beamRect[3]),\
                                          beamRect[3]))
    beamRect = beamSurface.get_rect()
    beamSurface, transCoords = rot_fixedPoint(beamSurface, theta,\
                              (-beamRect[2]/2.0, 0))
##    ret = [pygame.draw.aaline(surface, color, (x0, y0), (x1, y1))]
    ret = []
    ret += [surface.blit(beamSurface,(x0+transCoords[0],\
                                      y0+transCoords[1]))]
##    sections = 1+int((((x1-x0)**2 + (y1-y0)**2)**.5)/beamRect[2])
##    xbeamLength = beamRect[2]*xV/((xV**2+yV**2)**.5)
##    ybeamLength = beamRect[2]*yV/((xV**2+yV**2)**.5)
##    for i in range(sections):
##        ret += [surface.blit(beamSurface,(x0+i*xbeamLength+transCoords[0],\
##                                          y0+i*ybeamLength+transCoords[1]))]
    pygame.display.update(ret)
    return ret
    ##For now, this is just a ray. Will improve in the future.
    

def drawBeam(time, surface, beamSprite, rayData):
    """Draws a beam.
    beamSprite is the sprite for a segment of the beam
    rayData is a 4-tuple, the first 2 coefficients are the
        starting point for the ray, and the last 2 coefficients
        are the coordinates of another point on the line."""
    return

def drawBulletPath(time, surface, bulletSprite, rayData):
    """Draws the path of the Bullet.
        bulletSprite is the sprite of the bullet.
        rayData is a 4-tuple, the first 2 coefficients are the
        starting point for the ray, and the last 2 coefficients
        are the coordinates of another point on the line."""
    return

def drawFighterPath(time, surface, fighterSprite, path):
    """Draws the path of the fighter.
    fighterSprite is the sprite of the fighter.
    path is the series of tiles the fighter will walk through."""
    return

def getCurrentBoardSurface(board, zoom):
    """Returns the surface related to the board object passed."""
    return

def drawBoardSurface(surface, board, center, zoom, updateRects = None):
    """Draws the current board onto a surface at the given rects."""
    return

def drawActiveStationaryFighter(time, selectedFighterGroup):
    """Draws the stationary motion for an active fighter."""
    return

def drawFighterPath(time, startHex, finishHex):
    """Draws the path the fighter will walk through."""
    return

def drawFighterWalking(time, startHex, finishHex, walkingFighterGroup):
    """Draws the fighter walking through a path."""
    return

def changeTeamColors(teamGroup, colorKey, newColor):
    """Changes the colors of a team."""
    for fighterSprite in teamGroup:
        for row in fighterSprite.images:
            for i in row:
                i.set_palette_at(colorKey, newColor)
            

def drawDamageWhenAim(damage, location):
    """Draws the damage when aiming at an enemy"""
    ###We need to find a font that will work for us. Do research!
    return
