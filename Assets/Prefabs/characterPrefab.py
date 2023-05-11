# pyright: reportGeneralTypeIssues=false

from main import newPrefab

@newPrefab
class Character():
    def Start(self) -> object:
        self.newComponent('components\\ConfigData',
            dirFileName = 'CharacterProperties',
            fileType = "toml")
        self.newComponent('components\\Transform',
            xPos=self.ConfigData.configFile["body"]["xpos"],
            yPos=self.ConfigData.configFile["body"]["ypos"],     
            zPos=self.ConfigData.configFile["body"]["zpos"])
        self.newComponent('Renderer\\Renderer',
            color = (255, 0,0),
            xOffset=0,
            yOffset=0,
            xLength=50,
            yLength=20,
            path="\\Assets\\Images\\hehe.png",
            tier=5)
        self.newComponent('Collider\\Collider',
            xLength = 0,
            yLength = 20)
        self.newComponent('Collider\\RigidBody',
            mass = 5)
        self.newComponent('character\\Character')
