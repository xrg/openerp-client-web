import inspect

import pooler

__all__ = ['TemplateEditor']

EDITORS_GROUP = '_terp_template_editors'
def edition_preprocessor(template_text):
    # inspect.currentframe() -> logging_preprocessor
    #        .f_back         -> mako.lexer.Lexer.parse
    #        .f_back         -> mako.template._compile_text or mako.template._compile_module_file
    template = inspect.currentframe().f_back.f_back.f_locals['template']

    Editor = pooler.get_pool().get(template.uri, group=EDITORS_GROUP)

    if Editor:
        return Editor().edit(template, template_text)
    return template_text

class EditorType(type):
    def __init__(cls, name, bases, attributes):
        super(EditorType, cls).__init__(name, bases, attributes)
        for template in attributes.get('templates', []):
            pooler.register_object(cls, template, group=EDITORS_GROUP)

class TemplateEditor(object):
    """
    Template edition object. Subclass to specify edition/overrides to
    perform on existing Mako templates before lexing and interpreting
    them.

    :var templates: A list of templates to match for edition, as
                    strings, from the web client root, starting with a
                    '/'
    """
    __metaclass__ = EditorType

    def edit(self, template, template_text):
        """
        Template-edition method to override: edits the text content of
        a raw Mako template (before lexing or any other processing)
        and returns the edited template text as a unicode object.

        All templates specified in the ``templates`` class attribute
        will be sent here for processing.

        TemplateEditor instances should call their super().edit either
        before or after their own processing, and use its output as
        their own input or output.

        :param template: The Mako template object, created but not yet
                         lexed and compiled. May be used to extract
                         more data on the context in which the
                         template editor executes, and decide whether
                         it's going to perform any edition or return
                         the original template as-is.
        :type template: :py:class:`mako.template.Template`
        :param template_text: The text of the current template, which
                              should be returned unchanged or with any
                              necessary edition.
        :type template_text: unicode
        :rtype: unicode
        """
        return template_text
