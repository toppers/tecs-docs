# -*- coding: utf-8 -*-
"""
    latexfix
    ~~~~~~~~~~~~~~~~
    Altered shinx.builders.LaTeXBuilder that handles no-break spaces correctly.
    :copyright:
    :license:
"""

from os import path
from sphinx.builders.latex import LaTeXBuilder

class MyLaTeXBuilder(LaTeXBuilder):
    name = 'latex-fixed'
    def write(self, *ignored):
        super(MyLaTeXBuilder, self).write(*ignored)

        # Rewrite destination files
        for entry in self.document_data:
            docname, targetname, title, author, docclass = entry[:5]

            destination_path = path.join(self.outdir, targetname)

            with open(destination_path) as f:
                text = f.read()

            # Replace U+00A0 characters (no-break space) with LaTeX
            # non-breaking spaces
            text = text.replace(u'\xa0', u'~')

            with open(destination_path, 'w') as f:
                f.write(text)

def setup(app):
    app.add_builder(MyLaTeXBuilder)
    app.add_latex_package('hyperref', 'dvipdfmx')
