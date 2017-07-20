# from __future__ import absolute_import


from django.core.management.base import BaseCommand

from ._templates import find_unused_templates


class Command(BaseCommand):
    help = 'Lists all unused template files.'

    def add_arguments(self, parser):
        pass  # parser.add_argument('poll_id', nargs='+', type=int)
        # parser.add_argument('--many', dest='many', action='store_true', default=False,
        #                     help='create db for many migrations')

    def handle(self, *args, **options):
        find_unused_templates()
        # self.stdout.ending = None  # work around because it's not a string
