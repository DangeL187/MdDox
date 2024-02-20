import clang.cindex
from clang.cindex import CursorKind

clang.cindex.Config.set_library_file('D:\\LLVM\\bin\\libclang.dll')

decl_types = {CursorKind.STRUCT_DECL: 'structure', CursorKind.TYPEDEF_DECL: 'typedef', CursorKind.CLASS_DECL: 'class',
              CursorKind.FUNCTION_DECL: 'function', CursorKind.VAR_DECL: 'variable',
              CursorKind.CONSTRUCTOR: 'constructor', CursorKind.DESTRUCTOR: 'destructor'}


def dictAppend(dictionary, key, value):
    if key in dictionary:
        dictionary[key].append(value)
    else:
        dictionary[key] = [value]


def getGeneratedTree(file_path, cursor, parent=None, output=None, full_name=None):
    if output is None:
        output = dict()
    if full_name is None:
        full_name = []

    full_name.append(cursor.spelling)

    if len(full_name) < 3:
        full_name_ = '::'.join(full_name[:-1])
    else:
        full_name_ = '::'.join(full_name[1:-1])

    if cursor.kind == CursorKind.CXX_METHOD:
        dictAppend(output, full_name_,
                   [str(cursor.access_specifier).split('.')[1], 'method', '::'.join(full_name[1:])])
    elif cursor.kind == CursorKind.FIELD_DECL:
        dictAppend(output, full_name_,
                   [str(cursor.access_specifier).split('.')[1], 'field', '::'.join(full_name[1:])])
    elif cursor.kind in decl_types and parent.spelling != '':
        dictAppend(output, full_name_, [None, decl_types[cursor.kind], '::'.join(full_name[1:])])

    for child in cursor.get_children():
        if str(child.location.file) == str(file_path):
            output = getGeneratedTree(file_path, child, cursor, output, full_name)
            if len(full_name) > 0:
                full_name.pop(-1)
    return output


def parseFile(file_path):
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_path)
    root_cursor = translation_unit.cursor

    return getGeneratedTree(file_path, root_cursor)
