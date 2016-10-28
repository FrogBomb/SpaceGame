import pygame, math, sys
"""Thank you:
http://shinylittlething.com/2009/07/21/pygame-and-animated-sprites/"""
SPEEDCALIBRATOR = 2000

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
        self.update(0, (0, 1))

    def update(self, t, direction = (0, 0), speed = 1):
        """Updates the sprite.
            t is the current time that has passed."""
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
        x, y = direction
        if x == 0:
            if y>0:
                self._curRow = 0
            elif y<0:
                self._curRow = len(self._images)/2
            elif y == 0:
                self._frame = 0 #stopped moving, no direction
        else:
            theta = math.atan(float(y)/float(x))
            if x < 0:
                theta = math.pi-theta
            numOfSections = len(self._images)
            self._curRow = self._circleSection(theta, numOfSections)
            
    def changeSpeed(self, speed):
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
    pass

class wallSprite(animatedSprite):
    pass ##Will interact with a fighter sprite at some point.

class tileSprite(animatedSprite):
    pass ##For tile destuction

class bulletSprite(animatedSprite):
    pass

class beamSprite(animatedSprite):
    pass ##Groups will be important here.

