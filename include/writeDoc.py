from pathlib import Path


def unique(a, b):
    result = ''
    for char_a, char_b in zip(a, b):
        if char_a == char_b:
            result += char_a
        else:
            break
    return b[len(result):]


def getBriefFunRef(ref, class_name, file_name=None):
    new_ref = ref.name.split('(')
    ref_name_list = new_ref[0].split()

    if len(new_ref) > 1:
        if len(ref_name_list) > 1:
            ref_type = ' '.join(ref_name_list[:-1])
            if class_name == '':
                ref_name = '[' + ref_name_list[-1] + '](./' + file_name.split('/')[-1].split('.')[0] + '.md#' + ref.name.replace(' ', '_') + ') (' + new_ref[-1]
            else:
                ref_name = '[' + ref_name_list[-1] + '](./' + 'Class_' + class_name.split()[0].replace('::', '_') + '.md#' + ref.name.replace(' ', '_') + ') (' + new_ref[-1]
        else:
            ref_type = ''
            ref_name = '[' + ref_name_list[0] + '](./' + 'Class_' + class_name.split()[0].replace('::', '_') + '.md#' + ref.name.replace(' ', '_') + ') (' + new_ref[-1]
        output = '| ' + ref_type + ' | <p> ' + ref_name + ' </p> <p> ' + ref.brief + ' </p> <img width=1920/> |\n'
        return output
    else:
        return ''


def getBriefRef(ref, class_name):
    ref_name_list = ref.name.split()

    if len(ref_name_list) > 1:
        ref_type = ' '.join(ref_name_list[:-1])
        ref_name = '[' + ref_name_list[-1] + '](./' + 'Class_' + class_name.split()[0].replace('::', '_') + '.md#' + ref.name.replace(' ', '_') + ')'
        output = '| ' + ref_type + ' | <p> ' + ref_name + ' </p> <p> ' + ref.brief + ' </p> <img width=1920/> |\n'
        return output
    else:
        return ''


def getRef(ref):
    output = '| <p id="' + ref.name.replace(' ', '_') + '"><p align="left"> `' + ref.name + '` |\n|-|\n'
    output += '| <p> '
    if ref.brief:
        output += '<p> ' + ref.brief + ' </p>'
    if len(ref.detailed) > 0:
        output += '<p> Detailed description: </p> <ul> <li> ' + ' </li> <li> '.join(ref.detailed) + ' </li> </ul>'
    output += ' </p> <img width=1920/> | \n\n'
    return output


def getFunRef(fun_ref):
    output = '| <p id="' + fun_ref.name.replace(' ', '_') + '"><p align="left"> `' + fun_ref.name + '` |\n|-|\n'
    output += '| <p> '
    if fun_ref.brief:
        output += '<p> ' + fun_ref.brief + ' </p>'
    if len(fun_ref.detailed) > 0:
        output += '<p> <b> Detailed description: </b> </p> <ul> <li> ' + ' </li> <li> '.join(fun_ref.detailed) + ' </li> </ul>'
    if len(fun_ref.params) > 0:
        output += '<p> <b> Parameters: </b> </p> <ul> <li> ' + ' </li> <li> '.join(fun_ref.params) + ' </li> </ul>'
    if fun_ref.returns != '':
        output += '<p> <b> Returns: </b> </p> <ul> <li> ' + fun_ref.returns + ' </li> </ul>'
    output += ' </p> <img width=1920/> | \n\n'
    return output


