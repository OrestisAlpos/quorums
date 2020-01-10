import BSC.checker.checker as checker
import BSC.parser.jsonparser as jsonparser
import os

# run this file with python -m BSC

def getParsedSystemFromConfig(fileName, configName, isFrozenset):
    if isFrozenset:
        (universe, failProneSystem) = jsonparser.parseJsonAsym(fileName, configName)
    else:
        (universe, failProneSystem) = jsonparser.parseJsonAsymToBitmap(fileName, configName)
    return (universe, failProneSystem)


def checkB3ForParsedSystem(universe, failProneSystem):
    return checker.checkB3(universe, failProneSystem)


if __name__ == "__main__":

    fileName = input("Please insert the location of the file you would like to parse:")
    if not os.path.isfile(fileName):
        fileName = os.path.join(os.path.dirname(__file__), fileName)
        
    configName = input("Please insert the name of the config you would like to use:")
    isFrozenset = False
    isFrozensetString = input("If you would like your System to be parsed as a frozenset, please enter 'y' for yes:")
    if isFrozensetString == 'y':
        isFrozenset = True
    print("Your system is getting parsed...")
    (universe, failProneSystem) = getParsedSystemFromConfig(fileName, configName, isFrozenset)
    print("Parsing of system completed. B3-checker is run...")
    isVerified = checkB3ForParsedSystem(universe, failProneSystem)
    if isVerified:
        print('The condition holds for your system.')
    else:
        print('The condition does not hold for your system.')


    
