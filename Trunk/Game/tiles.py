import pygame, spriteHelper
class BoardError(StandardError):
    pass
TILESIZE = (100, 66) ##(Width, Hight)
TILEFILETYPE = "bmp"
TILECOLORKEY = (0, 255, 255)
class tile(pygame.sprite.GroupSingle):
    """This is the tile class.
        tileType is a string designating the tile type.
        health is how much health this tile is given
        wallValues is a length 6 list designating
            the type of walls around the tile.
            This is the index of the wall in
            the wallList of the board."""
    def __init__(self, tileType, health, walls):
        pygame.sprite.GroupSingle.__init__(self)
        if type(tileType)!=int:
            raise TypeError("tileType must be a int")
        if type(health) != int:
            raise TypeError("health must be an int")
        if type(walls) != list or len(walls)!=6:
            raise TypeError("wallValues must be a length 6 list")
        self._type = tileType
        self._damage = health
        self._walls = walls
        self._destroyed = False
        self._occupiedBy = None
        self.add(pygame.sprite.Sprite())
        
    def takeDamage(self, damage):
        self._damage-=damage
        if self._damage<=0:
            self._damage = 0
            self._destroyed = True
            
    def add(self, sprite):
        pygame.sprite.GroupSingle.add(self, sprite)
        sprite.update(0, self._type)

    def destroy(self):
        self._damage = 0
        self._destroyed = True

    def getType(self):
        return self._type
    
    def changeType(self, tileType):
        self._type = tileType
        self.sprite().update(0, self._type)

    def getWalls(self):
        return self._walls
    
    def isDestroyed(self):
        return self._destoryed

    def moveTo(self, fighter):
        self._occupiedBy = fighter

    def moveFrom(self):
        self._occupiedBy = None
        
class board(pygame.sprite.LayeredUpdates):
    """This is the game board.
        rows and cols are the dimentions of the board
        tiles is a list of tiles.
        wallList is the list of walls that can appear on a tile.
        skinType tells what the board's skin is.
        fighterList is a list of all the fighters."""

    
    def __init__(self, rows, cols, tiles = None, wallList = None,
                 skinType = None, teams = None, fighterList = None):
        pygame.sprite.LayeredUpdates.__init__(self)
        self._numRows = rows
        self._numCols = cols
        self._skinType = None
        self._fighterList = fighterList
        self._tileImages = None
##        self.image = pygame.Surface((rows*(3*TILESIZE[0]/4)+TILESIZE[0]/4,\
##                                      cols*TILESIZE[1] + TILESIZE[1]/2))
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
            raise TypeError("fighterList must only contain fighters.")
        else:
            self._fighterList = list(fighterList)
        if tiles == None:
            tiles = [tile(0, 0, [0]*6) for i in range(rows*cols)]
        if not all(isinstance(t, tile) for t in tiles):
            raise TypeError("tiles must be a list of tiles.")
        if len(tiles)>rows*cols:
            raise BufferError("data must be able to fit in the matrix")
        else:
            self._data = list(tiles) + [tile(0, 0, [0]*6) for i\
                                        in range(rows*cols-len(tiles))]
        self.uploadSkinset(skinType)
        

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

    def tileDrawLocation(self, tile):
        row, col = self.tileCoordinates(tile)
        curX = col*3*TILESIZE[0]/4 ##75
        curY = row*TILESIZE[1] ##66
        if col%2 == 1:
            curY += TILESIZE[1]/2 ##33
        return curX, curY

    def uploadSkinset(self, skinType):
        if self._skinType == skinType:
            return
        self.skinType = skinType
        if self._tileImages != None:
            self.empty()
            for r in self._tileImages:
                for i in self._tileImages:
                    del i
        self._tileImages = spriteHelper.load_tiles(TILESIZE[0], TILESIZE[1],\
                                                   skinType,\
                                             TILEFILETYPE)
        for r in self._tileImages:
            for i in r:
                i.set_colorkey(TILECOLORKEY)
        for t in self._data:
            sprite = spriteHelper.tileSprite(self._tileImages,\
                                             self.tileDrawLocation(t))
            t.add(sprite)
            self.add(sprite)
        for f in self._fighterList:
            self.add(f.sprite()) 

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
        if direction == "up" or direction == 0:
            row-=2
        elif direction == "down" or direction == 3:
            row+=2
        elif direction == "upL" or direction == 1:
            if row%2 == 0:
                row-=1
                col-=1
            else:
                row-=1
        elif direction == "upR" or direction == 5:
            if row%2 == 0:
                row-=1
            else:
                row-=1
                col+=1
        elif direction == "downL" or direction == 2:
            if row%2 == 0:
                row+=1
                col-=1
            else:
                row+=1
        elif direction == "downR" or direction == 4:
            if row%2 == 0:
                row+=1
            else:
                row+=1
                col+=1
        return row, col

    def get_boardRect(self):
        botRightTile = self[-1]
        TRect = botRightTile.sprite.rect
        if self._numCols%2 == 1:
            return pygame.Rect(0, 0, TRect[0]+TRect[2],\
                               TRect[1]+TRect[3]+TILESIZE[1]/2)
        else:
            return pygame.Rect(0, 0, TRect[0]+TRect[2],\
                               TRect[1]+TRect[3])
    def getTileAt(self, pos):
        sprites = self.get_sprites_at(pos)
        tiles = []
        for s in sprites:
            if isinstance(s, spriteHelper.tileSprite):
                groups = s.groups
                for g in groups:
                    if isinstance(g, tile):
                        tiles.append(g)
        if len(tiles)>1:
            curMinDis = sum((tiles[0].rect.center[i]-pos[i])**2\
                            for i in range(2))
            curBestTile = tiles[0]
            for t in tiles:
                canDis = sum((t.rect.center[i]-pos[i])**2\
                             for i in range(2))
                if canDis<curMinDis:
                    curMinDis = canDis
                    curBestTile = t
            return t
        elif len(tiles)==1:
            return tiles[0]
        else:
            return None
        

class wall:
    def __init__(self, blocking, location, wallType):
        self._blocking = blocking
        self._type = wallType
        self._location = location
        
    def getBlocking(self):
        return self._blocking

    def getType(self):
        return self._type

def findWallHits(lineData):
    return
