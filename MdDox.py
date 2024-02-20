import sys
import glob
import os
from include.parseFile import *
from include.comments import *
from include.genRef import *
from include.writeDoc import *


def genDoc(file_path, output_file_path):
    file = None
    comments = None
    documentation = None

    try:
        file = parseFile(file_path)
    except:
        print('No such file: ', file_path)
        return ''
    try:
        comments = parseComments(file_path)
        addEmptyComments(file, comments)
    except:
        print('Failed to parse comments for: ', file_path)
        return ''
    try:
        documentation = generateReferences(file_path, file, comments)
    except:
        print('Failed to generate references for:', file_path)
        return ''
    try:
        ret = writeDocumentation(file_path, documentation, output_file_path)
        print('Documentation was successfully generated for:', file_path)
        return ret
    except:
        print('Failed to write documentation for:', file_path)
        return ''


if __name__ == "__main__":
    extensions = ['hpp', 'cpp', 'c', 'h']
    project_name = 'Project'
    input_dir = '.'
    output_dir = 'docs'
    if len(sys.argv) == 2:
        project_name = sys.argv[1]
    elif len(sys.argv) == 3:
        project_name = sys.argv[1]
        output_dir = sys.argv[2]
    elif len(sys.argv) != 1:
        print('Usage: MdDox.py [PROJECT_NAME] [OUTPUT_DIR]')
        exit(1)

    output_dir = input_dir + '/' + output_dir

    output_doc = '\n---\n<h1 align="center"> Documentation of ' + project_name + '</h1>\n\n---\n## File List\n\n| <img width=1920 />|\n|-|\n'

    for ext in extensions:
        for file_name in glob.iglob(os.path.join(input_dir, '**', '*.' + ext), recursive=True):
            doc_file_name = genDoc(file_name.replace('\\', '/'), output_dir)

            if doc_file_name != '':
                output_doc += '| [' + file_name.replace('\\', '/')[2:] + '](' + doc_file_name + '.md)|\n'

    with open(output_dir + '/Documentation.md', 'w') as ff:
        ff.write(output_doc)


# Does NOT support classes inside other classes yet!
