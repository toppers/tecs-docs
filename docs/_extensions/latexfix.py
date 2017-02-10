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
from sphinx.util.console import bold

class MyLaTeXBuilder(LaTeXBuilder):
    name = 'latex-fixed'

    def __init__(self, *args, **kwargs):
        super(MyLaTeXBuilder, self).__init__(*args, **kwargs)

        self.usepackages.append(('hyperref', 'dvipdfmx'))

    def write(self, *ignored):
        super(MyLaTeXBuilder, self).write(*ignored)

        # Rewrite destination files
        self.info(bold('latexfix: patching destination files...'), nonl=1)
        for entry in self.document_data:
            docname, targetname, title, author, docclass = entry[:5]

            self.info(' '+targetname, nonl=1)

            destination_path = path.join(self.outdir, targetname)

            with open(destination_path) as f:
                text = f.read()

            # Replace U+00A0 characters (no-break space) with LaTeX
            # non-breaking spaces
            text = text.replace('\xa0', '~')

            with open(destination_path, 'w') as f:
                f.write(text)
        self.info()

    def finish(self):
        super(MyLaTeXBuilder, self).finish()

        self.info(bold('latexfix: patching support files...'))

        # Patch sphinx.sty so the compilation doesn't fail because of option clash
        sty_path = path.join(self.outdir, 'sphinx.sty')
        with open(sty_path) as f:
            text = f.read()

        i = text.find('\\newcount\\pdfoutput\\pdfoutput=0')
        if i == -1:
            self.warn('Marker not found. Skipping.')
        else:
            inserted = '\\PassOptionsToPackage{dvipdfmx}{hyperref}'
            inserted += '\\PassOptionsToPackage{dvipdfmx}{graphicx}'
            text = text[:i] + inserted + text[i:]

        with open(sty_path, 'w') as f:
            f.write(text)

        self.info('done')

def setup(app):
    app.add_builder(MyLaTeXBuilder)
