import pygame as pyg
import Scripts.Components.components as MainComponent
import Scripts.Components.character  as CharacterComponent
from Scripts.componentManager   import *
from Scripts.timer          import Timer
from Scripts.boards         import Boards
from Scripts.inputMapper    import Input
from Main   import *


def _init() -> None:
    global _Settings, _level, _xOffset, _yOffset,_xDefault, _yDefault, _focusPoint

    _Settings:dict = Main.Settings
    _xOffset:float = 0
    _yOffset:float = 0
    _level:  Main.Level|None = None
    _focusPoint: object|None = None
    _focusPoint.Transform = Components.new()

def _setFocusPoint(_obj:object|None = None, xPos:float=0, yPos:float=0):
    if isinstance(_obj, None):
        _focusPoint.Transform.xPosition = xPos
        _focusPoint.Transform.yPosition = yPos
    else:
        _focusPoint.Transform = _obj

def _update() -> None:
    if Input.getHeld("LEFT"):
        _xOffset -= 10
    elif Input.getHeld("RIGHT"):
        _xOffset += 10
    if Input.getHeld("UP"):
        _yOffset -= 10
    elif Input.getHeld("DOWN"):
        _yOffset += 10

    if Input.getHeld("up") or Input.getHeld("down") or Input.getHeld("left") or Input.getHeld("right"):
        _xOffset = 0
        _yOffset = 0


    
    _xPosition = _focus + _xOffset
    _yPosition = ydefault + _yOffset

    
    if _xPosition < 0:
        _xPosition = 0
    elif _xPosition > _level.xLength - _Settings['screen_width']:
        _xPosition = _level.xLength - _Settings['screen_width']




class Camera():
    init = _init
    update = _update
    setFocusPoint = _setFocusPoint