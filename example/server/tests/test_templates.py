from django.core.management import call_command
from django.test import TestCase

from django_unused.unused.find_templates import find_app_templates, find_global_templates, find_py_files


class UnusedTemplateTestCase(TestCase):
    def test_find_app_templates(self):
        template_files, templates = find_app_templates()

        # self.assertEqual(template_files, [])  # not sure who to do this
        self.assertEqual(templates, ['server/unused.html',
                                     'server/sub1/used_in_tpl.html',
                                     'app1/used_in_view.html'])

    def test_find_global_templates(self):
        template_files, templates = find_global_templates()

        # self.assertEqual(template_files, [])
        self.assertEqual(templates, ['server/used_in_view.html', 'server/sub1/unused.html'])

    def test_find_py_files(self):
        py_files, pys = find_py_files()

        self.assertEqual(len(py_files), 13)
        self.assertEqual(len(py_files), 13)

    def test_run_unusedtemplates_with_no_args(self):
        call_command('unused', 'templates')
