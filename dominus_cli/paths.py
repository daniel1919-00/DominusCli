
import sys
from pathlib import Path
from os import path, chdir

scriptParent = Path(__file__).parent
PATH_CLI_ROOT = str(scriptParent.absolute())
PATH_CLI_THEMES = path.join(PATH_CLI_ROOT, 'themes')
PATH_CLI_PARENT = str(scriptParent.parent.parent.absolute())
PATH_DEFAULT_SAVE_DATA = path.join(PATH_CLI_ROOT, 'savedData')

PATH_DOMINUS_PROJECT_ROOT = path.join(PATH_CLI_PARENT)
if not path.exists(path.join(PATH_DOMINUS_PROJECT_ROOT, 'Dominus', "paths.php")):
    PATH_DOMINUS_PROJECT_ROOT = ""

sys.path.append(path.join(PATH_CLI_ROOT, 'command_modules'))
chdir(PATH_CLI_PARENT)