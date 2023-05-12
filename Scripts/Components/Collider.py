from Scripts.componentManager import newComponent
# pyright: reportGeneralTypeIssues=false


@newComponent
class Collider():
    """Used to check as to whether the selected item is colliding with an object
    This will NOT handle physics, incase it should be used as a collisionless trigger that has an
    activation area. If you want to add physical collisions, use this in tangent with RigidBody
    It works by having a tag or set of tags in which it can collide with"""
    from Scripts.Components.components import Transform as te
    requiredDependencies={ "Transform": te }

    class Hitbox():
        def __init__(self,
                transform,
                offset,
                xLength:int, yLength:int,
                ) -> None:
            self.Transform = transform
            self.collideList = []
            self.xLength = xLength
            self.yLength = yLength

        def check(self, item):
            s = self.Transform
            i = item.Transform
            if  i.yPos +  item.yLength >= s.yPos \
            and i.yPos <= self.yLength +  s.yPos \
            and i.xPos +  item.xLength >= s.xPos \
            and i.xPos <= self.xLength +  s.xPos :
                return True
            return False

    def Start(self,
        xLength:int=50, yLength:int=50,
        hitboxs:set|str='BoxCollider',
        collisionTags:set=set(),
        ) -> None:

        self.Transform = self.parent.Transform
        BoxCollider = {
        Collider.Hitbox( #overall
            self.Transform,
            self.Transform.Vector(0, 0),
            xLength, yLength
            ),
        Collider.Hitbox( #top
            self.Transform,
            self.Transform.Vector(0, 0),
            xLength, yLength/2
            ),
        Collider.Hitbox( #bottom
            self.Transform,
            self.Transform.Vector(0, yLength/2),
            xLength, yLength/2
            ),
        Collider.Hitbox( #left
            self.Transform,
            self.Transform.Vector(0, 0),
            xLength/2, yLength
            ),
        Collider.Hitbox( #right
            self.Transform,
            self.Transform.Vector(xLength/2, 0),
            xLength/2, yLength
            ),
        }

        defaultHitboxTypes = {
            'BoxCollider': BoxCollider
        }

        self.xLength = xLength
        self.yLength = yLength
        if isinstance(hitboxs, str):
            if hitboxs in defaultHitboxTypes:
                hitboxs = defaultHitboxTypes[hitboxs]
            else:
                hitboxs = defaultHitboxTypes['BoxCollider']
        else:
            self.hitboxs = hitboxs
        self.collideList: list[tuple[object, list[bool]]] = []
        self.collisionTags=collisionTags

    def Update(self) -> None:
        self.collideList = []
        if self.active == False: return
        

        for tag in self.collisionTags:
            for object in self.scene.SceneTags[tag]: # type: ignore
                if not 'Collider' in object.Components: continue
                if object.Collider.active == False: continue
                
                Colliding = False
                for checkingHitbox in self.hitboxs:
                    if checkingHitbox.active == False: continue
                    for questioningHitbox in object.Collider.hitboxs:
                        if questioningHitbox.active == False: continue

                        if checkingHitbox.check(questioningHitbox):
                            Colliding = True
                            checkingHitbox.collideList.append(questioningHitbox)

                if Colliding:
                    self.collideList.append(object)


@newComponent
class RigidBody():
    """Used to handle collisions, gravity and other physical forces
    Use with a Collider to properly collide with other objects that have Colliders 
    mass = weight of object
    grounded = is touching ground and is unaffected by gravity until leaving ground again. 
    """
    from Scripts.Components.components import Transform
    requiredDependencies={
    "Transform": Transform, 
    "Collider": Collider
    }


    def Start(self, mass:int=0) -> None:
        self.mass = mass
        self.grounded = False
    
    def Update(self) -> None:
        if not self.grounded:
            if self.parent.Transform.yVel < self.mass:
                self.parent.Transform.yVel += self.mass / 10
                if self.parent.Transform.yVel > self.mass:
                    self.parent.Transform.yVel = self.mass

        self.grounded = False
        for i in self.parent.Collider.collideList:
            item, lis = i
            if lis[1]:
                self.grounded = True
                self.parent.transform.yVel = 0
                self.parent.transform.yPos = item.yPos - self.Collider.yLength
            if lis[2]:
                self.parent.transform.yVel = 0
                self.parent.transform.yPos = item.yPos + item.Collider.yLength
            if lis[3]:
                self.parent.transform.xVel = 0
                self.parent.transform.xPos = item.xPos + self.Collider.xLength
            if lis[4]:
                self.parent.transform.xVel = 0
                self.parent.transform.xPos = item.yPos - item.Collider.yLength