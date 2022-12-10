from os import getcwd
from common import printCmdOutput
from dominus import DominusCLI

def run(session: DominusCLI, arguments = []):
    printCmdOutput(getcwd())