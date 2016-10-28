from gear import *
import pygame, spriteHelper
##several generic colors.
##This may change location at some point
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)##This is the optional color key
CYAN     = (  0, 255, 255)##This is the background key
DEFAULT_MUTINY = 0

def loadColors():
    return dict(red = [RED, False], blue = [BLUE, False],
                   green = [GREEN, False], yellow = [YELLOW, False],
                   orange = [ORANGE, False])

class ColorTakenError(StandardError):
    pass

class team:
    """This is the team class, which contains fighters.
        A team has a name, color, and an alliagence to a
        race"""
    
    ##Every color in _colors contains the 3 character
    ##tuple representing the color, and if the color is being used.
    ##More colors may be added to this dictionary

    _colors = loadColors()
    
    def __init__(self, name, color, race):
        self._name = name
        self._color = None
        self._setColor(color)
        self._race = race
        self._fighters = []
        self._raceBuff()
        self._isActive = False
        self.teamGroup = pygame.sprite.RenderPlain()

    def _raceBuff(self):
        if self._race == None:
            return
        else:
            return ##This will change by using a helper class

    def getName(self):
        return self._name

    def getColorCode(self):
        return self._colors[self._color][0]
    
    def getColor(self):
        return self._color

    def getColors(self):
        return self._colors

    def newColor(self, colorName, colorCode):
        self._colors[colorName] = [colorCode, False]

    def _setColor(self, color):
        ##This line switches the color from being used to not.
        team._colors[color][1] = False
        ##This checks to see if the desired color is being used.
        ##If it is, the function raises an error
        if team._colors[color][1]:
            raise ColorTakenError("The team color has been taken!")  
        ##Otherwise, it changes the color
        else:
            team._colors[color][1] = True
            self._color = color
        
    def fighters(self):
        return self._fighters

    def getRace(self):
         return self._race
        
    def hasFighter(self):
        return any(newFighter == f for f in self.fighters)

    def killFighter(self, deadFighter):
        deadFighter.kill()

    def rmFighter(self, fighter):
        self._fighters.remove(fighter)
        self.teamGroup.remove(fighter.sprite())
        fighter.changeTeam(None)

    def addFighter(self, newFighter):
        if self.hasFighter(newFighter):
            return
        self._fighters.append(newFighter)
        self.teamGroup.add(fighter.sprite())
        newFighter.changeTeam(self)
        
    def addFighters(self, fighterList):
        for f in fighterList:
            self.addFighter(f)

    def getMutiny(self):
        return sum(f.getMutiny() for f in self._fighters)

    def makeActive(self):
        self._isActive = True

    def makeInactive(self):
        self._isActive = False

    def isActive(self):
        return self._isActive

def _defaultGear():
    return gear()
    
class fighter(pygame.sprite.GroupSingle):
    """This is the fighter class.
        A fighter has a name, health, a race, knows its location
        on the board, knows its team, knows its gear, and
        knows its level."""
    activeFighterGroup = pygame.sprite.GroupSingle()
    def __init__(self, name, health, race = None, location = None,
                 team = None, gear=None, level = 1):
        pygame.sprite.GroupSingle.__init__(self)
        self._name = name
        self._health = health ##Comes in fully healed
        self._maxhealth = health
        self._location = location
        self._isDead = False
        if gear == None:
            self._gear = _defaultGear()
        else:
            self._gear = gear
        self._race = race
        self._level = level
        self._muntiny = DEFAULT_MUTINY
        if team == None:
            self._team = None
        else:
            self._team = team
            team.addFighter(self)
        self._applyAugments()
        self._generateSprite()
        self._raceBuff()

    def _raceBuff(self):
        if self._race == None:
            return
        else:
            return ##This will change by using a helper class

    def _generateSprite(self):
        ###This function will eventually handle generating the sprite.
        return

    def getName(self):
        return self._name

    def getHealth(self):
        return self._health

    def getLocation(self):
        return self._location
            
    def changeTeam(self, team):
        self._team.rmFighter(self)
        self._team =  team
        team.addFighter(self)

    def getRace(self):
        return self._race

    def getGear(self):
        return self._gear

    def getMutiny(self):
        return self._muntiny

    def changeGear(self, gun=None, armor=None, **augments):
        if gun != None:
            self._gear._changeGun(gun)
        if armor != None:
            self._gear._changeArmor(armor)
        self._deactivateAugments()
        self._gear._changeAugments(**augments)
        self._applyAugments
        
    def moveFromTo(self, end):
        self._location = end

    def kill(self):
        self._health = 0
        self._isDead = True
        self.sprite().kill() ##eventually, there will be a "kill" animation.

    def takeDamage(self, ammo):
        damage= ammo.getDamage()
        self._health-=damage
        if self._health<=0:
            self._damage = 0
            self.kill()

    def gainLevel(self):
        self._level+=1
        self.gainLevelBonuses()

    def gainLevelBonuses(self):
        return

    def loseLevel(self):
        self._level-=1

    def addMutiny(self, mutiny):
        self._mutiny += mutiny

    def subMutiny(self, mutiny):
        self._muntiny -= mutiny
        if self._mutiny<=0:
            self._mutiny = 0

    def makeActive(self):
        self.activeFighterGroup.add(self.sprite())

    def isActive(self):
        return self.activeFighterGroup.has(self.sprite())

    def _applyAugments(self):
        for aug in self._gear._augments:
            aug.runFunction(self)

    def _deactivateAugments(self):
        for aug in self._gear._augments:
            aug.reverseFunction(self)

class fighterFactory:
    """This class generates fighters."""
    def __init__(self, team):
        self._team = team
    def makeFighters(n, nameList, healthList, raceList,
                     gearList=None, levelList = None):
        if len(nameList)!=n:
            raise BufferError("nameList must be size n")
        if len(healthList)!=n:
            raise BufferError("healthList must be size n")
        if len(raceList)!=n:
            raise BufferError("raceList must be size n")
        if len(spriteList)!=n:
            raise BufferError("spriteList must be size n")
        if gearList == None:
            gearList = [gear()]*n
        elif len(gearList)!=n:
            raise BufferError("gearList must be size n")
        if levelList == None:
            levelList = [1]*n
        elif len(levelList)!=n:
            raise BufferError("levelList must be size n")
        fighterList = []
        for i in range(n):
            fighterList.append(fighter(nameList[i], healthList[i], raceList[i],\
                                    team = self._team, gear = gearList[i]))
        return fighterList
