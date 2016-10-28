from fighters import *
from gear import *
TEAMFOLDER = "./saveFiles/teams/"
TEAMLIST = "./saveFiles/teams/teamList.txt"
GUNREF = "./data/guns.txt"
ARMORREF = "./data/armors.txt"
AUGMENTREF = "./data/augments.txt"
DATAFILE = "./data"
RESTRICTEDCHARS = '/?<>\\:*|"$\n'

class SaverLoaderError(StandardError):
    pass

class NameCheckError(StandardError):
    pass

def nameCheck(name):
    for s in name:
        if any(s==i for i in RESTRICTEDCHARS):
            raise NameCheckError(RESTRICTEDCHARS[:-1]+\
                                 " or a new line are not\
                                 allowed in the name %s."\
                                 % name)
    return name
            
        
class teamSaverLoader:
    """This class loads and saves teams into
    a team save file.

    The format of the team files has 2 parts:
    --The first is the team, designated by
        the name, color, then race.
    --The second part is contains the individual fighter information:
        the name, health, race, gear, and level. (in that order)
        The gear is a 2-tuple, containing the gun name and the
        armor name. These names will be referenced in GUNREF
        and ARMORREF, which contain all generating
        information. The fighters are organized by teams.
        (in the same order the teams appear in the
        first part of the file)
    There cannot be two teams with the same name.
    All entries are separated by a single $"""
    def __init__(self, teamFolder = TEAMFOLDER):
        self._folder = teamFolder
        self._gT = gearTranslator()

    def load(self, teamName):
        with open(self._folder + nameCheck(teamName) + ".dat") as inFile:
            readLines = inFile.readlines()
        team = self._convertToTeam(readLines[0])
        fighters = [self._convertToFighter(f) for f in readLines[1:]]
        team.addFighters(fighters)
        return team
        
##        teams = readLines[:readLines.index('%')]
##        fighters = readLines[readLines.index('%')+1:]
##        fightersInTeams = [[]]*len(teams)
##        i = 0
##        for f in fighters:
##            if f == "~":
##                i+=1
##            else:
##                fighersInTeams[i].append(self._convertToFighter(f))
##        teams = [self._convertToTeam(t) for t in teams]
##        for i in range(len(teams)):
##            teams[i].addFighters(fightersInTeams[i])
##        return teams
                
    def _convertToFighter(self, fString):
        sF.lstrip("\n")
        sF = fString.split("$")
##        gear = sF[3].split(",")
##        if gear[0].startswith("(") and gear[1].endswith(")"):
##            gear[0] = gear[0][1:]
##            gear[1] = gear[1][:-1]
##        else:
##            raise SaverLoaderError("Error loading Fighter %s" % sF[0])
        
        return fighter(sF[0], int(sF[1]),\
                       self._raceTranslatorTo(sF[2]), \
                       self._gearTranslatorTo(gear),\
                       int(sF[4]))

    def _convertToTeam(self, tString):
        sT.lstrip("\n")
        sT = tString.split("$")
        return team(sT[0], sT[1], self._raceTranslatorTo(sF[2]))

    def _raceTranslatorTo(self, race):
        return race

    def _gearTranslatorTo(self, gear):
        return self._gt.translateTo(gear)

    def _raceTranslatorFrom(self, race):
        return race

    def _gearTranslatorFrom(self, gear):
        return self._gt.translateFrom(gear) 
        
    def save(self, team):
        try:
            inFile = open(TEAMLIST, 'r+')
            teamlist = inFile.readlines()
            teamName = nameCheck(team.getName())
            flag = False
            try: ##Checks to see if the value is in the list
                teamlist.index(teamName + '\n')
            except ValueError:
                 flag = True
            if flag:
                inFile.seek(0,2)##Goes to the end of the file
                inFile.write(teamName+"\n")
                inFile.close()
            else:
                inFile.close()
                raise SaverLoaderError("The team name is already taken!")
        finally:
            inFile.close()
        outString = [self._convertFromFighter(f)\
                     for f in team.fighters()]
        outString = [self._convertFromTeam(team)]+outString
        outString = "\n".join(outString)
        with open(TEAMFOLDER + teamName + ".dat", "w")\
                as outFile:
            outFile.write(outString)
        

    def _convertFromFighter(self, fighter):
        fSI = fighter.saveInfo()
        return "$".join(nameCheck(fSI[0]), str(fSI[1]),\
                        self._raceTraslatorFrom(fSI[2]),\
                        self._gearTraslatorFrom(fSI[3]),\
                        str(fSI[4]))

    def _convertFromTeam(self, team):
        sT = team.saveInfo()
        return team(sT[0], sT[1], self._raceTranslator(sF[2]))



class gearTranslator:
    """This class allows for the translation of a gear save string
        into the gear, and back.

        This function takes advantage of reference files, GUNREF, ARMORREF
        and AUGMENTREF which will list the guns with all of
        the gun, armor, and augment reference information."""
    def __init__(self, gunFile = GUNREF, armorFile = ARMORREF,
                 augmentFile = AUGMENTREF):
        with open(gunFile) as gFile:
            self._gunFile = gFile.readlines()
        with open(armorFile) as aFile:
            self._armorFile = aFile.readlines()
        with open(augmentFile) as auFile:
            self._augmentFile = auFile.readlines()
        

    def translateTo(self, gearString):
        raise NotImplementedError

    def translateFrom(self, gear):
        raise NotImplementedError
    
