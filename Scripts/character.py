import Scripts.boards as Boards
import Scripts.cameramanager as cam
from Scripts.timer import Timer 
import Scripts.components as Component
import tomllib, os
#import main
colors = {
    "red":   (255,0,  0  ),
    "green": (0,  255,0  ),
    "blue":  (0,  0,  255),
    "gray":  (30, 30, 30 ),
}
class create():
    def __init__(self):
        self.ConfigData = Component.ConfigData(
            "characterProperties"
        )
        self.Transform = Component.Transform(
            xPosition = self.ConfigData.configFile['body']['xpos'],
            yPosition = self.ConfigData.configFile['body']['ypos'],
            zPosition = 0,
            xVelocity = 0,
            yVelocity = 0,
            zVelocity = 0,
        )
        self.Collider = Component.Collider(
            xLength=self.ConfigData.configFile['body']['xlength'],
            yLength=self.ConfigData.configFile['body']['ylength'],
            xOffset=0,
            yOffset=0,
        )
        self.RigidBody = Component.RigidBody(
            mass=0,
        )
        self.Renderer = Component.Renderer(
            xLength=10,
            yLength=10,
            xOffset=0,
            yOffset=0,
            path=r"\Assets\Images\hehe.png",
        )
        self.Controller = Component.Controller(

        )
        self.CharacterController = Component.CharacterManager(
            {
            "Transform": self.Transform,
            "Renderer": self.Renderer,
            "ConfigData": self.ConfigData,
            }
        )
