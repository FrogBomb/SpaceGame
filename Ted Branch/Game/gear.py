class ReplicatorError(StandardError):
    pass

class gear:
    """This is the gear class.
    This class contains the gun, armor, and augments of a fighter."""
    def __init__(self, gun=None, armor=None, **augments):
        self._gun = gun
        self._armor = armor
        self._augments = augments

    def getGun(self):
        return self._gun

    def getArmor(self):
        return self._armor

    def getAugments(self):
        return self._augments

    def _changeGun(self, gun):
        self._gun = gun

    def _changeArmor(self, armor):
        self._armor = armor

    def _changeAugments(self, **augments):
        self._augments.clear()
        self._addAugments(**augments)

    def _addAugments(self, **augments):
        self._augments.update(augments)

    def _rmAugmentKey(self, augmentKey):
        self._augments.pop(augmentKey)

class gun:
    """This is the gun class.
        ammo is the type of ammo for the gun
        the capacity is the cap on how many bullets
        the gun may have. The skin is a reference to
        the skin of the gun."""
    def __init__(self, name, ammo, capacity, skin, gunType):
        self._name = name
        self._ammo = ammo
        self._capacity = capacity
        self._skin = skin
        self._type = gunType
##        self._functions = buffFunctions
        
    def _copy(self):
        return gun(self._name, self._ammo, self._capacity,
                   self._skin)

    def getName(self):
        return self._name

    def getSkin(self):
        return self._skin

    def getCapacity(self):
        return self._capacity

    def getAmmo(self):
        return self._ammo

    def shoot(self):
        """Shoots the gun, then returns the damage."""
        self._ammo._count-=1
        return self._ammo.getDamage()

    def reloadGun(self, n):
        """Reloads the gun with n more bullets, then returns how many
        didn't fit."""
        bulletsBack = 0
        self._ammo._count += n
        if self._ammo._count > self._capacity:
            bulletsBack = self._capacity - self._ammo._count
            self._ammo._count = self._capacity
        return bulletsBack

    
##    def runFunctions(self, fighter):
##        for f in self._functions:
##            f(fighter)
    
class ammo:
    """This is the class for ammo
        damage is the damage of the bullet
        skin is a file reference to the skin of the bullets
        ammoType is the type of ammo (either a beam or
        a projectile)."""
    def __init__(self, name, damage, skin, *ammoType):
        self._name = name
        self._damage = damage
        self._count = 0
        self._skin = skin
        self._type = ammoType

    def getName(self):
        return self._name

    def getDamage(self):
        return self._damage

    def getCount(self):
        return self._count

    def getSkin(self):
        return self._skin
    
    def getType(self):
        return self._type
        
class armor:
    def __init__(self, name, defence, skin):
        self._name = name
        self._defence = defense
        self._skin = skin
##        self._functions = buffFunctions

    def _copy(self):
        return armor(self._name, self._defence, self._skin)

    def getName(self):
        return self._name

    def getSkin(self):
        return self._skin

    def getDefense(self):
        return self._defence

##    def runFunctions(self, fighter):
##        for f in self._functions:
##            f(fighter)

class augment:
    def __init__(self, name, location, augFunction):
        self._name = name
        self._location = location
        self._function = augFunction

    def getName(self):
        return self._name

    def getLocation(self):
        return self._location

    def runFunction(self, fighter):
        self._function.EffectFighter(fighter)

    def reverseFunction(self, fighter):
        self._function.rmEffect(fighter)

    

class gunReplicator:
    """Takes an instance of a gun and
        replicates it."""
    def __init__(self, gun):
        self._gunModel = gun

    def generateGuns(self, n, newGun = None):
        if newGun == None:
            return [self._gunModel._copy() for i in range(n)]
        elif isinstance(newGun, gun):
            self._gunModel = newGun
            return self.generateGuns(n)
        raise ReplicatorError("Must be a gun to replicate")

class armorReplicator:
    """Takes and instance of armor and
        replicates it."""
    def __init__(self, armor):
        self._armorModel = armor

    def generateArmor(self, n, newArmor = None):
        if newArmor == None:
            return [self._armorModel._copy() for i in range(n)]
        elif isinstance(newArmor, armor):
            self._armorModel = newArmor
            return self.generateArmor(n)
        ReplicatorError("Must be armor to replicate")
            

