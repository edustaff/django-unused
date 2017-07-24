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
    view_files = []
    view_file_paths = []
    # Get app configs
    for config in apps.get_app_configs():
        # If the app is a user created app
        if config.path.find(settings.BASE_DIR) > -1:
            for root, dirs, filenames in os.walk(config.path):
                # files either directly inside or in a sub dir of a 'views' directory
                if os.path.basename(root) == 'views':
                    for sub_root, sub_dirs, sub_filenames in os.walk(root):
                        for filename in sub_filenames:
                            if filename.endswith('.py'):
                                # view_files.append(filename)
                                view_file_paths.append(os.path.join(
                                                                    os.path.relpath(os.path.join('../', sub_root)),
                                                                    os.path.splitext(filename)[0]).replace('\\', '/'))
                # Files named 'views.py
                for filename in filenames:
                    if filename == 'views.py':
                        # view_files.append(filename)
                        view_file_paths.append(os.path.join(
                                                            os.path.relpath(root),
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


# List for the view names found in the URLs.
url_view_names = []


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
    get_view_names(urlpatterns, non_matches)

    return url_view_names


def get_view_names(urlpatterns, non_matches):
    """
    Pulling this function out allows it to be called recursively.

    :param urlpatterns: A list of URL patterns.
    :param non_matches: View names which will be excluded.
    """
    for pattern in urlpatterns:
        # If the pattern is a resolver, keep going down the chain until we get to an actual pattern
        if isinstance(pattern, RegexURLResolver):
            get_view_names(pattern.url_patterns, non_matches)
        # Then, if the pattern is not excluded, add it to the list.
        elif isinstance(pattern, RegexURLPattern) and pattern.callback.__name__ not in non_matches:
            url_view_names.append(pattern.callback.__name__)
