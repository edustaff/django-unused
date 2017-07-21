import os

from django.apps import apps
from django.conf import settings

template_extensions = ['html', 'xml', 'rml', 'txt', 'csv', ]
python_extensions = ['py', ]


def find_app_templates():
    templates = []
    template_files = []
    # if settings.TEMPLATES:
    #     for template_backend in settings.TEMPLATES:
    #         if template_backend.get('APP_DIRS', False):
    for config in apps.get_app_configs():
        if config.path.find(settings.BASE_DIR) > -1:
            dir = os.path.join(config.path, 'templates')
            for root, dirs, files in os.walk(dir):
                for file in files:
                    template = os.path.join(root, file)
                    template_files.append(template)
                    templates.append(template.replace(dir, '').replace('\\', '/')[1:])
    return template_files, templates


def find_global_templates():
    templates = []
    template_files = []
    if settings.TEMPLATES:
        for template_backend in settings.TEMPLATES:
            for dir in template_backend.get('DIRS', []):
                for root, dirs, files in os.walk(dir):
                    for file in files:
                        template = os.path.join(root, file)
                        template_files.append(template)
                        templates.append(template.replace(dir, '').replace('\\', '/')[1:])
    return template_files, templates


def find_py_files():
    pys = []
    py_files = []
    for config in apps.get_app_configs():
        if config.path.find(settings.BASE_DIR) > -1:
            dir = config.path
            for root, dirs, files in os.walk(dir):
                if os.path.join('example', 'server', 'tests') in root:  # todo: don't hard code?
                    print('excluding: {}'.format(root))
                    continue
                for file in files:
                    filename, extension = os.path.splitext(file)
                    if extension[1:] in python_extensions:
                        # print(['py_files', file])
                        template = os.path.join(root, file)
                        py_files.append(template)
                        pys.append(template.replace(dir, '')[1:])
    return py_files, pys
