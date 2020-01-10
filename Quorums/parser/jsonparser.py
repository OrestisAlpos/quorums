import BSC.parser.parserutil as parserutil
import BSC.parser.bitmapparserutil as bitmapparserutil
import json
import pyroaring
import os

def parseAsymFailProneSystem(confTitle):
    return parseJsonAsym(os.path.join(os.path.dirname(__file__), 'config.json'), confTitle, 'FailProneSystem')

def parseAsymQuorumSystem():
    return parseJsonAsym('stellar/stellar.json', confTitle='', specificationToUse='QuorumSystem')

def parseAsymFailProneSystemAsBitmap(confTitle):
    return parseJsonAsymToBitmap(os.path.join(os.path.dirname(__file__), 'config.json'), confTitle, 'FailProneSystem')

def parseAsymQuorumSystemAsBitmap():
    return parseJsonAsymToBitmap('stellar/stellar.json', confTitle='', specificationToUse='QuorumSystem')

# stellar.json includes some pubkeys in the quorum set that don't seem to be part of the universe
# (they don't seem to have a quorum set themselves). So I had to remove these for the parser to work with integer keys.
def parseAdaptedAsymQuorumSystemAsBitmap():
    return parseJsonAsymToBitmap('stellar/stellar_adapted.json', confTitle='', specificationToUse='QuorumSystem')

def parseAdaptedAsymQuorumSystem():
    return parseJsonAsym('stellar/stellar_adapted.json', confTitle='', specificationToUse='QuorumSystem')


# Use this to parse a description of a Fail Prone System in the SYMMETRIC trust setting.
# Input: a string that indicates an entry in config.json. That entry describes the Fail Prone System.
# Returns the Fail Prone System, which is a set of sets (the outer set is usually called Fail Prone System and the inner sets are the Fail Prone Sets).
# For technical reasons I used the frozenset Python's data structure instead of the set data structure.
def parseJson(confTitle):  
    jsonString = ""
    with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'r') as conf:
        jsonString = json.loads(conf.read())
    systemDescription = jsonString[confTitle]
    #systemDescription is a list of lists: each systemDescription[i] describes a Fail Prone Set.
    setsParsed = list()
    for description in systemDescription:
        setsParsed.append(parserutil.parseSetsFromDescription(description))
    return frozenset().union(*setsParsed)    

# Use this to parse a description of a Fail Prone System (or Quorum System) in the ASYMMETRIC trust setting.
# Input: a string that indicates an entry in config.json. That entry describes the Fail Prone Systems, that is the Fail Prone System for every process, assuming one line per process (See config.json).
# Returns a tuple of the universe as a key dict and the failpronesystem as a dict
# dict: str (name of process) -> frozenset of frozensets (failProneSet of process).
# For technical reasons I used the frozenset Python's data structure instead of the set data structure.
def parseJsonAsym(confFile, confTitle = '', specificationToUse = 'FailProneSystem'):  #Returns a 
    universe = parserutil.setIntegerIdsForPubKeys(confFile, confTitle)
    jsonString = ""
    with open(confFile, 'r') as conf:
        jsonString = json.loads(conf.read())
    if confTitle == "":
        systemDescription = jsonString
    else:
        systemDescription = jsonString[confTitle]
    #systemDescription is a list of dicts: each systemDescription[i] describes a process Fi
    res = {}
    for processDescription in systemDescription:

        if isinstance(processDescription[specificationToUse], list):
            processTrustAssumption = parserutil.parseArraysFromThresholdDescription(processDescription[specificationToUse], universe)
        else:
            processTrustAssumption = parserutil.parseSetsFromThresholdDescription(processDescription[specificationToUse], universe)
        res[universe[processDescription['PubKey']]] = processTrustAssumption
    return (universe, res) 

# returns a tuple of the universe as a key dict and the failpronesystem as a dict
def parseJsonAsymToBitmap(confFile, confTitle = '', specificationToUse = 'FailProneSystem'):
    universe = parserutil.setIntegerIdsForPubKeys(confFile, confTitle)
    jsonString = ""
    with open(confFile, 'r') as conf:
        jsonString = json.loads(conf.read())
    if confTitle == "":
        systemDescription = jsonString
    else:
        systemDescription = jsonString[confTitle]
    res = {}
    for processDescription in systemDescription:
        if isinstance(processDescription[specificationToUse], list):
            processTrustAssumption = bitmapparserutil.parseArraysFromThresholdDescription(processDescription[specificationToUse], universe)
        else:
            processTrustAssumption = bitmapparserutil.parseBitMapSetsFromThresholdDescription(processDescription[specificationToUse], universe)
        res[universe[processDescription['PubKey']]] = processTrustAssumption
    return (universe, res)

def parseUniverseFromJsonAsym(confFile, confTitle = '', specificationToUse = 'FailProneSystem'):
    jsonString = ""
    with open(confFile, 'r') as conf:
        jsonString = json.loads(conf.read())
    if confTitle == "":
        systemDescription = jsonString
    else:
        systemDescription = jsonString[confTitle]
    res = set()
    for processDescription in systemDescription:
        res.add(processDescription['PubKey'])
    return res

    
