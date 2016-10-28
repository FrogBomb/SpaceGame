DEFAULT_HEALTH = 300
from fighters import team, fighterFactory

class player:
    """This is the player class
        The player has access to edit anything about his/her team,
        and the player can choose his/her name."""
    
    def __init__(self, playerName, color, race):
        self._team = team(playerName + "'s team", color, race)
        self._name = playerName
        self._fFactory = fighterFactory(team)
        
    def generateTeam(n, names=None, healths=None, races = None,
                     gears = None, levels = None):
        if names==None:
            names = generateNames(n)
        if healths==None:
            healths = [DEFAULT_HEALTH]*n
        if races==None:
            races = [self._team.getRace()]*n
        if levels==None:
            levels = [1]*n
        fighters = self._fFactory.makeFighters(n, generateNames(n),
                                               healths,
                                               races, gears, levels)
        self._team.addFighters(fighters)

    def editPlayerName(self, name):
        self._name = name

    def editTeamName(self, name):
        self._team._name = name

    def editColor(self, color):
        self._team._setColor(color)

    def editRace(self, race):
        self._team._race = race

    def setTeamArmor(self, armor):
        for i in range(len(self._fighters)):
            self._team._fighters[i].setArmor(armor)
        
def generateNames(n):
    """Generates a list of 'random' names."""
    return range(n)##To be improved later
