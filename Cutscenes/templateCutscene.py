#templateCutscene.py and minTemplateCutscene.py are excluded from running on startup, so copy+paste either file and change the name to let it run.


#References to objects are stored in prop, a dictionary put in every paramater under the following names:
# The player character:         "char"
# The current platform data:    "plat"
# The current player inputs:    "input"
#Use prop[{name}] to access that reference

#Some useful properties of objects:
# char: allowControl, x, y, xl/ yl (length), gr (grounded), xv/ yv (velocitiy)
# 

#setting allowControl to False will still register inputs and are still useable, but will prevent them from being used to move the character.

#EVERY FUNCTION MUST HAVE EXACTLY ONE PARAMATER, EVEN IF IT WILL GO UNUSED

#Runs when cutscene is started
def start(prop) -> None:
    character = prop["char"]
    character.allowControl = False

#Runs every frame after started
def update(prop) -> None:
    character = prop["char"]
    character.yv = -10
    pass

#Runs when cutscene ends 
def end(prop) -> None:
    character = prop["char"]
    character.allowControl = True


#If no cutscene active, run every frame to check whether to start function
#RETURN EITHER DICT WITH TEMPLATE BELOW OR BOOL FOR CUSTOM START CONDITIONS
def startCheck(prop) -> bool or dict:
    return {
        "trigger": False,
        "triggerHitbox": {
            "x": 0,
            "y": 0,
            "xl": 0,
            "yl": 0,
            }
        }

#If cutscene is active, runs once per frame to determine whether to end cutscene
#RETURN A BOOL VALUE
#ONLY USE CONDITIONALS AND RETURN, ALL OTHER CODE PUT INTO end()
def endCheck(prop) -> bool:
    if prop["char"].y < -100:
        return True
    return False

#Feel free to add whatever other functions to execute, but remember that only these four are called by the main script. All others defined will only be used by you.