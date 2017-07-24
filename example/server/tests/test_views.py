from django.core.management import call_command
from django.test import TestCase

from django_unused.unused.find_views import get_view_files, get_views, get_url_view_names


class UnusedViewTestCase(TestCase):
    def test_get_view_files(self):
        files = get_view_files()
        self.assertEqual(files, ['server/views/view_not_named_view', 'server/views/__init__',
                                 'server/views/sub/view_file', 'server/views/sub/__init__',
                                 'app1/views'])

    def test_get_views(self):
        files = get_view_files()
        views = get_views(files)
        self.assertEqual(len(views), 5)
        self.assertEquals(views[0].__name__, 'ServerView')
        self.assertEquals(views[1].__name__, 'UnusedView')
        self.assertEquals(views[2].__name__, 'UsedView')
        self.assertEquals(views[3].__name__, 'SubApp1View')
        self.assertEquals(views[4].__name__, 'App1View')

    def test_get_url_view_names(self):
        url_view_names = get_url_view_names()
        self.assertEqual(url_view_names, ['ServerView', 'UsedView'])

    def test_run_unusedtemplates_with_no_args(self):
        call_command('unused', 'views')