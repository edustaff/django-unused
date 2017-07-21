# Get registered views: https://stackoverflow.com/questions/1275486/django-how-can-i-see-a-list-of-urlpatterns/1275601#1275601
# https://stackoverflow.com/questions/32933229/how-to-get-a-list-of-all-views-in-a-django-application
import os
from django.apps import apps
from django.apps.config import AppConfig


def get_view_files():
    """
    Gets any file named 'views.py' or any .py file inside a 'views' directory.
    Only checks user-created apps in INCLUDED_APPS.
    """
    view_files = []
    view_file_paths = []
    # Get app configs
    for config in apps.get_app_configs():
        # If the app is a user created app
        if type(config) is AppConfig:
            for root, dirs, filenames in os.walk(config.path):
                # files inside a 'views directory
                if os.path.basename(root) == 'views':
                    for filename in filenames:
                        if filename.endswith('.py'):
                            view_files.append(filename)
                            view_file_paths.append(os.path.join(root, filename))
                # Files named 'views.py
                for filename in filenames:
                    if filename == 'views.py':
                        view_files.append(filename)
                        view_file_paths.append(os.path.join(root, filename))

    return view_files, view_file_paths

