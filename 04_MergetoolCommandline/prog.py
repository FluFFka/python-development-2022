import shlex
import cmd
import readline
import pynames

lang = pynames.LANGUAGE.NATIVE
lang_default = pynames.LANGUAGE.NATIVE

class repl(cmd.Cmd):
    def do_language(self, arg):
        args = shlex.split(arg, comments=True)
        if len(args) >= 1:
            try:
                lang = eval(f"pynames.LANGUAGE.{args[0]}")
            except Exception:
                print(f"No language {args[0]}.")
                print("Available languages:", end=' ')
                print(*[i.upper() for i in pynames.LANGUAGE.ALL], sep=', ')
        else:
            print("Command template: language <language>")

    def complete_language(self, prefix, linef, beg, end):
        return [s.upper() for s in pynames.LANGUAGE.ALL if s.startswith(prefix)]

    def do_exit(self, arg):
        return True


repl().cmdloop()
