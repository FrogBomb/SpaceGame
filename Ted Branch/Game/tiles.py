class BoardError(StandardError):
    pass

class tile:
    """This is the tile class.
        tileType is a string designating the tile type.
        health is how much health this tile is given
        wallValues is a length 6 list designating
            the type of walls around the tile.
            This is the index of the wall in
            the wallList of the board."""
    def __init__(self, tileType, health, wallValues):
        if type(tileType)!=str:
            raise TypeError("tileType must be a string")
        if type(health) != int:
            raise TypeError("health must be an int")
        if type(wallValues) != list or len(wallValues)!=6:
            raise TypeError("wallValues must be a length 6 list")
        self._type = tileType
        self._damage = damage
        self._wallValues = wallValues
        self._destroyed = False
        self._occupiedBy = None
        
    def takeDamage(self, damage):
        self._damage-=damage
        if self._damage<=0:
            self._damage = 0
            self._destroyed = True

    def destroy(self):
        self._damage = 0
        self._destroyed = True

    def getType(self):
        return self._type

    def getWallValues(self):
        return self._wallValues
    
    def isDestroyed(self):
        return self._destoryed

    def moveTo(self, fighter):
        self._occupiedBy = fighter

    def moveFrom(self):
        self._occupiedBy = None
        
class board:
    """This is the game board.
        rows and cols are the dimentions of the board
        tiles is a list of tiles.
        wallList is the list of walls that can appear on a tile.
        skinType tells what the board's skin is.
        fighterList is a list of all the fighters."""
    def __init__(self, rows, cols, tiles = None, wallList = None,
                 skinType = None, teams = None, fighterList = None):
        self._numRows = rows
        self._numCols = cols
        self._skinType = skinType
        self._fighterList = fighterList
        if wallList == None:
            self._wallList = []
        elif not all(isinstance(w, wall) for w in wallset):
            raise TypeError("wallset must only contain walls.")
        else:
            self._wallList = list(wallList)
        if teams == None:
            self._teams = []
        elif not all(isinstance(t, team )for t in teams):
            raise TypeError("teams must only contain teams.")
        else:
            self._teams = list(teams)
        if fighterList == None:
            self._fighterList = []
        elif not all(isinstance(f, fighter) for f in fighterList):
            raise TypeError("teams must only contain teams.")
        else:
            self._fighterList = list(fighterList)
        if tiles == None:
            data = [tile('0', 0, '000000')]*rows*cols
        if not all(isinstance(t, tile) for t in tiles):
            raise TypeError("tiles must be a list of tiles.")
        if len(tiles)>rows*cols:
            raise BufferError("data must be able to fit in the matrix")
        else:
            self._data = list(data) + [tile('0', 0, '000000')]*(rows*cols-len(data))
    
    def __getitem__(self, key):
        if type(key) == int:
            return self._data[key]
        elif type(key) == tuple:
            if len(key) == 2:
                if (key[0]<self._numRows)&(key[1]<self._numCols)&(key[0]>=0)&(key[1]>=0):
                    return self._data[self._numCols*key[0] + key[1]]
                else:
                    raise IndexError("list index out of range")
        raise TypeError("Key must be an int or two ints separated by a comma")

    def __setitem__(self, key, value):
        if not isinstance(value, tile):
            raise TypeError("The value must be a tile.")
        if type(key) == int:
            self._data[key] = value
            return
        if type(key) == tuple:
            if len(key) == 2:
                if (key[0]<self._numRows)&(key[1]<self._numCols)\
                   &(key[0]>=0)&(key[1]>=0):
                    self._data[self._numCols*key[0] + key[1]] = value
                    return
                else:
                    raise IndexError("list index out of range")
        raise TypeError("Key must be an int or two ints separated by a comma")

    def tileCoordinates(self, tile):
        index = self._data.index(tile)
        row = index/self._numCols
        col = index%self._numCols
        return row, col

    def fighterTile(self, fighter):
        fighterT = None
        for t in self._data:
            if t._occupiedBy == fighter:
                fighterT = t
                break
        return fighterT

    def dims(self):
        return self._numRows, self._numCols

    def getSkin(self):
        return self._skinType
    
    def getWallList(self):
        return self._wallList

    def getFighterList(self):
        return self._fighterList

    def moveFighter(self, fighter, toTile):
        if not any(fighter == f for f in self._fighterList):
            raise BoardError("Fighter must be on the board to move it.")
        fighterTile = self.fighterTile(fighter)
        fighterTile.moveFrom()
        toTile.moveTo(fighter)
        fighter.moveFromto(self.tileLocation(fighterTile),\
                           self.tileLocation(toTile))

    def adjacentTileCoords(self, tileCoords, direction):
        row, col = tileCoords
        if direction == "up":
            row-=2
        elif direction == "down":
            row+=2
        elif direction == "upL":
            if row%2 == 0:
                row-=1
                col-=1
            else:
                row-=1
        elif direction == "upR":
            if row%2 == 0:
                row-=1
            else:
                row-=1
                col+=1
        elif direction == "downL":
            if row%2 == 0:
                row+=1
                col-=1
            else:
                row+=1
        elif direction == "downR":
            if row%2 == 0:
                row+=1
            else:
                row+=1
                col+=1
        return row, col

class wall:
    def __init__(self, blocking, wallType):
        self._blocking = blocking
        self._type = wallType
        
    def getBlocking(self):
        return self._blocking

    def getType(self):
        return self._type
