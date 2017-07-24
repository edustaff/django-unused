# from __future__ import absolute_import
from django.core.management.base import BaseCommand

from ._templates import find_unused_templates
from ._views import find_unused_views


class Command(BaseCommand):
    help = 'Lists all unused template files.'

    def add_arguments(self, parser):
        # Unused_type is the parameter of the type of file you want to find.
        parser.add_argument('unused_type')

    def handle(self, *args, **options):
        unused_type = options['unused_type']
        if unused_type.lower() == 'templates' or unused_type.lower() == 'template':
            find_unused_templates()
        elif unused_type.lower() == 'views' or unused_type.lower() == 'view':
            find_unused_views()
        elif unused_type.lower() == 'media':
            print('media')
        else:
            return unused_type + ' is not a valid parameter. Valid parameters are templates, views, and media.'
        # self.stdout.ending = None  # work around because it's not a string
