import sys
import importlib
import inspect
import ast
import textwrap
import difflib

f_texts = []

for arg in sys.argv[1:]:
    module_name = arg
    module = importlib.import_module(module_name)
    for mem in inspect.getmembers(module):
        if mem[0][:2] != '__':
            if not inspect.ismodule(mem[1]):
                if inspect.isclass(mem[1]):
                    for inner in inspect.getmembers(mem[1]):
                        if inspect.isfunction(inner[1]):
                            f_texts.append((module_name + '.' + mem[0] + '.' + inner[0], inspect.getsource(inner[1])))
                elif inspect.isfunction(inner[1]):
                    f_texts.append((module_name + '.' + mem[0], inspect.getsource(mem[1])))
"""
with open(sys.argv[1] + '.py') as f:
    prog_text = f.read()
    tree = ast.parse(prog_text)
#print(ast.dump(tree, indent=4))

functions = []

module_name = sys.argv[1]

for inst in tree.body:
    if isinstance(inst, ast.FunctionDef):
        functions.append((inst.name, inst))
    elif isinstance(inst, ast.ClassDef):
        for inner in inst.body:
            if isinstance(inner, ast.FunctionDef):
                functions.append((inst.name + '.' + inner.name, inner))
"""

changed = []

for name, text in f_texts:
    T = ast.parse(textwrap.dedent(text))
     
    for i in ast.walk(T):
        if hasattr(i, 'name'):
            i.name = '_'
        if hasattr(i, 'id'):
            i.id = '_'
        if hasattr(i, 'arg'):
            i.arg = '_'
        if hasattr(i, 'attr'):
            i.attr = '_'
    changed.append((name, ast.unparse(T)))

for i in range(len(changed)):
    for j in range(i+1, len(changed)):
        if difflib.SequenceMatcher(None, changed[i][1], changed[j][1]).ratio() > 0.95:
            print(changed[i][0], ':', changed[j][0])
