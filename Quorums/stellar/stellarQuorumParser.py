import json
import requests
import sys
import os

api_url = 'http://api.stellarbeat.io/v1/nodes'
headers = {'Content-Type': 'application/json'}

def writeStellarQuorumConf():
    response = requests.get(api_url, headers=headers)
    stellarConf = {}
    if response.status_code == 200:
        responseText = json.loads(response.content.decode('utf-8'))
        stellarConf = parseStellarQuorumSystem(responseText)
        f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "stellar.json"), "w")
        f.write(json.dumps(stellarConf, indent=2, separators=(',', ': ')))
        f.close()
        print("Successfully written stellar.json")

def parseStellarQuorumSystem(stellarConfigFile):
    asymQuorumSystem = []
    for stellarValidator in (stellarValidator for stellarValidator in stellarConfigFile if stellarValidator['isValidator'] == True):
        validatorPubKey = stellarValidator['publicKey']
        validatorQuorumSet = parseQuorumSet(stellarValidator['quorumSet'])
        asymQuorumSystem.append({'PubKey' : validatorPubKey, 'FailProneSystem' : {}, 'QuorumSystem' : validatorQuorumSet})
    return asymQuorumSystem

def parseQuorumSet(quorumSet):
    threshold = quorumSet['threshold']
    validators = quorumSet['validators']
    innerQuorumSets = quorumSet['innerQuorumSets']
    for innerQuorumSet in innerQuorumSets:
        validators.append(parseQuorumSet(innerQuorumSet))
    return {'select': threshold, 'out-of': validators}

def setIntegerIdsForPubKeys(confFile):
    systemDescription = ""
    with open(confFile, 'r') as conf:
        systemDescription = json.loads(conf.read())
    res = {}
    counter = 1
    for processDescription in systemDescription:
        res[processDescription['PubKey']] = counter
        counter += 1

    f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "integer-keys.json"), "w")
    f.write(json.dumps(res, indent=2, separators=(',', ': ')))
    f.close()
    print("Successfully written integer-keys.json")

def getIntegerIdsForPubKeys(pubKey):
    integerKeys = ""
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'integer-keys.json'), 'r') as conf:
        integerKeys = json.loads(conf.read())
    return integerKeys[pubKey]