# -*- coding: utf-8 -*-
"""
    tecs
    ~~~~~~~~~~~~~~~~
    The TECS CDL domain.
    :copyright:
    :license:
"""

import re
import string

from docutils import nodes

from sphinx import addnodes
from sphinx.roles import XRefRole
from sphinx.domains import Domain, ObjType
from sphinx.directives import ObjectDescription
from sphinx.locale import l_, _
from sphinx.util.nodes import make_refnode
from sphinx.util.docfields import Field, TypedField

from sphinx.domains.c import CObject

# RE to split at word boundaries
wsplit_re = re.compile(r'(\W+)')

# REs for TECS entities
# TODO: support something like [omit]?
# TODO: maybe there's no need to include "containing something" in these regexs
tecs_ct_sig_re = re.compile(
    r'''^ ((?:\w+::)*)       # containing namespace
          (\w+)              # cell type name
          \s*$               # end of signature
          ''', re.VERBOSE)

tecs_port_sig_re = re.compile(
    r'''^ (\w+(?:::\w+)*)\s+    # signature
          (\w+)              # port name
          \s*$               # end of signature
          ''', re.VERBOSE)

# TODO: support other kind of types: function pointer, etc.
tecs_va_sig_re = re.compile(
    r'''^ (.+?)\b\s*         # type
          (\w+)              # var/attr name
          \s*$               # end of signature
          ''', re.VERBOSE)

tecs_sigfn_sig_re = re.compile(
    r'''^ (\[.+\])?\s*       # attributes
          ([^(]+?)\b\s*      # return type
          (\w+)\s*           # function name
          \((.*)\)           # arguments
          \s*$               # end of signature
          ''', re.VERBOSE)

tecs_fnparam_sig_re = re.compile(
    r'''^ (\[.+?\])?\s*      # attributes
          (.+?)\b\s*         # type
          (\w+)              # parameter name
          \s*$               # end of signature
          ''', re.VERBOSE)

class TECSObject(ObjectDescription):
    """Description of a TECS object.
    """

    # stopwords imported from C
    stopwords = CObject.stopwords

    def get_index_text(self, name):
        raise NotImplementedError("must be implemented in subclass")

    def add_target_and_index(self, name, sig, signode):
        targetname = 'c.' + name

        if targetname not in self.state.document.ids:
            inv = self.env.domaindata['tecs']['objects']
            if name in inv:
                self.state_machine.reporter.warning(
                    'duplicate C object description of %s, ' % name +
                    'other instance in ' + self.env.doc2path(inv[name][0]),
                    line=self.lineno)
            inv[name] = (self.env.docname, self.objtype)

        indextext = self.get_index_text(name)
        if indextext:
            self.indexnode['entries'].append(('single', indextext,
                                              targetname, '', None))

    def _parse_c_type(self, node, ctype):
        # add cross-ref nodes for all words
        for part in [_f for _f in wsplit_re.split(ctype) if _f]:
            tnode = nodes.Text(part, part)
            if part[0] in string.ascii_letters+'_' and \
               part not in self.stopwords:
                pnode = addnodes.pending_xref(
                    '', refdomain='c', reftype='type', reftarget=part,
                    modname=None, classname=None)
                pnode += tnode
                node += pnode
            else:
                node += tnode


class TECSSignatureObject(TECSObject):
    """Description of a TECS signature.
    """
    def handle_signature(self, sig, signode):
        """Transform a TECS signature signature into RST nodes.

        Returns fully qualified name of the signature
        """
        m = tecs_ct_sig_re.match(sig)
        if m is None:
            raise ValueError
        name_prefix, name = m.groups()
        if name_prefix:
            name_prefix = '::'.join((e.strip() for e in name_prefix.split('::')))
            fullname = name_prefix + name
        else:
            fullname = name

        signode += addnodes.desc_annotation('signature', 'signature')
        signode += nodes.Text(' ', '')
        if name_prefix:
            signode += addnodes.desc_addname(name_prefix, name_prefix)
        signode += addnodes.desc_name(name, name)

        return fullname

    def get_index_text(self, name):
        return _('%s (TECS signature)') % name

    def before_content(self):
        self.typename_set = False
        if self.names: # FIXME: what's "names"???
            self.env.ref_context['tecs:signature'] = self.names[0]
            self.typename_set = True

    def after_content(self):
        if self.typename_set:
            self.env.ref_context.pop('tecs:signature', None)

