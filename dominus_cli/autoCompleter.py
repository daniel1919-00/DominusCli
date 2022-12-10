from os import path, getcwd
from thefuzz import process, utils
from commands import Commands, getCommandDefinition
from prompt_toolkit.completion import Completer, Completion, PathCompleter
from prompt_toolkit.document import Document
from common import importCommandModule, replaceDirSeparatorWithOs

class AutoCompleter(Completer):
    currentCommand = ''
    dominusSession = None

    def __init__(self, dominusSession):
        self.path_completer = PathCompleter(only_directories=True)
        self.dominusSession = dominusSession

    def get_completions(self, document, complete_event):
        wordBeforeCursor = str(document.get_word_before_cursor(WORD=True)).strip()
        autoCompleteList = []

        if document.find_backwards(' ') != None:
            commandParts = document.text.split(' ')
            arguments = []
            
            for index, cmdPart in enumerate(commandParts):
                if index == 0:
                    command = cmdPart.strip().lower()
                else:
                    arguments.append(cmdPart.strip())

            if len(arguments) > 1:
                return complete_event

            mainCommandDef =  getCommandDefinition(command)
            if mainCommandDef:
                if "autocomplete" in mainCommandDef:
                    if "pathCompleter" in mainCommandDef["autocomplete"] and mainCommandDef["autocomplete"]["pathCompleter"]:
                        try:
                            sub_doc = Document(path.join(getcwd(), replaceDirSeparatorWithOs(arguments[0])))
                        except IndexError:
                            sub_doc = Document(document.text[3:])

                        yield from (Completion(completion.text, completion.start_position, display=completion.display)
                            for completion
                            in self.path_completer.get_completions(sub_doc, complete_event))
                    else:
                        autoCompleteList = importCommandModule(mainCommandDef["pythonModule"]).autocomplete(self.dominusSession, arguments)
                        if not autoCompleteList:
                            return complete_event
                elif mainCommandDef["arguments"]:
                    for arg in mainCommandDef["arguments"]:
                        autoCompleteList.append(arg["argument"])
                else:
                    return complete_event
            else:
                return complete_event 
        else:
            autoCompleteList = sorted(Commands.keys())

        if autoCompleteList:
            if utils.full_process(wordBeforeCursor):
                matches = process.extract(wordBeforeCursor, autoCompleteList)
                for m in matches:
                    yield Completion(m[0], start_position=-len(wordBeforeCursor))
            else:
                for m in autoCompleteList:
                    yield Completion(m, start_position=0)