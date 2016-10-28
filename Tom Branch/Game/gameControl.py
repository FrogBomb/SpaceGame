import pygame, draw
DEFAULTVIEWDIMS = (0, 0, 500, 500)
MINZOOM = 200
EDGEPIXELRANGE = 20
DEFAULTZOOM = 1.1
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
        if zoomBy<=0:
            raise ZoomError("zoomBy must be greater than 0")
        zoomBy = zoomBy - 1
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

class inputControl:
    """This class controls input through an interpreter.
    This is the bare bones base class."""
    def __init__(self, **kwargs):
        self.attributes = kwargs

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
class makeType_gIC(inputControl):
    """This is an abstract class for
    state wrappers for gameInputControl."""
    def __init__(self, gameInputControl, **newAttributes):
        self.attributes = gameInputControl.attributes
        for key in newAttributes.iterkeys():
            self.attributes[key] = newAttributes[key]
        self._linkAttributes()
    def _linkAttributes(self):
        return
        
class makeBoard_gIC(makeType_gIC):
    """Wrapper for inputControl.
    This makes the current gameInputControl
    into a controller for the Board.
    Implements gameInputControl. """
    
    def _linkAttributes(self):
        self._player = self.attributes["player"]
        self._board = self.attributes["board"]
        self._viewControl = self.attributes["viewControl"]
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
            self._viewControl.zoom(DEFAULTZOOM**-1)
        if upOrDown == 0:
            self._viewControl.zoom(DEFAULTZOOM)
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

class inputInterpreter:
    """This class interprets input"""
    def __init__(self, state="board", doubleClickDelay=250, holdDelay = 150,\
                 **kwargs):
        self._gIC = inputControl(**kwargs)
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
        self._holding = False
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
                    break
                if ev.button == 5:
                    self._gIC.onScroll(0)
                    break
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
                self._holding = True
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
                self._holding = False
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
                elif self._holding:
                    self._gIC.onStartDragging(self._mousePressed)
                    self._dragging = True
        onEdges = self.get_mouseOnEdges()
        if onEdges != []:
            self._gIC.onMouseOnEdge(onEdges)

    def get_mouseOnEdges(self):
        return []
    
class gameInputInterpreter(inputInterpreter):
    """This class interprets game input."""
    def __init__(self, player, board, viewControl,\
                 state="board", doubleClickDelay=250, holdDelay = 150):
        inputInterpreter.__init__(self, state, doubleClickDelay, holdDelay,\
                         player= player, board =board,\
                        viewControl= viewControl)


