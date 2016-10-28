import pygame, draw
DEFAULTVIEWDIMS = (0, 0, 500, 500)
MINZOOM = 200
EDGEPIXELRANGE = 20
class ZoomError(StandardError):
    pass
class StateError(StandardError):
    pass

class gameViewControl:
    """This class controls the game view"""
    def __init__(self, display, board, bgLayers):
        self._display = display
        self._board = board
        self._bgLayers = bgLayers
        self._boardViewRect = pygame.Rect(display.get_rect())
        self._curZoom = 1
        
        
    def update(self, t, *args, **kwargs):
        board = self._board
##        self._bgLayers.update(t)
##        self._bgLayers.draw(self._display)
        board.update(t, *args, **kwargs)
        bRect = board.get_boardRect() ##this will be a pygame.Rect
        vRect = self._boardViewRect ##this will be a pygame.Rect
        boardSurface = pygame.Surface(bRect.size)
        boardSurface.blit(self._bgLayers, (0, 0))
        board.draw(boardSurface)
        try:
            boardView = boardSurface.subsurface(vRect)
        except ValueError:
            while(not boardSurface.get_rect().contains(vRect)):
                vRect.inflate_ip(-1,-1)
            self._boardViewRect = vRect
            boardView = boardSurface.subsurface(vRect.clip(bRect))
        pygame.transform.smoothscale(boardView,\
                               self._display.get_size(),\
                               self._display)
        
    def zoom(self, zoomBy):
        """Zooms the view in or out.
        zoomBy is the fractional difference in the view window
        after the zoom. e.g.: zoomBy<0 is a zoom in, while
        zoomBy>0 is a zoom out."""
        if zoomBy<=-1:
            raise ZoomError("zoomBy must be greater than -1")
        orig_bVRect = pygame.Rect(self._boardViewRect)
        size = (self._boardViewRect[2]*zoomBy,\
                self._boardViewRect[3]*zoomBy)
        bRect = self._board.get_boardRect()
        self._boardViewRect.inflate_ip(*size)
        self._boardViewRect.clamp_ip(bRect)
        if not bRect.contains(self._boardViewRect):
            self._boardViewRect = orig_bVRect
        elif not all(i>MINZOOM for i in self._boardViewRect.size):
            self._boardViewRect = orig_bVRect
        else:
            self._curZoom += self._curZoom*zoomBy

    def move(self, x, y):
        bRect = self._board.get_boardRect()
        self._boardViewRect.move_ip(x*self._curZoom,\
                                    y*self._curZoom)
        self._boardViewRect.clamp_ip(bRect)

class gameInputControl:
    """This class controls input through an interpreter.
    This is the bare bones base class."""
    def __init__(self, player, board, viewControl):
        self._player = player
        self._board = board
        self._viewControl = viewControl

    def changePlayer(self, newPlayer):
        self._player = newPlayer
        
    def changeboard(self, newboard):
        self._board = newboard
        
    def changeViewControl(self, newViewControl):
        self._viewControl = newViewControl
               

    def onMousePress(self, mouseButton):
        print "you pressed mouse", mouseButton
        return
    
    def onClick(self, mouseButton):
        print "you clicked", mouseButton
        return

    def onDoubleClick(self):
        print "double click!"
        return

    def onMouseOnEdge(self, edgeSections):
        print "mouse is on edges", edgeSections
        return
    
    def onScroll(self, upOrDown):
        """up == 1, down == 0"""
        if upOrDown == 1:
            print "scroll up"
        if upOrDown == 0:
            print "scroll down"
        return
    
    def onDrag(self, mouseMotionEvent):
        print "you dragged", mouseMotionEvent.rel,\
                               mouseMotionEvent.pos
        return
    
    def onKeyPress(self, key):
        print "you pressed the key", key
        return

    def onKeyHold(self, key):
        print "you are holding the key", key
        return

    def onStartDragging(self, mouseButton):
        print "you started dragging with mouse", mouseButton
        
    def onStopDragging(self, mouseButton):
        print "you stopped dragging with mouse", mouseButton

##    def onKeyHoldToDrag(self, keyPressed):
##        return
class makeType_gIC(gameInputControl):
    """This is an abstract class for
    state wrappers for gameInputControl."""
    def __init__(self, gameInputControl):
        self._player = gameInputControl._player
        self._board = gameInputControl._board
        self._viewControl = gameInputControl._viewControl
        
