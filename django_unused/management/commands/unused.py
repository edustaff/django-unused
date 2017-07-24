# from __future__ import absolute_import
from django.core.management.base import BaseCommand

from ._templates import find_unused_templates, find_unused_templates_whoosh
from ._views import find_unused_views


class Command(BaseCommand):
    help = 'Lists all unused template files.'

    def add_arguments(self, parser):
        # Unused_type is the parameter of the type of file you want to find.
        parser.add_argument('unused_type', help='What to find: templates, views, media')
        parser.add_argument('--dev', dest='dev_mode', action='store_true', default=False,
                            help='Use development methods to find things')

    def handle(self, *args, **options):
        unused_type = options['unused_type']
        dev_mode = options.get('dev_mode', False)
        if unused_type.lower() in ['templates', 'template']:
            if dev_mode:
                find_unused_templates_whoosh()
            else:
                find_unused_templates()
        elif unused_type.lower() in ['views', 'view']:
            find_unused_views()
        elif unused_type.lower() == 'media':
            print('media')
        else:
            return unused_type + ' is not a valid parameter. Valid parameters are templates, views, and media.'
            # self.stdout.ending = None  # work around because it's not a string
