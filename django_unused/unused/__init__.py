from collections import MutableSequence


class TemplateList(MutableSequence):
    pass


class Template(object):
    def __init__(self, template):
        self.template = template
