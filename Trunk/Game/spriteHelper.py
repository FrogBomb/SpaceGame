import pygame, math, sys
"""Thank you:
http://shinylittlething.com/2009/07/21/pygame-and-animated-sprites/"""
SPEEDCALIBRATOR = 100
class WallSpriteError(StandardError):
    pass

def load_tiles(w, h, tileType, fileType):
    return load_sprite_sequence(w, h,\
                                "./data/images/tile"+tileType+"."+\
                                fileType)

def load_sprite_sequence(w, h, filename):
    """Loads a sequence of images with width w and hight h
        that compose a sprite into a list of surfaces."""
    images = []
    master_image = pygame.image.load(filename)
    master_width, master_height = master_image.get_size()
    for row in range(int(master_height/h)):
        images.append(\
            [master_image.subsurface((i*w, row*h, w, h)) for\
             i in range(int(master_width/w))])
    return images

class animatedSprite(pygame.sprite.Sprite):
    """"Animates a series of images into a sprite
        Regards go to
        http://www.sacredchao.net/~piman/writing/sprite-tutorial.shtml

        Images should be a list of lists containing surface objects."""
    
    def __init__(self, images, fps = 10):
        pygame.sprite.Sprite.__init__(self)
        self._images = images
        self._start = pygame.time.get_ticks()
        self._delay = 1000/fps
        self.last_update = 0
        self._frame = 0
        self._last_update = 0
        self._curRow = 0
        self.rect = images[0][0].get_rect()
        self.update(0, (0, 1))
        ##self.image

    def update(self, t, direction = (0, 0), speed = None, position = None):
        """Updates the sprite.
            t is the current time that has passed.
            Direction may be either an int or a 2-tuple"""
        if position != None:
            self.rect.move(position[0], position[1])
        if t - self._last_update > self._delay:
            self._frame += 1
            self._last_update = t
        self.changeDirection(direction)
        self.changeSpeed(speed)
        if self._frame >= len(self._images[0]): self._frame = 0
        self.image = self._images[self._curRow][self._frame]
        

    def stationaryUpdate(self, t):
        """Updates the sprite without changing speed or direction."""
        if t - self._last_update > self._delay:
            self._frame += 1
            self._last_update = t
        if self._frame >= len(self._images[0]): self._frame = 0
        self.image = self._images[self._curRow][self._frame]

    def updateToKill(self, t):
        """Updates the sprite untill the end of images, then kill.
            t is the current time that has passed."""
        self.update(t)
        if self._frame == 0: self.kill()

    def changeDirection(self, direction):
        if type(direction) == int:
            self._curRow = direction
            return
        x, y = direction
        x = -x
        if x == 0:
            if y>0:
                self._curRow = 0
            elif y<0:
                self._curRow = len(self._images)/2
            elif y == 0:
                self._frame = 0 #stopped moving, no direction
        else:
            theta = math.atan(float(y)/float(x)) + math.pi
            if x < 0:
                theta = math.pi + theta
            numOfSections = len(self._images)
            self._curRow = self._circleSection(theta, numOfSections)
            
    def changeSpeed(self, speed):
        if speed == None:
            return
        self.changeFPS(speed*SPEEDCALIBRATOR)

    def _circleSection(self, theta, numOfSections):
        lenOfSection = (2*math.pi)/numOfSections
        shiftedTheta = (theta - (math.pi-lenOfSection)/2)%(2*math.pi)
        return int(shiftedTheta//lenOfSection)
        
    def changeFPS(self, fps):
        if fps == 0:
            self._delay = sys.maxint
        else:
            self._delay = 1000/fps

    def getSpeed(self):
        return ((1000/self._delay))/float(SPEEDCALIBRATOR)

class fighterSprite(animatedSprite):
    def __init__(self, images, position = (0, 0), fps=10):
        pygame.sprite.Sprite.__init__(self)
        self._layer = 3 #this is just the default.
        self._images = images
        self._start = pygame.time.get_ticks()
        self._delay = 1000/fps
        size = images[0][0].get_size()
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.last_update = 0
        self._frame = 0
        self._last_update = 0
        self._curRow = 0
        self.rect = images[0][0].get_rect()
        self.update(0)
        ##self.image
    def changeDirection(self, direction):
        animatedSprite.changeDirection(self, direction)
        if direction == (0, 0):
            self._frame = 2
    

class wallSprite(animatedSprite):
    def __init__(self, images, position, directionInt, row, col, fps=10):
        """The walls will have 3 directions, 0=left, 1=middle,\
        2= right"""
        pygame.sprite.Sprite.__init__(self)
        if type(directionInt)!=int:
            raise WallSpriteError("The directionInt must be an int!")
        if directionInt == 0 or directionInt == 2:
            self._layer = row*4+3+(col%2)*2
        elif directionInt == 1:
            self._layer = row*4+4+(col%2)*2
        pygame.sprite.Sprite.__init__(self)
        self._images = images
        self._start = pygame.time.get_ticks()
        self._delay = 1000/fps
        size = images[0][0].get_size()
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.last_update = 0
        self._frame = 0
        self._last_update = 0
        self._curRow = 0
        self.rect = images[0][0].get_rect()
        self.update(0, direction)
        ##self.image
##    update = animatedSprite.stationaryUpdate
    def changeDirection(self, direction):
        if type(directionInt)!=int:
            raise WallSpriteError("The directionInt must be an int!")
        animatedSprite.changeDirection(self, direction)
    def changeType(self, tileType):
        self.changeDirection(tileType)

class tileSprite(animatedSprite):
    def __init__(self, images, tileType, isAnimated = False, fps=10):
        pygame.sprite.Sprite.__init__(self)
        self._layer = 0 ##will be on the bottom layer of the board
        self._images = images
        self._start = pygame.time.get_ticks()
        self._delay = 1000/fps
        size = images[0][0].get_size()
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.last_update = 0
        if isAnimated:
            self._frame = 0
        else:
            self._frame = 1
        self._last_update = 0
        self._curRow = 0
        self._isAnimated = isAnimated
        self.update(0)
    def update(self, t, tileType, toggleAnimation = False):
        if toggleAnimation:
            self._isAnimated = not self._isAnimated
        if self._isAnimated:
            if t - self._last_update > self._delay:
                self._frame += 1
                self._last_update = t
            if self._frame >= len(self._images[0]): self._frame = 1
            self.image = self._images[self._curRow][self._frame]
        else:
            self._last_update = t
            self._frame = 0
    stationaryUpdate = update
        ##self.image
##    update = animatedSprite.stationaryUpdate

class bulletSprite(animatedSprite):
    pass

class beamSprite(animatedSprite):
    pass ##Groups will be important here.

