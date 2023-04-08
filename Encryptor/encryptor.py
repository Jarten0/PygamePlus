"""from Scripts.componentManager import newComponent
from main import *
from main import Object, Component

@newComponent
class EncryptionManager():
    runOnStart = True
    def init(self):
        buttons = {
            'start': [0,50,0,0,0,100,100]
        }

        self.buttonList: dict[str, object] = {}
        for i in buttons:
            self.buttonList[i] = Object.new(i, Button, True, *buttons[i])

    def update(self):
        print(self.buttonList)
        updateObjectsInList(self.buttonList)

@newComponent
class Button():
    import Scripts.Components.components as cmp
    requiredDependencies = {
        'Transform' : cmp.Transform,      
        'Renderer'  : cmp.Renderer,      
        'Collider'  : cmp.Collider,      
    }
    @classmethod
    def create(cls,
        x, y, z=0, xo=0, yo=0, xl=128, yl=128, t=0,
                *args, **kwargs):
        Transform = Component.new('components\\Transform',
            xPosition=x,
            yPosition=y,
            zPosition=z,
            )
        Renderer  = Component.new('components\\Renderer', 
            Transform = Transform,  
            xOffset=xo,
            yOffset=yo,
            xLength=xl,
            yLength=yl,
            path="\\Assets\\Images\\Button.png",
            tier=t,
            )
        Collider  = Component.new('components\\Collider',
            Transform = Transform,
            xLength = xl,
            yLength = yl,
            ) 
        return cls, "Button", {
            'Transform': Transform,
            'Renderer': Renderer,
            'Collider': Collider,
        }
    
    def init(self, *args, Transform, Renderer, Collider):
        self.Transform = Transform      
        self.Renderer = Renderer  
        self.Collider = Collider
        self.pressed = False

    def update(self):
        Mouse = Object.get('Mouse')
        if 'Mouse' in self.Collider.collideList and Mouse.down: # type: ignore
            self.pressed = True
            print("Click!")
        else: self.pressed = False


"""




class Ec():
    @classmethod
    def encrypt(cls, input_:str='1234'):        
        import time
        initialInputList = list(input_)
        IntList=[]
        PsuedoRandomizedList=[]
        for i in range(len(initialInputList)): 
            IntList.append( int(initialInputList[i]))
        for i in range(len(IntList)):
            PsuedoRandomizedList.append((IntList[i]+7)%10)
        PsuedoRandomizedList[0], PsuedoRandomizedList[2] = PsuedoRandomizedList[2], PsuedoRandomizedList[0]
        PsuedoRandomizedList[1], PsuedoRandomizedList[3] = PsuedoRandomizedList[3], PsuedoRandomizedList[1]
        strEncryptedList = str(PsuedoRandomizedList).replace("'", '').replace(" ", '').replace(",", '').removeprefix('[').removesuffix(']')
        with open('log.txt', 'r') as rf:
            prevFile = rf.read()
            print(prevFile)
            with open('log.txt', 'w') as f:
                f.write(f"Encrypted {input_} at time "+str(int(time.time()))+" to: "+strEncryptedList+"\n")
                f.write(prevFile)
                f.close()
        return strEncryptedList

    @classmethod
    def decrypt(cls, input_:str='0189'):
        import time
        initialEncryptedList = list(str(input_))
        intEncryptedList:list[int]=[]
        for i in range(len(initialEncryptedList)): 
            intEncryptedList.append( int(initialEncryptedList[i]))
        intDecryptedList:list[int] = [intEncryptedList[2], intEncryptedList[3], intEncryptedList[0], intEncryptedList[1]]
        strDecryptedList:str = ''
        for i in range(len(intDecryptedList)):
            strDecryptedList += str((intDecryptedList[i]+3)%10)
        with open('log.txt', 'r') as rf:
            with open('log.txt', 'w') as f:
                prevFile = rf.read()
                print(prevFile)
                f.write(f"Decrypted {input_} at time "+str(int(time.time()))+" to: "+strDecryptedList+"\n")
                f.write(prevFile)
                f.close()
        return strDecryptedList
print(Ec.encrypt("1773"))
print(Ec.decrypt(Ec.encrypt("1773")))