def getClassRef(class_ref, file_path):
    output = ''
    if class_ref.name != '':
        output += '\n---\n <h4 align="center"> Declared In The Following File: <a href="./' + \
                 file_path.split('/')[-1].split('.')[0] + '.md"> ' + file_path + ' </a></h4> \n'
        output += '\n---\n# ' + class_ref.name + '\n'

    if class_ref.brief:
        output += '### ' + class_ref.brief + '\n'
    if class_ref.detailed:
        output += class_ref.detailed + '\n'

    funcs = [['## Global Function Documentation', class_ref.global_functions]]

    methods = []
    if class_ref.public_methods:
        methods.append(['## Public Member Function Documentation', class_ref.public_methods])
    if class_ref.private_methods:
        methods.append(['## Private Member Function Documentation', class_ref.private_methods])
    if class_ref.protected_methods:
        methods.append(['## Protected Member Function Documentation', class_ref.protected_methods])

    data = []
    if class_ref.public_data_members:
        data.append(['## Public Member Data Documentation', class_ref.public_data_members])
    if class_ref.private_data_members:
        data.append(['## Private Member Data Documentation', class_ref.private_data_members])
    if class_ref.protected_data_members:
        data.append(['## Protected Member Data Documentation', class_ref.protected_data_members])

    # brief:

    for iterator, value in enumerate(funcs):
        brief_list = ['', '']
        if iterator == 0:
            brief_list[0] += '\n---\n'
        brief_list[0] += value[0][:-14] + 's\n\n|||\n|-|-|\n'
        for fun in value[1]:
            br = getBriefFunRef(fun, class_ref.name, file_path)
            if br != '':
                brief_list[1] += br
        if brief_list[1] != '':
            output += ''.join(brief_list) + '\n'

    for iterator, value in enumerate(methods):
        brief_list = ['', '']
        if iterator == 0:
            brief_list[0] += '\n---\n'
        brief_list[0] += value[0][:-14] + 's\n\n|||\n|-|-|\n'
        for fun in value[1]:
            br = getBriefFunRef(fun, class_ref.name)
            if br != '':
                brief_list[1] += br
        if brief_list[1] != '':
            output += ''.join(brief_list) + '\n'

    for iterator, value in enumerate(data):
        brief_list = ['', '']
        if iterator == 0:
            brief_list[0] += '\n'
        brief_list[0] += value[0][:-14] + '\n\n|||\n|-|-|\n'
        for fun in value[1]:
            br = getBriefRef(fun, class_ref.name)
            if br != '':
                brief_list[1] += br
        if brief_list[1] != '':
            output += ''.join(brief_list) + '\n'

    # detailed:

    for iterator, value in enumerate(funcs):
        if iterator == 0:
            output += '\n---\n'
        output += value[0] + '\n\n'
        for fun in value[1]:
            output += getFunRef(fun)

    for iterator, value in enumerate(methods):
        if iterator == 0:
            output += '\n---\n'
        output += value[0] + '\n\n'
        for fun in value[1]:
            output += getFunRef(fun)

    for iterator, value in enumerate(data):
        if iterator == 0:
            output += '\n'
        output += value[0] + '\n\n'
        for val in value[1]:
            output += getRef(val)

    if len(class_ref.type_members) > 0:
        output += '## Member Typedef Documentation:\n\n'
        for val in class_ref.type_members:
            output += getRef(val)
    output += '\nThe documentation for this class was generated using [MdDox](https://github.com/DangeL187/MdDox)\n'
    return output


def writeDocumentation(file_path, documentation, output_file_path):
    menu_file_path = '.'.join(file_path.split('.')[:-1])

    unique_menu_path = unique(output_file_path.replace('\\', '/'), menu_file_path)

    full_menu_file_path = output_file_path.replace('\\', '/') + '/' + unique_menu_path

    if full_menu_file_path.count('.') == 0:
        depth = full_menu_file_path.count('/')
    else:
        depth = full_menu_file_path.count('/') // full_menu_file_path.count('.')

    menu_output = '\n---\n <h4 align="center"> <a href="./' + (file_path.count('/') * '../') + 'Documentation.md"> Project Documentation </a></h4> \n'
    menu_output += '\n---\n <h4 align="center"> <a href="' + '../' * depth + file_path + '"> Go to the source code of this file </a></h4> \n\n---\n# ' + file_path[2:] + ' File Reference\n'

    for i in documentation:
        if i.name != '':
            new_file_path = 'Class_' + i.name.split()[0].replace('::', '_') + '.md'  # create unique name for class file
            menu_output += '* ## [' + i.name.split()[
                0] + '](./' + new_file_path + ')\n'  # add class to the documentation
            Path(full_menu_file_path).mkdir(parents=True, exist_ok=True)  # create new folder
            with open(full_menu_file_path + '/' + new_file_path, 'w') as f:  # create new .md file for class
                f.write(getClassRef(i, file_path).replace('<', '\<'))
        else:
            menu_output += getClassRef(i, file_path)
    Path(full_menu_file_path).mkdir(parents=True, exist_ok=True)  # create new folder
    with open(full_menu_file_path + '/' + menu_file_path.split('/')[-1] + '.md', 'w') as f:  # create new .md file for file
        f.write(menu_output.replace('<', '\<'))
    return unique_menu_path + '/' + menu_file_path.split('/')[-1]
