import json
from os import path
from paths import PATH_CLI_ROOT
from dominusUserConfig import getUserConfig

Commands = {}
MainCommands = []
CommandAliasMap = {}

def constructCommandAliasMap():
    with open(path.join(PATH_CLI_ROOT, 'commands.json')) as commandsFile:
        storedCommands = json.load(commandsFile)
        for alias in storedCommands:
            Commands[alias] = storedCommands[alias]

    existingCommands = getUserConfig().get('existingAliases')
    for alias in existingCommands:
        Commands[alias] = existingCommands[alias]  
        
    del MainCommands[:]
    sortedCommands = sorted(list(Commands.keys()))
    for command in sortedCommands:
        MainCommands.append(command)
        commandAliases = Commands[command]['aliases']
        if commandAliases:
            for alias in commandAliases:
                CommandAliasMap[alias] = command

def getCommandDefinition(command: str):
    if command in MainCommands:
        return Commands[command]
    elif command in CommandAliasMap:
        return Commands[CommandAliasMap[command]]
    else:
        return None