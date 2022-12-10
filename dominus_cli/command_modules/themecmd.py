from common import printCmdOutput, printInfo, promptChoice, printError
from dominus import DominusCLI
from theme import currentTheme, getThemesList, currentThemeFilePath, reloadTheme
from os import path
from shutil import copyfile
from paths import PATH_CLI_THEMES

def run(session: DominusCLI, arguments = []):
    if not arguments:
        arguments.append('list')
    
    if 'list' in arguments:
        themes = getThemesList()
        printInfo('Available themes:')
        currentThemeName = currentTheme.name
        for theme in themes:
            themeApplied = ''
            if theme == currentThemeName:
                themeApplied = '*'
            
            printCmdOutput(f'[{themeApplied}] {theme}')
            print('')
        return

    if 'set' in arguments or 'change' in arguments:
        newThemeName = None
        try:
            newThemeName = arguments[1]
        except IndexError:
            themes = getThemesList()
            newThemeName = promptChoice("Select a theme", themes)

        if newThemeName == currentTheme.name:
            printInfo('Theme already applied.')
            return

        newThemePath = path.join(PATH_CLI_THEMES, newThemeName + '.json')

        if not path.exists(newThemePath):
            printError(f"Theme config not found: {newThemePath}")
            return
        
        copyfile(newThemePath, currentThemeFilePath)
        reloadTheme()