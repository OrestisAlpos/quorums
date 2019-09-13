import parserutil
import json

# Use this to parse a description of a Fail Prone System in the SYMMETRIC trust setting.
# Input: a string that indicates an entry in config.json. That entry describes the Fail Prone System.
# Returns the Fail Prone System, which is a set of sets (the outer set is usually called Fail Prone System and the inner sets are the Fail Prone Sets).
# For technical reasons I used the frozenset Python's data structure instead of the set data structure.
def parseJson(confTitle):  
    jsonString = ""
    with open('config.json', 'r') as conf:
        jsonString = json.loads(conf.read())
    systemDescription = jsonString[confTitle]
    #systemDescription is a list of lists: each systemDescription[i] describes a Fail Prone Set.
    setsParsed = list()
    for description in systemDescription:
        setsParsed.append(parserutil.parseSetsFromDescription(description))
    return frozenset().union(*setsParsed)    

# Use this to parse a description of a Fail Prone System in the ASYMMETRIC trust setting.
# Input: a string that indicates an entry in config.json. That entry describes the Fail Prone Systems, that is the Fail Prone System for every process, assuming one line per process (See config.json).
# Returns a dictionary. The key of the dictionary is the name of the process and the value is the Fail Prone System of that process; dict: str (name of process) -> frozenset of frozensets (failProneSet of process).
# For technical reasons I used the frozenset Python's data structure instead of the set data structure.
def parseJsonAsym(confTitle):  #Returns a 
    jsonString = ""
    with open('config.json', 'r') as conf:
        jsonString = json.loads(conf.read())
    systemDescription = jsonString[confTitle]
    #systemDescription is a list of lists: each systemDescription[i] describes Fi, which is the FailProneSystem of process i
    setsParsed = list()
    for description in systemDescription:
        setsParsed.append(parserutil.parseSetsFromDescription(description))
    res = {}
    for i in range(len(setsParsed)):
        res[str(i + 1)] = setsParsed[i]
    return res  
