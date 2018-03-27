from __future__ import print_function

import time

from ...unused.find_views import get_view_files, get_views, get_url_view_names


def find_unused_views():
    """
    Finds all views in the project. The criteria for an unused view are:
        1. It is not used in any URL.
        2. It is not subclassed by any other view.
    """
    start = time.perf_counter()
    print('Finding all unused views...')
    print(' Getting all view files...')
    view_file_paths = get_view_files()
    print(' Searching for references of each view...', end='')# , flush=True)
    # Get each view
    views = get_views(view_file_paths)
    # Get the names of the views used in URLs
    url_view_names = get_url_view_names()

    # Find each unused view
    unused_views = []
    for view in views:
        print('.', end='')# , flush=True)

        # If a view is not decorated with used_view, not called by a url and is not subclassed, it is unused.
        # Pulling view.__subclasses__() out of the other loop made it find all classes which subclassed view...
        #   probably something to do with namespacing.
        if not hasattr(view, 'is_used') and view.__name__ not in url_view_names and not view.__subclasses__():
            unused_views.append(view)
        # Cover the odd case where the view has is_used == False
        elif hasattr(view, 'is_used') and not view.is_used:
            unused_views.append(view)

    print('\nDone')
    print('\nUnused views:')
    for view in unused_views:
        print(view)
    end = time.perf_counter()
    print('Finished in ' + str(end - start) + ' seconds.')
    return unused_views
