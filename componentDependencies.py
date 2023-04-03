from main import Object, Component

from Scripts.Components.character import Character
from Scripts.Components.components import Renderer
from Scripts.Components.components import ConfigData
from Scripts.Components.components import Collider
from Scripts.Components.components import Mouse
from Scripts.Components.components import DependenciesTemplate
from Scripts.Components.components import RigidBody
from Scripts.Components.components import Transform
from Scripts.Components.platforms import Platform

Object.new(name_='Character Object', class_=Character, addToList_=False,
	#No Dependencies
	#No Arguments

)
Object.new(name_='Renderer Object', class_=Renderer, addToList_=False,
	#Dependencies
    Transform    = Transform(),
	#Arguments
    path         = '',        #<class 'str'>
    tier         = 3,        #<class 'int'>
    xOffset      = 0.0,        #<class 'float'>, #Optional
    yOffset      = 0.0,        #<class 'float'>, #Optional
    xLength      = 0.0,        #<class 'float'>
    yLength      = 0.0,        #<class 'float'>
    color        = (30, 30, 30),        #<class 'tuple'>
    surface      = 'Surface(128x128x32 SW)',        #<class 'pygame.Surface'>
    alpha        = 0.0,        #<class 'float'>
    surfaceRows  = 1,        #<class 'int'>
    surfaceColumns = 1,        #<class 'int'>
    autoCulling  = True,        #<class 'bool'>

)
Component.new(ConfigData,
	#No Dependencies
	#No Arguments

)
Component.new(Collider,
	#Dependencies
    Transform    = Transform(),
	#No Arguments

)
Component.new(Mouse,
	#No Dependencies
	#No Arguments

)
Component.new(DependenciesTemplate,
	#No Dependencies
	#No Arguments

)
Component.new(RigidBody,
	#Dependencies
    Transform    = Transform(),
    Collider    = Collider(Transform = Transform()),
	#No Arguments

)
Component.new(Transform,
	#No Dependencies
	#Arguments
    xPosition = 0.0,        #<class 'float'>, #Optional
    yPosition = 0.0,        #<class 'float'>, #Optional
    zPosition = 0,        #<class 'int'>, #Optional
    xVelocity = 0.0,        #<class 'float'>, #Optional
    yVelocity = 0.0,        #<class 'float'>, #Optional
    rotation = 0.0,        #<class 'float'>, #Optional

)
Object.new(name_='Platform Object', class_=Platform, addToList_=False,
	#Dependencies
    Transform    = Transform(),
    Collider    = Collider(Transform = Transform()),
	#No Arguments

)