class TECSSignatureFunctionObject(TECSObject):
    def handle_signature(self, sig, signode):
        """Transform a TECS cell type signature into RST nodes.

        Returns fully qualified name of the cell type
        """
        m = tecs_sigfn_sig_re.match(sig)
        if m is None:
            raise ValueError
        attrs, ret_type, name, arglist = m.groups()

        sig_name = self.env.ref_context.get('tecs:signature')
        fullname = sig_name + '::' + name

        if attrs:
            signode += addnodes.desc_annotation(attrs, attrs)

        signode += addnodes.desc_type('', '')
        self._parse_c_type(signode[-1], ret_type)

        signode += addnodes.desc_name(name, u'\xa0' + name)

        paramlist = addnodes.desc_parameterlist()
        arglist = arglist.replace('`', '').replace('\\ ', '')  # remove markup

        # don't think about function pointer types for now...
        # TODO: don't split inside brackets!
        for arg in arglist.split(','):
            arg = arg.strip()
            param = addnodes.desc_parameter('', '', noemph=True)
            m = tecs_fnparam_sig_re.match(arg)
            if m:
                arg_attrs, arg_type, arg_name = m.groups()
                if arg_attrs:
                    param += addnodes.desc_annotation(arg_attrs, arg_attrs)
                self._parse_c_type(param, arg_type)
                # separate by non-breaking space in the output
                param += nodes.emphasis(' ' + arg_name, u'\xa0' + arg_name)
            else:
                # unrecognizable format
                # `(void)` also reaches here
                param += nodes.Text(arg, arg)

            paramlist += param
        signode += paramlist

        return fullname

    def get_index_text(self, name):
        return _('%s (TECS signature member)') % name

class TECSCellTypeObject(TECSObject):
    """Description of a TECS cell type.
    """
    def handle_signature(self, sig, signode):
        """Transform a TECS cell type signature into RST nodes.

        Returns fully qualified name of the cell type
        """
        m = tecs_ct_sig_re.match(sig)
        if m is None:
            raise ValueError
        name_prefix, name = m.groups()
        if name_prefix:
            name_prefix = '::'.join((e.strip() for e in name_prefix.split('::')))
            fullname = name_prefix + name
        else:
            fullname = name

        signode += addnodes.desc_annotation('celltype', 'celltype')
        signode += nodes.Text(' ', '')
        if name_prefix:
            signode += addnodes.desc_addname(name_prefix, name_prefix)
        signode += addnodes.desc_name(name, name)

        return fullname

    def get_index_text(self, name):
        return _('%s (TECS cell type)') % name

    def before_content(self):
        self.typename_set = False
        if self.names: # FIXME: what's "names"???
            self.env.ref_context['tecs:celltype'] = self.names[0]
            self.typename_set = True

    def after_content(self):
        if self.typename_set:
            self.env.ref_context.pop('tecs:celltype', None)

class TECSCellTypeMemberObject(TECSObject):
    """Description of a TECS cell type member (e.g., attributes, ports).
    """
    def get_signature_prefix(self, sig):
        """May return a prefix to put before the object name in the
        signature.
        """
        return ''

class TECSCellTypePortObject(TECSCellTypeMemberObject):
    def handle_signature(self, sig, signode):
        """Transform a TECS cell type signature into RST nodes.

        Returns fully qualified name of the cell type
        """
        m = tecs_port_sig_re.match(sig)
        if m is None:
            raise ValueError
        sig_name, name = m.groups()

        celltype = self.env.ref_context.get('tecs:celltype')
        fullname = celltype + '::' + name

        sig_prefix = self.get_signature_prefix(sig)
        signode += addnodes.desc_annotation(sig_prefix, sig_prefix)
        signode += nodes.Text(' ', '')
        signode += addnodes.desc_type('', '')
        pnode = addnodes.pending_xref(
            '', refdomain='tecs', reftype='signature', reftarget=sig_name,
            modname=None, classname=None)
        pnode += nodes.Text(sig_name, sig_name)
        signode[-1] += pnode
        signode += nodes.Text(' ', '')
        signode += addnodes.desc_name(name, u'\xa0' + name)

        return fullname

class TECSCellTypeCallPortObject(TECSCellTypePortObject):
    """Description of a TECS call port.
    """
    def get_signature_prefix(self, sig):
        return 'call'

    def get_index_text(self, name):
        return _('%s (TECS call port)') % name

class TECSCellTypeEntryPortObject(TECSCellTypePortObject):
    """Description of a TECS entry port.
    """
    def get_signature_prefix(self, sig):
        return 'entry'

    def get_index_text(self, name):
        return _('%s (TECS entry port)') % name


