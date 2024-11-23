import os
import re
import datetime
from time import sleep

test = "tanks digin; tanks defend; if damaged retreat else if mountains infantry attack else tanks attack;"


ActorList = [
    "tank",
    "infantry",
    "artillery",
    "anti-tank",
    "motorized",
    "engineers"
]

ActionList = [
    "digin",
    "attack",
    "retreat",
    "barrage",
    "defend"
]

class Condition:
    def __init__(self, a, b, cond):
        self.success = a
        self.fail = b

        self.cond = cond

    def __str__(self):
        return f"Condition: [{self.cond}]: ({self.success}) else ({self.fail})"

class Action:
    def __init__( self, actor, action ):
        self.actor = actor
        self.action = action

    def __str__(self):
        return f"{self.actor and self.actor or "All"}: {self.action}"

def parseStatement( data, pos ):
    while data[pos] == "":
        pos += 1
        if pos >= len(data): return len(data), None
    if data[pos] == "if":
        obj = Condition( None, None, None )
        newpos, sstat = parseStatement( data, pos + 2 )
        cond = data[pos + 1]
        newpos, fstat = parseStatement( data, newpos + 2 )

        obj.success, obj.fail, obj.cond = sstat, fstat, cond

        return newpos, obj
    else:
        act = Action( None, None )

        actor = None
        action = None
        if data[pos] in ActorList or any( [((i + "s") == data[pos]) for i in ActorList] ): actor = data[pos]
        elif data[pos] in ActionList or any( [((i + "s") == data[pos]) for i in ActionList] ): action = data[pos]

        pos += 1
        if pos >= len(data):
            act.actor, act.action = actor, action
            return pos, act
        if data[pos] in ActorList or any( [((i + "s") == data[pos]) for i in ActorList] ): actor = data[pos]
        elif data[pos] in ActionList or any( [((i + "s") == data[pos]) for i in ActionList] ): action = data[pos]
        else: pos -= 1

        act.actor, act.action = actor, action

        return pos, act






def parseLine( data ):
    a, o = parseStatement( data, 0 )
    return o


def parseCommand( txt ):
    out = []
    for a in re.split(';|,|then |after', txt):
        out.append( parseLine( a.split( " " ) ))

    return out

o = parseCommand(test)
print( "\n".join([str(i) for i in o] ) )

hour = 0
minute = 0


def printClock():
    sc = ""
    global dat

    os.system('cls' if os.name == 'nt' else 'clear')
    sc = f"|{dat}|\n" + "-" * 64 + "\n"

    for line in range(0, 16):
        sc += "#" * 32 + "\n"

    print( sc )


#while True:
    #for _ in range(15): dat.tick()
    #printClock()
    #sleep( 0.5 )

