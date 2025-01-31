import json
from os import path, sep as dirSep, getlogin, access, chmod
from pathlib import Path
import platform
import subprocess
from typing import Literal
from prompt_toolkit import print_formatted_text, ANSI
import getpass
import inquirer
from theme import getCurrentTheme
from paths import PATH_CLI_ROOT
from shutil import rmtree
import dominusConfig

AnsiColors = Literal[
    'black',
    'red',
    'lightred',
    'green',
    'lightgreen',
    'yellow',
    'lightyellow',
    'blue',
    'lightblue',
    'purple',
    'lightpurple',
    'cyan',
    'lightcyan'
]

AnsiEscapeSequences = {
    'reset': '\033[0m',
    'black': '\033[0;30m',
    'bold_black': '\033[1;30m',
    'background_black': '\033[40m',
    'red': '\033[0;31m',
    'bold_red': '\033[1;31m',
    'background_red': '\033[41m',
    'lightred': '\033[0;91m',
    'bold_lightred': '\033[1;91m',
    'background_lightred': '\033[0;101m',
    'green': '\033[0;32m',
    'bold_green': '\033[1;32m',
    'background_green': '\033[42m',
    'lightgreen': '\033[0;92m',
    'bold_lightgreen': '\033[1;92m',
    'background_lightgreen': '\033[0;102m',
    'yellow': '\033[0;33m',
    'bold_yellow': '\033[1;33m',
    'background_yellow': '\033[43m',
    'lightyellow': '\033[0;93m',
    'bold_lightyellow': '\033[1;93m',
    'background_lightyellow': '\033[0;103m',
    'blue': '\033[0;34m',
    'bold_blue': '\033[1;34m',
    'background_blue': '\033[44m',
    'lightblue': '\033[0;94m',
    'bold_lightblue': '\033[1;94m',
    'background_lightblue': '\033[0;104m',
    'purple': '\033[0;35m',
    'bold_purple': '\033[1;35m ',
    'background_purple': '\033[45m',
    'lightpurple': '\033[0;95m',
    'bold_lightpurple': '\033[1;95m',
    'background_lightpurple': '\033[0;105m',
    'cyan': '\033[0;36m',
    'bold_cyan': '\033[1;36m',
    'background_cyan': '\033[46m',
    'lightcyan': '\033[0;96m',
    'bold_lightcyan': '\033[1;96m',
    'background_lightcyan': '\033[0;106m'
}

def getUserName() -> str:
    username = ''
    try:
        username = getpass.getuser()
    except:
        try:
            username = getlogin()
        except:
            usernameCache = path.join(dominusConfig.cliDefaultSaveDataDirPath, 'usrname')
            if path.exists(usernameCache):
                return Path(usernameCache).read_text()

            while username == '':
                username = input("Failed to obtain the current user name from the os. Please enter the current user name: ").strip()
            
            with open(usernameCache, "w") as usernameCacheFile:
                usernameCacheFile.write(username)

            printInfo(f"User name cached to: {usernameCache}.")

    return username


def printf(str: str) -> None:
    print_formatted_text(ANSI(str))

def applyAnsiColor(string: str, foreground: AnsiColors='', background: AnsiColors='', bold=False) -> str:
    if foreground:
        if bold:
            foreground = 'bold_' + foreground

        foregroundEscapeSeq = AnsiEscapeSequences[foreground]
    else:
        foregroundEscapeSeq = ''
    
    if background:
        backgroundEscapeSeq = AnsiEscapeSequences['background_' + background]
    else:
        backgroundEscapeSeq = ''

    return f'{backgroundEscapeSeq}{foregroundEscapeSeq}{string}{AnsiEscapeSequences["reset"]}'

def printColored(string: str, foreground: AnsiColors, background: AnsiColors='', bold=False) -> None:
    printf(applyAnsiColor(string, foreground, background, bold))

def inputColored(prompt: str, foreground: AnsiColors, background: AnsiColors='', bold=False) -> str:
    return input(applyAnsiColor(prompt, foreground, background, bold))

def printInfo(string: str) -> None:
    printColored(string, getCurrentTheme().printInfoColor, bold=True)

def printOk(string: str) -> None:
    printColored(string, getCurrentTheme().printOkColor, bold=True)

def printWarning(string: str) -> None:
    printColored(string, getCurrentTheme().printWarningColor, bold=True)

def printError(string: str) -> None:
    printColored(string, getCurrentTheme().printErrorColor, bold=True)

def printCmdOutput(string: str) -> None:
    printColored(string, getCurrentTheme().printCmdOutputColor, bold=True)
    
def promptOk(prompt: str) -> str:
    return inputColored(prompt, getCurrentTheme().printOkColor)

def promptError(prompt: str) -> str:
    return inputColored(prompt, getCurrentTheme().printErrorColor)

def promptWarning(prompt: str) -> str:
    return inputColored(prompt, getCurrentTheme().printWarningColor)

def promptInfo(prompt: str) -> str:
    return inputColored(prompt, getCurrentTheme().printInfoColor)

def promptChoice(prompt: str, choices: list):
    answers = inquirer.prompt([
        inquirer.List('choice',
            message=prompt,
            choices=choices,
        )
    ])
    return answers["choice"]

def isWindows() -> bool:
    return platform.system() == "Windows"

def clearTerminal() -> None:
    if isWindows():
        subprocess.Popen("cls", shell=True).communicate()
        print("")
    else:
        print("\033c")

class CommandOutput:
    output = ''
    error = ''

    def __init__(self, output, error):
        self.output = output
        self.error = error

def runTerminalCommand(command: str, printOutputRealtime = False) -> CommandOutput:
    if printOutputRealtime:
        p = subprocess.Popen(command, shell = True)
        p.wait()
        return CommandOutput('', '')

    sp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = sp.communicate()
    return CommandOutput(out.decode(), err.decode())

configStorage = {}
with open(path.join(PATH_CLI_ROOT, 'config.json')) as configFile:
    configStorage = json.load(configFile)

def getConfigParam(param: str):
    return configStorage[param]

def replaceDirSeparatorWithOs(path: str) -> str:
    return path.replace('/', dirSep).replace('\\', dirSep)

def importPythonModule(module: str):
    return __import__(module, locals(), globals(), ["main"])

def importCommandModule(cmdModule: str):
    return importPythonModule("command_modules.%s" % (cmdModule))

def parsePlaceholders(string: str, placeholders):
    if string != '':
        for placeholder in placeholders:
            string = string.replace(placeholder, placeholders[placeholder])
    return string

def getCopyrightText() -> str:
    return Path(path.join(PATH_CLI_ROOT, 'copyright')).read_text().strip()

def onrmtreeError(func, path, exc_info):
    import stat
    from os import W_OK
    if not access(path, W_OK):
        chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

def deleteTree(path: str):
    rmtree(path, onexc=onrmtreeError)