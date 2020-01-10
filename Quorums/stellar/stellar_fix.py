import os
import json

def getInactive():
    f = open("BSC/stellar/stellar.json", "r")
    qsystem = json.loads(f.read())
    f.close()
    inactive =list()
    for qs in qsystem:
        for tv in qs['QuorumSystem']['out-of']:
            if type(tv) == dict:
                for tv_tv in tv['out-of']:
                    if type(tv_tv) == dict:
                        for tv_tv_tv in tv_tv['out-of']:
                            #print("\t\t"+tv_tv_tv)
                            if not validator_exists(qsystem, tv_tv_tv):
                                inactive.append(tv_tv_tv)
                    else:
                        #print("\t"+tv_tv)
                        if not validator_exists(qsystem, tv_tv):
                            inactive.append(tv_tv)
            else:
                #print(tv)
                if not validator_exists(qsystem, tv):
                    inactive.append(tv)
    return inactive

def validator_exists(qs, v):
    return any(validator['PubKey'] == v for validator in qs) 