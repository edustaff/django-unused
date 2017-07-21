from ...unused.find_views import get_view_files


def find_unused_views():
    print('Finding all unused views...')
    print('Getting all view files...')
    view_files, view_file_paths = get_view_files()
    print(view_files)
    print(view_file_paths)
    print('Done.')

    print('Searching for references...')
    print('Done')

