import fileinput
import os
from collections import MutableSequence
from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Lists all unused template files.'
    template_extensions = ['html', 'xml', 'rml', 'txt', 'csv', ]
    python_extensions = ['py', ]

    def add_arguments(self, parser):
        pass  # parser.add_argument('poll_id', nargs='+', type=int)
        # parser.add_argument('--many', dest='many', action='store_true', default=False,
        #                     help='create db for many migrations')

    def handle(self, *args, **options):
        global_templates_files, global_templates = self.find_global_templates()
        app_templates_files, app_templates = self.find_app_templates()
        templates = global_templates + app_templates
        template_files = global_templates_files + app_templates_files
        # templates.sort()
        template_files.sort()

        py_files, pys = self.find_py_files()

        # templates = {}
        # for index, template in enumerate(global_templates):
        #     if template not in templates.keys():
        #         templates.update({template: {'dirs': [],
        #                                      'used_in_template': [],
        #                                      'used_in_python': []}})
        #
        #     templates[template]['dirs'].append('BASE_DIR{}'.format(global_templates_files[index].replace(settings.BASE_DIR, '')))
        #
        # for index, template in enumerate(global_templates):
        #     if template not in templates.keys():
        #         templates.update({template: {'dirs': [],
        #                                      'used_in_template': [],
        #                                      'used_in_python': []}})
        #
        #     templates[template]['dirs'].append('BASE_DIR{}'.format(global_templates_files[index].replace(settings.BASE_DIR, '')))
        #
        # print('----------')
        # print(templates)
        # print('----------')

        all_files = py_files + template_files

        tl_count = [0 for t in templates]
        unused_templates = []

        for index, template in enumerate(templates):
            for line in fileinput.input(all_files):  # Loops through every line of every file
                # print([template, line])
                if str.find(line, template) > -1:
                    print(['FOUND', template, line])
                    tl_count[index] += 1

            if tl_count[index] == 0:
                unused_templates.append(template)
                # print(template)
            # else:
            #     print(['FOUND', tl_count[index], template])
        print(os.linesep.join(unused_templates))

        # setattr(unused_templates, '__eq__', lambda: False)
        self.stdout.ending = None
        return unused_templates

    def find_app_templates(self):
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
                        templates.append(template.replace(dir, '')[1:])
        return template_files, templates

    def find_global_templates(self):
        templates = []
        template_files = []
        if settings.TEMPLATES:
            for template_backend in settings.TEMPLATES:
                for dir in template_backend.get('DIRS', []):
                    for root, dirs, files in os.walk(dir):
                        for file in files:
                            template = os.path.join(root, file)
                            template_files.append(template)
                            templates.append(template.replace(dir, '')[1:])
        return template_files, templates

    def find_py_files(self):
        pys = []
        py_files = []
        for config in apps.get_app_configs():
            if config.path.find(settings.BASE_DIR) > -1:
                dir = config.path
                for root, dirs, files in os.walk(dir):
                    if 'example/server/tests' in root:
                        print('excluding: {}'.format(root))
                        continue
                    for file in files:
                        filename, extension = os.path.splitext(file)
                        if extension[1:] in self.python_extensions:
                            print(['py_files', file])
                            template = os.path.join(root, file)
                            py_files.append(template)
                            pys.append(template.replace(dir, '')[1:])
        return py_files, pys
