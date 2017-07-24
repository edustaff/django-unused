import fileinput, time
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
    print('  Searching through templates for references', end="", flush=True)
    for index, template in enumerate(templates):
        print('.', end="", flush=True)
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
