from os import chdir

from .client.workspace import Workspace
from .client.translator import loop_variable, Var, ParseError, Symbol

__version__ = '1.0.2'
__all__ = [
    'Workspace', 'loop_variable', 'Var', 'ParseError', 'Symbol',
    'generate_static_completion'
]


def generate_static_completion():
    from subprocess import run
    from .client.extract import functions_by_prefix
    from .client.functions import name_without_prefix
    from pathlib import Path
    from re import fullmatch
    from keyword import iskeyword

    ident = r'[a-zA-Z_][a-zA-Z0-9_]*'

    client = Path(__file__).parent.absolute() / 'client'
    chdir(client)
    run(['stubgen', 'workspace.py', '-o', '.'])

    functions = functions_by_prefix()
    with open('workspace.pyi', 'a') as fout:
        for key, values in functions.items():
            if not fullmatch(ident, key) or iskeyword(key):
                continue

            fout.write(f'    class {key}:\n')
            lines = 0

            for func in values:
                name = name_without_prefix(func.name)

                if not fullmatch(ident, name) or iskeyword(name):
                    continue

                lines += 1
                fout.write(f'        def {name}(*args, **kwargs): ...\n')

            if not lines:
                fout.write('        pass\n')
