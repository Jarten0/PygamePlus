# pyright: reportGeneralTypeIssues=false

from main import Component, newPrefab

@newPrefab
class Character():
    def init(self) -> object:
        ConfigData = self.newComponent('components\\ConfigData',
            dirFileName = 'CharacterProperties',
            fileType = "toml"
            )
        Transform = self.newComponent('components\\Transform',
            xPos=ConfigData.configFile["body"]["xpos"],     # type: ignore
            yPos=ConfigData.configFile["body"]["ypos"],     # type: ignore
            zPos=ConfigData.configFile["body"]["zpos"],     # type: ignore
            )
        Renderer = self.newComponent('Renderer\\Renderer',
            Transform = Transform,  
            color = (255, 0,0),
            xOffset=0,
            yOffset=0,
            xLength=50,
            yLength=20,
            path="\\Assets\\Images\\hehe.png",
            tier=5,
            )
        Collider = self.newComponent('Collider\\Collider',
            Transform = Transform,
            xLength = 0,
            yLength = 20,
            )
        RigidBody = self.newComponent('Collider\\RigidBody',
            Transform = Transform,    
            Collider = Collider,    
            mass = 5,
            )
        Character = self.newComponent('character\\Character',
            ConfigData = ConfigData,    
            Transform = Transform,      
            Renderer  = Renderer,      
            Collider  = Collider,      
            RigidBody = RigidBody,
        )
        return {
            'Character': Character,
            'ConfigData': ConfigData,
            'Transform': Transform,
            'Renderer': Renderer,
            'Collider': Collider,
            'RigidBody': RigidBody
            }