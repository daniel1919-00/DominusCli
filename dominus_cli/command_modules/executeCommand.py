from common import printInfo, runTerminalCommand
from dominus import DominusCLI

def run(session: DominusCLI, arguments = []):
    cmd = ' '.join(arguments).strip()
    printInfo(f'Executing: {cmd}')
    runTerminalCommand(cmd, True)