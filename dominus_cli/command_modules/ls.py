from dominus import DominusCLI
from os import listdir, path, linesep
from common import printf, applyAnsiColor
from theme import getCurrentTheme

def run(session: DominusCLI, arguments = []):
    dirContents = listdir()
    dirContents.sort()
    dirs = []
    files = []

    for item in dirContents:
        if item.startswith('.'):
            continue
        
        if path.isdir(item):
            dirs.append(applyAnsiColor(item, getCurrentTheme().get('ls_dirColor'), bold=True))
        else:
            files.append(applyAnsiColor(item, getCurrentTheme().get('ls_fileColor')))

    printf(linesep.join(dirs + files))