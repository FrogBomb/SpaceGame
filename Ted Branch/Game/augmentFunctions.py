##The augment functions work by a decorator patern.
##augmentFunction is a blank augment function
class augmentFunction:
    def __init__(self, value=0):
        self._value = value
        self._prevVals = None
    def effectFighter(self, fighter):
        return
    def rmEffect(self, fighter):
        return
##The convention for augmentFunctions will be that
##the name of every augmentFunction will start with augF_
##Here is an example of an augment function:
class augF_addMaxHealth(augmentFunction):
    def effectFighter(self, fighter):
        fighter._maxHealth += self._value
        fighter._health = fighter._maxHealth

    def rmEffect(self, fighter):
        fighter._maxHealth -= self._value
        fighter._health = fighter._maxHealth
##Future augmentFunctions will go here


##This is the base augmentDecorator.
##When decorators are instanciated, they
##return a modified version of the augmentFunction
class augDecorator(augmentFunction):
    def __init__(self, decoratedAugFunction, value=0):
        self._value = value
        self._decoratedAugF = decoratedAugFunction
        self._prevVals = None
        
    def effectFighter(self, fighter):
        self._dectoratedAugF.effectFighter(fighter)
        ##All the effects to the fighter go here

    def rmEffect(self, fighter):
        ##All the things that remove the effects
        ##go here
        self._dectoratedAugF.rmEffect(fighter)

##The convention for augmentDecorators will be that
##the name of every augmentDecorator will start with augD_
##Here are some examples:
class augD_addMaxHealth(augDecorator):
    def effectFighter(self, fighter):
        self._dectoratedAugF.effectFighter(fighter)
        fighter._maxHealth += self._value
        fighter._health = fighter._maxHealth

    def rmEffect(self, fighter):
        fighter._maxHealth -= self._value
        fighter._health = fighter._maxHealth
        self._dectoratedAugF.rmEffect(fighter)

class augD_givesPoisonDamage(augDecorator):
    def effectFighter(self, fighter):
        self._dectoratedAugF.effectFighter(fighter)
        self._prevVals = fighter._gear._gun._ammo.getType()
        fighter._gear._gun._ammo._type += ["poison"]
        
    def rmEffect(self, fighter):
        fighter._gear._gun._ammo._type = self._prevVals
        self._dectoratedAugF.rmEffect(fighter)

##More Decorators will go here

##Here is how they can be used. The following code makes 3 augment functions
##One that adds max health to a fighter, one that gives the fighter
##poison damage, and one that does both. Uncomment and run with 3 fighter
##objects (that have gear) to see this in action.

##def augFuncexample(fighterA, fighterB, fighterC):
##    k = input("Here are the stats of our fighters <press enter>")
##    print "Ammo of A: ", fighterA._gear._gun._ammo._type
##    print "Ammo of B: ", fighterB._gear._gun._ammo._type
##    print "Ammo of C: ", fighterC._gear._gun._ammo._type
##    print "MaxHealth of A: ", fighterA._maxHealth
##    print "MaxHealth of B: ", fighterB._maxHealth
##    print "MaxHealth of C: ", fighterC._maxHealth
##    addMaxHFunction = augF_addMaxHealth(50)
##    blankFunction = augmentFunction()
##    poisonFunction = augD_givesPoisonDamage(blankFunction)
##    poisonAndMaxHFunc = augD_addMaxHealth(poisonFunction)
##    #OR
##    #poisonAndMaxHFunc = augD_givesPoisonDamage(addMaxHFunction)
##    k = input("Now, we give the fighters effects <press enter>")
##    addMaxHFunction.effectFighter(fighterA)
##    poisonFunction.effectFighter(fighterB)
##    poisonAndMaxHFunc.effectFighter(fighterC)
##    print "Ammo of A: ", fighterA._gear._gun._ammo._type
##    print "Ammo of B: ", fighterB._gear._gun._ammo._type
##    print "Ammo of C: ", fighterC._gear._gun._ammo._type
##    print "MaxHealth of A: ", fighterA._maxHealth
##    print "MaxHealth of B: ", fighterB._maxHealth
##    print "MaxHealth of C: ", fighterC._maxHealth
##    k = input("Then, we can remove the effects <press enter>")
##    addMaxHFunction.rmEffect(fighterA)
##    poisonFunction.rmEffect(fighterB)
##    poisonAndMaxHFunc.rmEffect(fighterC)
##    print "Ammo of A: ", fighterA._gear._gun._ammo._type
##    print "Ammo of B: ", fighterB._gear._gun._ammo._type
##    print "Ammo of C: ", fighterC._gear._gun._ammo._type
##    print "MaxHealth of A: ", fighterA._maxHealth
##    print "MaxHealth of B: ", fighterB._maxHealth
##    print "MaxHealth of C: ", fighterC._maxHealth
    
