# run with python b3checker.py
import sys
import argparse

import Quorums.checker.checker as checker
import Quorums.parser.jsonparser as jsonparser
import os

def getParsedSystemFromConfig(fileName, configName, isBitMap, useQuorumSystem):
    if isBitMap:
        if useQuorumSystem:
            (universe, failProneSystem) = jsonparser.parseJsonAsymToBitmap(fileName, configName, 'QuorumSystem')
        else:
            (universe, failProneSystem) = jsonparser.parseJsonAsymToBitmap(fileName, configName)
    else:
        if useQuorumSystem:
            (universe, failProneSystem) = jsonparser.parseJsonAsym(fileName, configName, 'QuorumSystem')
        else:
            (universe, failProneSystem) = jsonparser.parseJsonAsym(fileName, configName)
    return (universe, failProneSystem)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('sys_name', metavar='sys_name', type=str, help='the name of a system defined in config.json')
    parser.add_argument('--file_path', type=str, help='use a file path')
    parser.add_argument('--parse_quorum_system', nargs='?', const=True, default=False, type=str, help='parse quorum system instead of fail-prone system')
    parser.add_argument('--use_opt', nargs='?', const=True, default=False, help='use optimised brute force algorithm instead of bounded search tree')
    parser.add_argument('--bitmap', nargs='?', const=True, default=False, help='use the BitMap data structure instead of sets')
    parser.add_argument('--show_all_faults', nargs='?', const=True, default=False, help='return all B3 violations found in the system')
    parser.add_argument('--one_process', type=str, help='test B3 only for one process')
    parser.add_argument('--two_processes', nargs='+', help='test B3 only for two processes')
    args = parser.parse_args()

    hasFilePath = args.file_path is not None
    configName = args.sys_name
    useQuorumSystem = args.parse_quorum_system
    useOpt = args.use_opt #in ['TRUE', 'True', 'true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh', 'dehalt']
    isBitMap = args.bitmap #in ['TRUE', 'True', 'true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']
    returnAll = args.show_all_faults #in ['TRUE', 'True', 'true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']
    oneProcess = args.one_process is not None
    twoProcesses = args.two_processes is not None

    if not hasFilePath or not os.path.isfile(args.file_path):
        fileName = os.path.join(os.path.dirname(__file__), 'system-config.json')
    else: 
        fileName = args.file_path
        
    print("Your system is getting parsed...")
    (universe, failProneSystem) = getParsedSystemFromConfig(fileName, configName, isBitMap, useQuorumSystem)
    print("Parsing of system completed. B3-checker is run...")

    if useOpt:
        if oneProcess:
            node = args.one_process
            isVerified = checker.checkB3ForOneNode(universe, failProneSystem, node)
        elif twoProcesses:
            nodes = args.two_processes
            system1 = failProneSystem[universe[nodes[0]]]
            system2 = failProneSystem[universe[nodes[1]]]
            isVerified = checker.checkB3TwoProcesses(universe, system1, system2)
        elif returnAll:
            isVerified = checker.getAllFailuresForB3(universe, failProneSystem)            
        else:
            isVerified = checker.checkB3(universe, failProneSystem)


    else:
        if oneProcess:
            node = args.one_process
            isVerified = checker.checkB3WithSetCoverForOneNode(universe, failProneSystem, node)
        elif twoProcesses:
            nodes = args.two_processes
            system1 = failProneSystem[universe[nodes[0]]]
            system2 = failProneSystem[universe[nodes[1]]]
            isVerified = checker.checkB3withSetCoverTwoProcesses(universe, system1, system2)
        elif returnAll:
            isVerified = checker.getAllFailuresForB3SetCover(universe, failProneSystem)
        else:
            isVerified = checker.checkB3withSetCover(universe, failProneSystem)


    
    if isVerified:
        print('The condition holds for your system.')
    else:
        print('The condition does not hold for your system.')