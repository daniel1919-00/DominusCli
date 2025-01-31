from common import printCmdOutput, printInfo, promptChoice, printError
from dominus import DominusCLI
from theme import getCurrentTheme, getThemesList, setTheme
from os import path
from paths import PATH_CLI_THEMES
from dominusUserConfig import updateUserConfig

def run(session: DominusCLI, arguments = []):
    if 'set' in arguments or 'change' in arguments:
        newThemeName = None
        try:
            newThemeName = arguments[1]
        except IndexError:
            themes = getThemesList()
            newThemeName = promptChoice("Select a theme", themes)

        if newThemeName == getCurrentTheme().get('name'):
            printInfo('Theme already applied.')
            return

        newThemePath = path.join(PATH_CLI_THEMES, newThemeName + '.json')

        if not path.exists(newThemePath):
            printError(f"Theme not found: {newThemePath}")
            return
        
        setTheme(newThemeName)
        updateUserConfig({"currentTheme": newThemeName})
    else:
        themes = getThemesList()
        printInfo('Available themes:')
        currentThemeName = getCurrentTheme().get('name')
        for theme in themes:
            themeApplied = ''
            if theme == currentThemeName:
                themeApplied = '*'
            
            printCmdOutput(f'[{themeApplied}] {theme}')
            print('')
        return