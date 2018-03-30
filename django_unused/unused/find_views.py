import importlib, inspect, types, os
from django.core.urlresolvers import RegexURLResolver, RegexURLPattern
from django.views.generic import View
from django.apps import apps
from django.conf import settings


def get_view_files():
    """
    Gets any file named 'views.py' or any .py file inside a 'views' directory.
    Only checks user-created apps in INCLUDED_APPS.
    Adds the BASE_DIR to the beginning of the path so that searching for subclasses will return all subclasses.
    """
    # view_files = []
    view_file_paths = []
    # Get app configs
    # print('BASE:', settings.BASE_DIR)
    for config in apps.get_app_configs():
        # If the app is a user created app
        # print('CONFIG:', config.name)
        # print('  ', config)
        # print('  ', config.path)

        if config.path.find(settings.BASE_DIR) > -1:
            for root, dirs, filenames in os.walk(config.path):
                # files either directly inside of or in a sub dir of a 'views' directory
                # print('    ', 'ROOT:', root)
                # print('    ', 'DIRS:', dirs)
                # print('    ', 'FILES:', filenames)
                if os.path.basename(root) == 'views':
                    for sub_root, sub_dirs, sub_filenames in os.walk(root):
                        for filename in sub_filenames:
                            if filename.endswith('.py'):
                                # view_files.append(filename)
                                # print('    --', filename)
                                # print('      ', os.path.splitext(filename))
                                # print('      ', os.path.splitext(filename)[0])
                                # print('      ', sub_root)
                                # print('      ', os.path.join('..', sub_root))
                                # print('      ', os.path.relpath(sub_root, start=settings.BASE_DIR))
                                # print('      ', sub_root.replace(settings.BASE_DIR, ''))
                                # print('      ')
                                view_file_paths.append(os.path.join(os.path.relpath(sub_root, start=settings.BASE_DIR),
                                                                    os.path.splitext(filename)[0]).replace('\\', '/'))
                # Files named 'views.py
                for filename in filenames:
                    if filename == 'views.py':
                        # view_files.append(filename)
                        view_file_paths.append(os.path.join(os.path.relpath(root, start=settings.BASE_DIR),
                                                            os.path.splitext(filename)[0]).replace('\\', '/'))

    return view_file_paths


def get_views(view_file_paths):
    """
    Given a list of files with their paths, return a list of all the views in those files.
    :param {list} view_file_paths: A list of view files including their paths relative to the project root.
    :return: A list which contains all the views which reside in the files.
    """
    views = []
    for path in view_file_paths:
        # import the module at the path
        dot_path = path.replace('/', '.')
        mod = importlib.import_module(dot_path)
        # Get each class from the module
        # Adapted from https://stackoverflow.com/a/5520589
        classes = [c for c in inspect.getmembers(mod, inspect.isclass) if c[1].__module__ == mod.__name__]
        if classes:
            # Add each view class to the list
            for c in classes:
                view = c[1]
                if issubclass(view, View):
                    views.append(c[1])
    return views


def get_url_view_names():
    """
    Returns all the names of all the views called by the URLS.
    Adapted from https://stackoverflow.com/a/32935392
    """
    root_urlconf = __import__(settings.ROOT_URLCONF)
    urlpatterns = root_urlconf.urls.urlpatterns
    # These are all Django created views.
    non_matches = ['index', 'login', 'logout', 'password_change', 'password_change_done', 'i18n_javascript', 'shortcut',
                   'changelist_view', 'add_view', 'history_view', 'delete_view', 'change_view', 'RedirectView',
                   'user_change_password', 'changelist_view', 'add_view', 'history_view', 'delete_view', 'change_view',
                   'RedirectView', 'app_index']

    url_view_names = get_view_names(urlpatterns, non_matches)
    return url_view_names


def get_view_names(url_list, non_matches, view_names=None):
    """
    Given a list of urlpatterns, return the names of all the views the URLs use.
    Adapted from https://stackoverflow.com/a/1829565 and http://code.activestate.com/recipes/576974/
    :param url_list: The urlpatterns.
    :param non_matches: A list of view names to be excluded.
    :param view_names: The final list of names.
    :return:
    """
    if view_names is None:
        view_names = []
    for entry in url_list:
        # If the entry is not a single pattern, recursively traverse the lists until we hit a single pattern.
        if hasattr(entry, 'url_patterns'):
            get_view_names(entry.url_patterns, non_matches, view_names)
        # If a single pattern is not one of the non-matches, add it to our list of view names.
        elif entry.callback.__name__ not in non_matches:
            view_names.append(entry.callback.__name__)

    return view_names





