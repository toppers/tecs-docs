# -*- coding: utf-8 -*-
"""
    tecslexer
    ~~~~~~~~~~~~~~~~
    TECS lexer for Pygments.
    :copyright:
    :license:
"""

from pygments.lexer import RegexLexer, include, bygroups, inherit, words, \
    default
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation
from pygments.lexers.c_cpp import CLexer, CppLexer

__all__ = ['TecsCdlLexer']

class TecsCdlLexer(CLexer):
    name = 'TECS CDL'
    aliases = ['tecs-cdl']
    filenames = ['*.cdl']
    mimetypes = ['text/x-tecs-cdl']

    tokens = {
        'statements': [
            (words((
                'celltype', 'cell', 'composite', 'signature', 'call', 'entry',
                'attr', 'var', 'in', 'out', 'size', 'count', 'string', 'const',
                'factory', 'FACTORY', 'C_EXP',
                'write'

                'asm', '__asm__', 'auto', 'bool', '_Bool', 'char', '_Complex',
                'double', 'enum', 'float', '_Imaginary', 'int', 'long', 'short',
                'signed', 'struct', 'typedef', 'union', 'unsigned', 'void',

                'int8_t', 'int16_t', 'int32_t', 'int64_t', 'uint8_t',
                'uint16_t', 'uint32_t', 'uint64_t', 'int_least8_t',
                'int_least16_t', 'int_least32_t', 'int_least64_t',
                'uint_least8_t', 'uint_least16_t', 'uint_least32_t',
                'uint_least64_t', 'int_fast8_t', 'int_fast16_t',
                'int_fast32_t', 'int_fast64_t', 'uint_fast8_t', 'uint_fast16_t',
                'uint_fast32_t', 'uint_fast64_t', 'intptr_t', 'uintptr_t',
                'intmax_t', 'intmax_t', 'uintmax_t', 'uintmax_t'), suffix=r'\b'),
             Keyword),
            #(r'()',
            # Keyword.Type),
            (r'[~!%^&*+=|?:<>/@-]', Operator),
            inherit,
        ],
    }

def setup(app):
    app.add_lexer('tecs-cdl', TecsCdlLexer(stripnl=False))
