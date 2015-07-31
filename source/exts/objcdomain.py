# -*- coding: utf-8 -*-
"""
    sphinx.domains.objc
    ~~~~~~~~~~~~~~~~~~~

    The Objective C domain.
"""

import re
from sphinx.locale import l_, _
from sphinx import addnodes
from sphinx.directives import ObjectDescription
from sphinx.domains import Domain, ObjType
from docutils import nodes


class ObjCAgument(object):
    def __init__(self, selector_part, has_arg, type, name):
        self.selector_part = selector_part
        self.has_arg = not not has_arg
        self.type = type
        self.name = name

    @property
    def type_str(self):
        if self.type:
            return '(%s)' % self.type
        else:
            return ''
    @property
    def name_str(self):
        if self.name:
            return self.name
        else:
            return ''

    @property
    def selector_part_with_colon(self):
        return self.selector_part + (':' if self.has_arg else '')

    def __repr__(self):
        if not self.has_arg:
            return self.selector_part
        else:
            return "%(selector_part)s:%(type)s%(name)s" % dict(selector_part=self.selector_part,
                                                               type=self.type_str,
                                                               name=self.name_str)

class ObjCSignature(ObjectDescription):
    objc_sig_parts = re.compile(
        r'''
            (?P<selector_part>\w+)(?P<has_arg>:(?:\((?P<type>[\w *]+)\))?(?P<name>\w+)?)?\ ?
        ''', re.VERBOSE)
    objc_sig_outer = re.compile(
        r'''^ (?P<class_or_instance>[+-])?          # optional whether it's public or private
                (?:\((?P<return_type>[\w *]+)\))?       # optional return type
                (?:\[(?P<class_name>\w+)\ )?        # if it has an open brace, then a class name
                (?P<inner_signature>
                    (?:
                        \w+(?::(?:\([\w *]+\))?(?:\w+)?)?\ ?
                    )+
                )
             (?(class_name)\]|)$ # if we have a class name, we need the closing brace
        ''', re.VERBOSE)
    
    def handle_signature(self, sig, signode):
        groups = self.objc_sig_outer.match(sig).groupdict()

        self.class_name = groups.get('class_name')
        # default to instance method
        self.is_class_method = groups.get('class_or_instance') == '+'
        self.return_type = groups.get('return_type')

        inner_sig = groups['inner_signature']
        self.arguments = [ObjCAgument(**part.groupdict()) for part in self.objc_sig_parts.finditer(inner_sig)]

        signode += nodes.Text(self.return_type_str)
        signode += addnodes.desc_addname(self.selector_with_args, self.selector_with_args)

        return '%s::%s' % (self.class_name, self.selector)
    
    @property
    def return_type_str(self):
        if self.return_type:
            return '(%s)' % self.return_type
        else:
            return ''

    @property
    def class_instance_str(self):
        if self.is_class_method:
            return '+'
        else:
            return '-'

    @property
    def selector(self):
        return ''.join(a.selector_part_with_colon for a in self.arguments)

    @property
    def selector_with_args(self):
        return ' '.join(repr(a) for a in self.arguments)

    @property
    def full_name(self):
        return "%s %s[%s %s]" % (
            self.class_instance_str,
            self.return_type_str,
            self.class_name,
            self.selector_with_args,
        )

    @property
    def short_name(self):
        return "%s %s%s" % (
            self.class_instance_str,
            self.return_type_str,
            self.selector_with_args,
        )

    @property
    def ref_name(self):
        return "%s[%s %s]" % (
            self.class_instance_str,
            self.class_name,
            self.selector,
        )

    def __repr__(self):
        if self.class_name:
            return self.full_name
        else:
            return self.short_name


class ObjectiveCDomain(Domain):
    name = 'objc'
    label = 'ObjectiveC'
    object_types = {
        'method': ObjType(l_('method'), 'method'),
    }

    directives = {
        'method': ObjCSignature,
    }
    initial_data = {
        'objects': {},  # fullname -> docname, objtype
    }

    def clear_doc(self, docname):
        for fullname, (fn, _) in self.data['objects'].items():
            if fn == docname:
                del self.data['objects'][fullname]

    def resolve_xref(self, env, fromdocname, builder,
                     typ, target, node, contnode):
        pass

    def get_objects(self):
        for refname, (docname, type) in self.data['objects'].iteritems():
            yield (refname, refname, type, docname, refname, 1)


def setup(app):
    app.add_domain(ObjectiveCDomain)
