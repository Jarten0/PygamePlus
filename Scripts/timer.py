"""Timer interface for setting and getting timers. Manages the timers automatically.
    
    \nFor best explanation, read on afterward, but in simplest terms, the methods are: 
\n    setInc(name, initialValue=60) to start a timer, 
\n    getInc(name) to stop a timer and return result, 
\n    setDec(name, initialValue=0) to start a stopwatch, 
\n    getDec(name) to see if a stopwatch is finished and stop it if so, 
\n    getValue(name, inc=True|False) to check on how a timer is doing.
    
    \nThere are two types of timers you can set: Incremental and Decremental. Incremental goes up on every frame while Decremental goes down on every frame.
    \nTo set a timer, use Timer.setInc or Timer.setDec depending on what kind of timer you want. Then, to get the result of the timer use Timer.getInc or
Timer.getDec to get the results of the timer you had set earlier. You can also use Timer.getValue to get the current progress in a timer without altering it. Read on to 
get a more in detail explanation
    

    \nThere are a few differences as to how both types of timers work. When setting an incremental timer, it will start at 0 on default and will count up every time the current frame
ends and the next one begins until you want to stop it and get the result. Then, once you access it using Timer.getDec, the timer will end and will get removed so you don't need to manage it.
However, if you want to keep the timer running, you can instead use Timer.getValue(name, inc=True #inc equals True by default) to get the current value from the timer without stopping it. This will
return False if the timer does not exist\\ the timer was already obtained\\ the timer has yet to be started.

    \nWhen settings a decremental timer using Timer.setDec, it will start at 60 on default, which roughly equates to one second, and will count down on every frame until it reaches 0.
When it reaches 0, it will instantly be set to True and will wait for you to next access the result. When accessing the result using Timer.getDec, if the timer has yet to finish, it will return False
and will keep going. However, if it has finished and has been set to True, it will return True and will automatically delete itself. If you want to see how many frames the timer
has to go until it is finished or if it has finished, and/or if you want to access it without potentially deleting it, you can use Timer.getValue(name, inc=False) to see. It will
return an interger if the timer has yet to finish, True if the timer has finished and is waiting to be checked, and False if the timer does not exist\\ the timer was finished and has been checked\\
 the timer has yet to be started.

    \nThe reasoning for all of this is to keep you from writing systems that create a bunch of unused timers that are started once and left unused, and to have a system that
allows you to simplify your code. You would use an incremental timer for either measuring how many frames it took for this to happen by starting it at one point and ending
it at another and never used again, or to simply keep as a statistic that will be accessed here or there. You would use a decremental timer by starting it at some point to have
something happen for a limited time, and while it is happening you check every frame to see if it should be over until it does end, where you finally get a True result and run
some stuff and then stop checking. That essentially sums up all of the uses of a timer, and to say, keep an incremental timer running long after you've finished measuring 
or have a decremental timer who finished long ago sitting in memory being unused. Thus, for those cases, once you've finished with those you can grab the result and leave the rest
to the system. Or, if you are keeping a timer as a statistic for a record, you can simply access it whenever you need to while not having to specify that the timer should be left running.

    \nThat about sums it up. It's rather simple, but the reasoning behind it isn't as much so.
"""


def _NextID(itemList:dict, name:str='') -> str:
    keylist = itemList.keys()
    for i in range(len(itemList)):
        if not name+str(i) in keylist:
            return name+str(i)
    return name+str(len(itemList))


_UpList: dict[str, int] = {}
_DownList: dict[str, int|bool] = {}


def tick() -> None:
    for incTimer in _UpList:
        _UpList[incTimer] += 1

    for decTimer in _DownList:
        if _DownList[decTimer] == True: continue
        _DownList[decTimer] -= 1
        if _DownList[decTimer] <= 0:
            _DownList[decTimer] = True

def setInc(name:str='', value:int = 0) -> None:
    if name in _UpList:
        name = _NextID(_UpList)
    _UpList[name] = value
    return

def setDec(name:str='', value:int=60) -> None:
    """Starts a timer that decrements by one every frame. Get using Timer.getDec(name)\n
    If the timer hits 0, it will activate and be set to True. Use this to simplify checking.\n
    If the name is already taken, it will find the next available username by using parenthesis.
    To make sure that you always are linked to the correct timer, set the return to a variable to
    refer back to the timer. It will always return the name of the timer."""
    if name in _DownList:
        name = _NextID(_DownList)
    _DownList[name] = value
    return

    
def getInc(key) -> int|bool:
    """Gets the value from an incremental timer. 
    \n! Removes the timer automatically after obtaining ! This differs from Timer.getDec 
    \n To access an incremental timer result without stopping it, use Timer.getValue(name, inc=True) to access it without removing it"""
    if not key in _UpList: return False
    
    return _UpList[key]

def getDec(key:str) -> bool:
    """Gets the value from a decremental timer.
    If the timer is finished, it will return True instead. If it is not, then it will return False. Use this to simplify checking. 
    \n! Will remove the timer afterward if the timer returns True !
    \nTo access a decremental timer result without deleting it or get it's current progress, use Timer.getValue(name, inc=False)"""
    if not key in _DownList: raise KeyError(f"Invalid timer name {key}!")
    if not _DownList[key] == True: return False
    del _DownList[key]
    return True

def getValue(name:str, inc:bool=True) -> int|bool:
    """Returns the value from a timer without deleting it. Useful for checking on timers from elsewhere."""
    if inc: return _UpList[name]
    return _DownList[name]

def ___str__() -> None:
    print("Current Timers:")
    for i in _UpList:
        print(_UpList)
        print(i,":", _UpList[i])
    for i in _DownList:
        print(i,":", _DownList[i])
