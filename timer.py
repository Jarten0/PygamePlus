class Timer():
    UpList = {}
    DownList = {}

    def tick():
        for i in Timer.UpList:
            Timer.UpList[i] += 1
        for i in Timer.DownList:
            if not Timer.DownList[i] == True:
                Timer.DownList[i] -= 1
            if Timer.DownList[i] == 0:
                Timer.DownList[i] = True

    def set(name = False, value = None, up = False):
        if value == None or up:
            if name == False:
                keylist = Timer.UpList.keys()
                for i in Timer.UpList:
                    if not keylist[Timer.UpList.index(i)] == i:
                        name = Timer.UpList[i]
                        print(name)
            if value == None:
                value = 0
            Timer.UpList[name] = value
        else:
            Timer.DownList[name] = value
        

    def get(name, up = False):
        if up:
            return Timer.UpList[name]
        if Timer.DownList[name] == True:
            #print(Timer.DownList)
            return True 
        else:
            return False

    def getvalue(name, up):
        if up:
            return Timer.UpList[name]
        return Timer.DownList[name]

    def __str__():
        print("Current Timers:")
        for i in Timer.UpList:
            print(Timer.UpList)
            print(i,":", Timer.UpList[i])
        for i in Timer.DownList:
            print(i,":", Timer.DownList[i])