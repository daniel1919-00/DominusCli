from prompt_toolkit import prompt, ANSI
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.formatted_text import HTML
from autoCompleter import AutoCompleter
from os import path, sep as dirSep, getcwd
from pathlib import Path
from commands import getCommandDefinition, constructCommandAliasMap
from common import importCommandModule, printWarning, printInfo, runTerminalCommand, applyAnsiColor, getConfigParam
from theme import getCurrentTheme
from dominusUserConfig import cliDefaultSaveDataDirPath

class DominusCLI:
    isRunning = False
    runningTerminalCommand = False

    def prompt(self):
        try:
            prompter = '['
            currentPath = getcwd()
            currentDir = Path(currentPath).absolute()
            parentDir = str(currentDir.parent.absolute().resolve())

            if parentDir != '/':
                prompter += '..' + dirSep + path.basename(parentDir)

            prompter += dirSep + path.basename(currentDir) + ']> '

            self.parseInput(prompt(
                ANSI(applyAnsiColor(prompter, getCurrentTheme().get('promptColor'))),
                history = FileHistory(path.join(cliDefaultSaveDataDirPath, 'cmd.hist')),
                auto_suggest = AutoSuggestFromHistory(),
                completer = AutoCompleter(self),
                complete_in_thread = True,
                bottom_toolbar = HTML(f'<b>Dominus CLI v{getConfigParam("version")}</b>| {currentPath}')
            ))
        except KeyboardInterrupt:
            if not self.runningTerminalCommand:
                self.stop("Force terminate!")
            else:
                self.runningTerminalCommand = False
        except EOFError:
            self.stop("Force terminate!")
        
    def executeCommand(self, command: str, arguments: list):
        cmdDef = getCommandDefinition(command)
        
        if not cmdDef:
            printWarning(f"Command not '{command}' available! Forwarding to terminal.")
            self.runningTerminalCommand = True
            runTerminalCommand(command + ' ' + ' '.join(arguments), True)
            self.runningTerminalCommand = False
            return

        if 'quit' in cmdDef['aliases']:
            exit(0)

        if "command" in cmdDef:
            printInfo(f"Executing alias {command} -> {cmdDef['command']}")
            self.parseInput(cmdDef["command"])
        else:
            importCommandModule(cmdDef['pythonModule']).run(self, arguments)

    def parseInput(self, rawInput: str):
        rawInput = rawInput.strip()
        if rawInput == '':
            return

        commandParts = []
        currentWord = ''
        unbalancedSpecialCharacter = ''
        escapedCharPositions = []
        for charIndex, char in enumerate(rawInput):
            if char == ' ' and not unbalancedSpecialCharacter:
                currentWord = currentWord.strip()
                if currentWord != '':
                    commandParts.append(currentWord)
                    currentWord = ''
                continue

            if char == '\\':
                try:
                    nextChar = charIndex + 1
                    if rawInput[nextChar] == '"' or rawInput[nextChar] == "'":
                        escapedCharPositions.append(nextChar)
                        continue
                except IndexError:
                    pass

            if charIndex not in escapedCharPositions:
                if not unbalancedSpecialCharacter and (char == '"' or char == "'"):
                    unbalancedSpecialCharacter = char
                    continue

                elif unbalancedSpecialCharacter == char:
                    unbalancedSpecialCharacter = ''
                    continue
            
            currentWord += char

        if currentWord != '':
            commandParts.append(currentWord)
        command = ''
        arguments = []

        for index, cmdPart in enumerate(commandParts):
            if index == 0:
                command = cmdPart.strip()
            else:
                arguments.append(cmdPart.strip())
        
        if command == '':
            return
            
        self.executeCommand(command, arguments)

    def start(self):
        constructCommandAliasMap()
        self.isRunning = True
        while self.isRunning:
            self.prompt()

    def stop(self, exitMessage: str = ''):
        if not exitMessage == '':
            printInfo(exitMessage)
        self.isRunning = False