class makeBoard_gIC(makeType_gIC):
    """Wrapper for gameInputControl.
    This makes the current gameInputControl
    into a controller for the Board.
    Implements gameInputControl. """

    def onMousePress(self, mouseButton):
        print "you pressed mouse", mouseButton
        return
    
    def onClick(self, mouseButton):
        print "you clicked", mouseButton
        return

    def onDoubleClick(self):
        print "double click!"
        return

    def onMouseOnEdge(self, edgeSections):
        print "mouse is on edges", edgeSections
        return
    
    def onScroll(self, upOrDown):
        """up == 1, down == 0"""
        if upOrDown == 1:
            self._viewControl.zoom((1.1**-1)-1)
        if upOrDown == 0:
            self._viewControl.zoom(.1)
        return
    
    def onDrag(self, mouseMotionEvent):
        self._viewControl.move(-mouseMotionEvent.rel[0],\
                               -mouseMotionEvent.rel[1])
        return
    
    def onKeyPress(self, key):
        print "you pressed the key", key
        return

    def onKeyHold(self, key):
        print "you are holding the key", key
        return

    def onStartDragging(self, mouseButton):
        print "you started dragging with mouse", mouseButton
        
    def onStopDragging(self, mouseButton):
        print "you stopped dragging with mouse", mouseButton

class gameInputInterpreter:
    """This class interprets game input."""
    def __init__(self, player, board, viewControl,\
                 state="board", doubleClickDelay=250, holdDelay = 150):
        self._gIC = gameInputControl(player, board, viewControl)
        self.changeState(state)
        self._dCdelay = doubleClickDelay
        self._holdDelay = holdDelay
        self._lastMouseHoldTime = 0
        self._lastKeyHoldTime = 0
        self._mousePressed = None
##        self._mousePressedLastFrame = False
        self._mouseHeldInDelay = False
        self._LMouseUpInDelay = False
##        self._keyPressed = None
        self._dragging = False
        self._doubleClicked = False
        self._lastDoubleClick = 0
        self._DCBlock = False

    def changeState(self, newState):
        if newState == "board":
            self._gIC = makeBoard_gIC(self._gIC)
        else:
            raise StateError("There is no state " + str(newState))

    def updateInput(self, t):
        events = pygame.event.get()
        pygame.event.clear()
        if self._mouseHeldInDelay == True\
           and (t - self._lastMouseHoldTime\
                    >=self._holdDelay)\
            and not self._dragging:
            self._gIC.onStartDragging(self._mousePressed) 
            self._dragging = True
        if (t - self._lastDoubleClick\
            >= self._dCdelay) and self._DCBlock:
            self._DCBlock = False
            self._doubleClicked = False
        for ev in events:
            if pygame.MOUSEBUTTONDOWN\
               == ev.type:
                if ev.button == 4:
                    self._gIC.onScroll(1)
                if ev.button == 5:
                    self._gIC.onScroll(0)
                self._mousePressed = ev.button
##                self._mousePressedLastFrame = True
                if self._LMouseUpInDelay and\
                    (t - self._lastMouseHoldTime\
                    <self._dCdelay):
                    if not self._DCBlock:
                        self._doubleClicked = True
                    self._LMouseUpInDelay = False
                else:
                    self._LMouseUpInDelay = False
                    self._gIC.onMousePress(self._mousePressed)
                self._mouseHeldInDelay = True
                self._lastMouseHoldTime = t
            if pygame.MOUSEBUTTONUP\
               == ev.type:
                if self._doubleClicked and not self._DCBlock:
                    self._gIC.onDoubleClick()
                    self._doubleClicked = False
                    self._lastDoubleClick = t
                    self._DCBlock = True
                elif not self._doubleClicked and\
                     not self._dragging:
                    self._gIC.onClick(ev.button)
                elif self._dragging:
                    self._gIC.onStopDragging(ev.button)
                if self._mouseHeldInDelay and\
                   ev.button == 1:
                    if t - self._lastMouseHoldTime\
                       <self._dCdelay:
                        self._LMouseUpInDelay = True
                self._mouseHeldInDelay = False
                self._dragging = False
            if pygame.KEYDOWN\
               == ev.type:
                self._lastKeyHoldTime = t
##                self._keyPressed = ev.key
                self._gIC.onKeyHold(ev.key)
            if pygame.KEYUP\
               == ev.type:
                self._gIC.onKeyPress(ev.key)
            if pygame.MOUSEMOTION\
               == ev.type:
                if self._dragging:
                    self._gIC.onDrag(ev)
        onEdges = self.get_mouseOnEdges()
        if onEdges != []:
            self._gIC.onMouseOnEdge(onEdges)

    def get_mouseOnEdges(self):
        return []
            
            
                    
##            else:
##                if self._mousePressedLastFrame:
                    
