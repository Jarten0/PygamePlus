import pygame as pyg
import Scripts.Components.components as MainComponent
from Scripts.timer import Timer
from Scripts.boards import Boards
from Scripts.inputMapper  import Input
from Scripts.componentManager import *
from main import *
from Scripts.componentManager import ComponentTools as comTools

@comTools.classWrapper
class devTools():

    def create(): pass
        
    @comTools.initWrapper
    def initialization__(self):
        pass