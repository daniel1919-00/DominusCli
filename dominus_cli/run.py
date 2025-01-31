from dominusUserConfig import cliConfigurationDone, setupUserConfiguration, getUserConfig
from cli import dominusCliSession
from common import clearTerminal
from theme import setTheme

if __name__ == '__main__':
    clearTerminal()

    if not cliConfigurationDone:
        setupUserConfiguration()
    setTheme(getUserConfig().get('currentTheme'))
    dominusCliSession.start()