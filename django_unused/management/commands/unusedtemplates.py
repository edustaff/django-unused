# from __future__ import absolute_import

import fileinput
import os

from django.core.management.base import BaseCommand

from ...unused import find_py_files, find_app_templates, find_global_templates


class Command(BaseCommand):
    help = 'Lists all unused template files.'

    def add_arguments(self, parser):
        pass  # parser.add_argument('poll_id', nargs='+', type=int)
        # parser.add_argument('--many', dest='many', action='store_true', default=False,
        #                     help='create db for many migrations')

    def handle(self, *args, **options):
        global_templates_files, global_templates = find_global_templates()
        app_templates_files, app_templates = find_app_templates()
        templates = global_templates + app_templates
        template_files = global_templates_files + app_templates_files
        # templates.sort()
        template_files.sort()

        py_files, pys = find_py_files()

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

        self.stdout.ending = None  # work around because it's not a string
        return unused_templates