class TECSCellTypeVAObject(TECSCellTypeMemberObject):
    def handle_signature(self, sig, signode):
        """Transform a TECS cell type signature into RST nodes.

        Returns fully qualified name of the cell type
        """
        m = tecs_va_sig_re.match(sig)
        if m is None:
            raise ValueError
        va_type, name = m.groups()

        celltype = self.env.ref_context.get('tecs:celltype')
        fullname = celltype + '::' + name

        sig_prefix = self.get_signature_prefix(sig)
        signode += addnodes.desc_annotation(sig_prefix, sig_prefix + u'\xa0')

        signode += addnodes.desc_type('', '')
        self._parse_c_type(signode[-1], va_type)

        signode += addnodes.desc_name(name, u'\xa0' + name)

        return fullname

class TECSCellTypeAttributeObject(TECSCellTypeVAObject):
    """Description of a TECS entry port.
    """
    def get_signature_prefix(self, sig):
        return 'attr'

    def get_index_text(self, name):
        return _('%s (TECS cell type attribute)') % name

class TECSCellTypeVariableObject(TECSCellTypeVAObject):
    """Description of a TECS entry port.
    """
    def get_signature_prefix(self, sig):
        return 'var'

    def get_index_text(self, name):
        return _('%s (TECS cell type variable)') % name

class TECSXRefRole(XRefRole):
    def process_link(self, env, refnode, has_explicit_title, title, target):
        if not has_explicit_title:
            target = target.lstrip('~')  # only has a meaning for the title
            # if the first character is a tilde, don't display the module/class
            # parts of the contents
            if title[0:1] == '~':
                title = title[1:]
                scope = title.rfind('::')
                if scope != -1:
                    title = title[scope+2:]
        return title, target

class TECSDomain(Domain):
    """TECS (TOPPERS Embedded Component System) CDL domain.
    """
    name = 'tecs'
    label = 'TECS'
    object_types = {
        'celltype':     ObjType(l_('cell type'),    'celltype'),
        'cell':         ObjType(l_('cell'),         'cell'),
        'call':         ObjType(l_('call port'),    'call'),
        'entry':        ObjType(l_('entry port'),   'entry'),
        'attribute':    ObjType(l_('attribute'),    'attr'),
        'variable':     ObjType(l_('variable'),     'var'),
        'signature':    ObjType(l_('signature'),    'signature'),
        'sigfunction':  ObjType(l_('sigfunction'),  'sigfunction'),
        'namespace':    ObjType(l_('namespace'),    'namespace'),
    }
    directives = {
        'celltype':     TECSCellTypeObject,
        'call':         TECSCellTypeCallPortObject,
        'entry':        TECSCellTypeEntryPortObject,
        'attr':         TECSCellTypeAttributeObject,
        'var':          TECSCellTypeVariableObject,
        'signature':    TECSSignatureObject,
        'sigfunction':  TECSSignatureFunctionObject
    }
    roles = {
        'celltype':     TECSXRefRole(),
        'cell':         TECSXRefRole(),
        'call':         TECSXRefRole(),
        'entry':        TECSXRefRole(),
        'attr':         TECSXRefRole(),
        'var':          TECSXRefRole(),
        'signature':    TECSXRefRole(),
        'sigfunction':  TECSXRefRole(),
        'namespace':    TECSXRefRole(),
    }
    initial_data = {
        'objects': {}, # full name -> docname, objtype
    }

    def clear_doc(self, docname):
        for fullname, (fn, _l) in list(self.data['objects'].items()):
            if fn == docname:
                del self.data['objects'][fullname]

    def merge_domaindata(self, docnames, otherdata):
        for fullname, (fn, objtype) in otherdata['objects'].items():
            if fn in docnames:
                self.data['objects'][fullname] = (fn, objtype)

    def resolve_xref(self, env, fromdocname, builder,
                     typ, target, node, contnode):
        if target not in self.data['objects']:
            return None
        obj = self.data['objects'][target]
        return make_refnode(builder, fromdocname, obj[0], 'tecs.' + target,
            contnode, target)

    def resolve_any_xref(self, env, fromdocname, builder, target,
                         node, contnode):
        if target not in self.data['objects']:
            return []
        obj = self.data['objects'][target]
        return [('tecs:' + self.role_for_objtype(obj[1]),
                 make_refnode(builder, fromdocname, obj[0], 'c.' + target,
                              contnode, target))]

    def get_objects(self):
        for refname, (docname, type) in list(self.data['objects'].items()):
            yield (refname, refname, type, docname, 'tecs.' + refname, 1)

def setup(app):
    app.add_domain(TECSDomain)
