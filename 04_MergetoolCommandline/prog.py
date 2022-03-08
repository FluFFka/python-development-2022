import shlex
import cmd
import readline
import pynames
import inspect

lang = pynames.LANGUAGE.NATIVE
lang_default = pynames.LANGUAGE.NATIVE
gender_default = pynames.GENDER.MALE

exs = ['FIXTURES_DIR', 'FromTablesGenerator', 'FromCSVTablesGenerator', 'FromListGenerator', 'os']

def print_name(generator, gender=gender_default, lang=lang_default):
    try:
        print(generator().get_name_simple(gender, lang))
    except Exception:
        print(generator().get_name_simple(gender, lang_default))


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

    def do_generate(self, arg):
        args = shlex.split(arg, comments=True)
        gens = pynames.generators.__all__
        if len(args) >= 1:
            name_class = args[0]
            gen_class = eval(f"pynames.generators.{name_class}")
            gen_subclass = []
            for i in inspect.getmembers(gen_class):
                if not i[0].startswith('__') and not i[0] in exs:
                    ds = ['Fullname', 'Generator', 'Names', 'Name']
                    i = list(i)
                    for d in ds:
                        i[0] = i[0].replace(d, '')
                    gen_subclass.append(i)
            
            if len(args) < 2:
                print_name(gen_subclass[0][1], lang=lang)
                return
            arg2 = args[1]
            for i in gen_subclass:
                if arg2 == i[0]:
                    if len(args) < 3:
                        print_name(i[1], lang=lang)
                    else:
                        arg2 = args[2]
                        if arg2 in ('male', 'female'):
                            arg2 = pynames.GENDER.MALE if arg2 == 'male' else pynames.GENDER.FEMALE
                            print_name(i[1], gender=arg2, lang=lang)
                        else:
                            print('Gender must be male or female')
                    return
            if arg2 in ('male', 'female'):
                arg2 = pynames.GENDER.MALE if arg2 == 'male' else pynames.GENDER.FEMALE
                print_name(gen_subclass[0][1], gender=arg2, lang=lang)
                return 
            print('Command pattern: generate <class> [subclass] [gender]')
        else:
            print('Command pattern: generate <class> [subclass] [gender]')
    
    def complete_generate(self, prefix, linef, beg, end):
        line = shlex.split(linef, comments=True)
        gens = pynames.generators.__all__
        if len(line) == 1:
            return gens
        if len(line) == 2:
            if not (line[1] in gens):
                return [s for s in gens if s.startswith(line[1])]
        if len(line) <= 3:
            gen_subclass = []
            gen_class = eval(f"pynames.generators.{line[1]}")
            try:
                for i in inspect.getmembers(gen_class):
                    if not i[0].startswith('__') and not i[0] in exs:
                        ds = ['Fullname', 'Generator', 'Names', 'Name']
                        i = list(i)
                        for d in ds:
                            i[0] = i[0].replace(d, '')
                        gen_subclass.append(i)
            except:
                return []
            if len(line) == 2 and linef[-1] == ' ':
                return [s[0] for s in gen_subclass]
            for i in gen_subclass:
                if line[2] == i[0]:
                    break
            else:
                return [s[0] for s in gen_subclass if s[0].startswith(line[2])]
        if len(line) <= 4:
            if len(line) == 3 and linef[-1] == ' ':
                return ['male', 'female']
            return [s for s in ('male', 'female') if s.startswith(line[3])]
        return []

    def do_exit(self, arg):
        return True


repl().cmdloop()
