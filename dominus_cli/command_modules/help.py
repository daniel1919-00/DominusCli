from commands import Commands, getCommandDefinition
from common import applyAnsiColor, printColored, printError, printf, printInfo
from theme import getCurrentTheme
from dominus import DominusCLI

def printHelpAll():
    printInfo('Available Commands:')

    maxCmdLen = 0
    maxCmdArgLen = 0
    formattedCommands = []
    currentTheme = getCurrentTheme()
    headerColor = currentTheme.helpHeaderColor
    normalColor = currentTheme.helpColor

    for mainCommand in Commands:
        cmdDef = Commands[mainCommand]
        cmdAliases = cmdDef['aliases']
        cmdArguments = cmdDef['arguments']
        cmdPadding = ' ' * 2

        if cmdAliases:
            mainCommand = mainCommand + '('+ ', '.join(cmdAliases) +')'
            
        cmdLen = len(mainCommand)
        if cmdLen > maxCmdLen:
            maxCmdLen = cmdLen
        
        formattedCommands.append([
            applyAnsiColor(f'{cmdPadding}{mainCommand}', headerColor, bold=True),
            cmdDef["description"],
            cmdLen
        ])

        if cmdArguments:
            cmdPadding = cmdPadding * 2

            for cmdArgDef in cmdArguments:
                cmdArg = cmdArgDef['argument']
                cmdArgLen = len(cmdArg)
                
                if cmdArgLen > maxCmdArgLen:
                    maxCmdArgLen = cmdArgLen
            
                formattedCommands.append([
                    applyAnsiColor(f'{cmdPadding}{cmdArg}', normalColor, bold=True),
                    cmdArgDef["description"],
                    cmdArgLen
                ])

    for cmd in formattedCommands:
        printf(
            cmd[0]
            + (' ' * (1 + maxCmdLen - cmd[2]))
            + cmd[1]
        )

def printHelpFor(command: str):
    cmdDef = getCommandDefinition(command)

    if not cmdDef:
        printError('Command not available!')
        return

    currentTheme = getCurrentTheme()
    headerColor = currentTheme.helpHeaderColor
    normalColor = currentTheme.helpColor
    indent = ' ' * 2

    print('')
    printColored('Command', headerColor)
    printColored(f'{indent}{command}', normalColor)

    print('')
    printColored('Description', headerColor)
    printColored(f'{indent}{cmdDef["description"]}', normalColor)

    print('')
    printColored('Arguments', headerColor)
    
    if cmdDef["arguments"]:
        for arg in cmdDef["arguments"]:
            printColored(f'{indent}{arg["argument"]}  {arg["description"]}', normalColor)
    else:
        printColored(f'{indent}N/A', normalColor)

    print('')
    printColored('Aliases', headerColor)
    
    if cmdDef["aliases"]:
        for alias in cmdDef["aliases"]:
            printColored(f'{indent}{alias}', normalColor)
    else:
        printColored(f'{indent}N/A', normalColor)

    print('')
    printColored('Examples', headerColor)

    if cmdDef["examples"]:
        for example in cmdDef["examples"]:
            printColored(f'{indent}{example}', normalColor)
    else:
        printColored(f'{indent}N/A', normalColor)

def run(session: DominusCLI, arguments = []):
    try:
        printHelpFor(str(arguments[0]).strip())
    except IndexError:
        printHelpAll()