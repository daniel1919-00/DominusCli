
import sys
from pathlib import Path
from os import path, chdir

scriptParent = Path(__file__).parent
PATH_CLI_ROOT = str(scriptParent.absolute())
PATH_CLI_THEMES = path.join(PATH_CLI_ROOT, 'themes')
PATH_CLI_PARENT = str(scriptParent.parent.parent.absolute())

sys.path.append(path.join(PATH_CLI_ROOT, 'command_modules'))
chdir(PATH_CLI_PARENT)