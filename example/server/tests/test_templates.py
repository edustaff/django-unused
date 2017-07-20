from django.test import TestCase

from django.core.management import call_command

class WorkingTestCase(TestCase):
    def test_that_is_is_working(self):
        unused_templates = call_command('unusedtemplates')

        self.assertEqual(unused_templates, ['server/sub1/unused.html', 'server/unused.html'])
