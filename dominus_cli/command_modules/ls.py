from dominus import DominusCLI
from os import listdir, path, linesep
from common import printf, applyAnsiColor
from theme import currentTheme

def run(session: DominusCLI, arguments = []):
    dirContents = listdir()
    dirContents.sort()
    dirs = []
    files = []

    for item in dirContents:
        if item.startswith('.'):
            continue
        
        if path.isdir(item):
            dirs.append(applyAnsiColor(item, currentTheme.ls_dirColor, bold=True))
        else:
            files.append(applyAnsiColor(item, currentTheme.ls_fileColor))

    printf(linesep.join(dirs + files))