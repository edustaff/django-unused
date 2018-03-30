from __future__ import print_function

import fileinput
import time

import six

if six.PY2:
    # No tempfile in PY2
    from backports import tempfile
    TemporaryDirectory = tempfile.TemporaryDirectory

    time.perf_counter = time.clock
else:
    from tempfile import TemporaryDirectory

from whoosh.analysis import RegexTokenizer
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in
from whoosh.qparser import QueryParser
from whoosh.util.text import rcompile

from ...unused.find_templates import find_py_files, find_app_templates, find_global_templates


def find_unused_templates():
    start = time.perf_counter()
    print('Finding all unused templates...')
    print('  Getting global templates...')
    global_templates_files, global_templates = find_global_templates()
    print('   Done.\n  Getting app templates...')
    app_templates_files, app_templates = find_app_templates()
    print('   Done.')
    templates = global_templates + app_templates
    template_files = global_templates_files + app_templates_files
    # templates.sort()
    template_files.sort()

    print('  Getting python files...')
    py_files, pys = find_py_files()
    print('   Done.')
    all_files = py_files + template_files

    tl_count = [0 for t in templates]
    unused_templates = []

    print('  Creating Index', end='')
    tmp_dir = TemporaryDirectory()

    schema = Schema(title=TEXT(stored=True),
                    path=ID(stored=True),
                    content=TEXT(analyzer=RegexTokenizer(expression=rcompile(r"[\w/.]+"))))
    ix = create_in(tmp_dir.name, schema)
    writer = ix.writer()

    for filename in all_files:
        print('.', end='')  # , flush=True)
        with open(filename, 'r') as f:
            # print('WHOOSH', filename, filename, f)
            # content = '/n'.join(f.readlines())
            # if content:
            #     print('HAS CONTENT')
            #     print(content)
            u_filename = filename
            try:  # Python2
                u_filename = unicode(filename)
            except NameError:
                pass
            writer.add_document(title=u_filename, path=u_filename,
                                content=six.u('/n'.join(f.readlines())))
                                # content=content)
    print('')  # , flush=True)
    writer.commit()
    print('   Done.')

    print('  Searching through templates for references', end='')  # , flush=True)
    with ix.searcher() as searcher:
        for count, template in enumerate(templates):
            print('.', end="")  # , flush=True)
            query = QueryParser("content", ix.schema).parse(template)
            results = searcher.search(query)
            if len(results) < 1:
                unused_templates.append(template)
    print('')  # , flush=True)
    print('   Done.')

    if not unused_templates:
        print('No unused templates found.')
    else:
        print('\nUnused templates:')
        for template in unused_templates:
            print(template)
    end = time.perf_counter()
    print('Finished in ' + str(end - start) + ' seconds.')
    return unused_templates


def find_unused_templates_whoosh():
    """
    Finds all templates in the project. The criteria for an unused view are:
        1. It is not used other template.
        2. It is not reference in any python file.
    """
    start = time.perf_counter()
    print('Finding all unused templates...')
    print('  Getting global templates...')
    global_templates_files, global_templates = find_global_templates()
    print('   Done.\n  Getting app templates...')
    app_templates_files, app_templates = find_app_templates()
    print('   Done.')
    templates = global_templates + app_templates
    template_files = global_templates_files + app_templates_files
    # templates.sort()
    template_files.sort()

    print('  Getting python files...')
    py_files, pys = find_py_files()
    print('   Done.')
    all_files = py_files + template_files

    tl_count = [0 for t in templates]
    unused_templates = []
    print('  Searching through templates for references', end="")  # , flush=True)
    for index, template in enumerate(templates):
        print('.', end="")  # , flush=True)
        for line in fileinput.input(all_files):  # Loops through every line of every file
            # print([template, line])
            if str.find(line, template) > -1:
                # print(['FOUND', template, line])
                tl_count[index] += 1
                break
        fileinput.close()

        if tl_count[index] == 0:
            unused_templates.append(template)
            # print(template)
            # else:
            #     print(['FOUND', tl_count[index], template])
    # print(os.linesep.join(unused_templates))
    print('\nDone.')

    if not unused_templates:
        print('No unused templates found.')
    else:
        print('\nUnused templates:')
        for template in unused_templates:
            print(template)
    end = time.perf_counter()
    print('Finished in ' + str(end - start) + ' seconds.')
    return unused_templates
