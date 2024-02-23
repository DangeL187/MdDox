class Reference:
    def __init__(self):
        self.name = ''
        self.brief = ''
        self.detailed = ''


class ClassReference(Reference):
    def __init__(self):
        super().__init__()
        self.global_functions = []

        self.public_methods = []
        self.private_methods = []
        self.protected_methods = []

        self.public_data_members = []
        self.private_data_members = []
        self.protected_data_members = []

        self.type_members = []


class FunctionReference(Reference):
    def __init__(self):
        super().__init__()
        self.params = []
        self.returns = ''


def getAccessSpecifier(parsed_values, types, element):
    for value in parsed_values:
        if value[1] in types and value[2] == element:
            return value[0]
    return False


def getAccessSpecifiers(file_path, parsed_file, types, element):
    s = element.split('::')

    if len(s) == 1:
        return getAccessSpecifier(parsed_file[file_path], types, element)

    for i in range(len(s) - 1):
        _ = getAccessSpecifier(parsed_file['::'.join(s[:-1])], types, element)
        if _ is not False:
            return _
    return False


def generateReferences(file_path, parsed_file, parsed_comments):
    class_references = []
    global_function_references = []
    function_references = [[], [], []]
    data_references = [[], [], []]
    type_references = []

    class_ref = ClassReference()
    global_ref = ClassReference()

    for item in parsed_comments:
        for key in item:
            if (key == '@class' or key == '@struct') and getAccessSpecifiers(file_path, parsed_file, ['class', 'structure'], item[key]) is not False:
                if class_ref.name != '':
                    class_ref.public_methods = function_references[0]
                    class_ref.private_methods = function_references[1]
                    class_ref.protected_methods = function_references[2]
                    class_ref.public_data_members = data_references[0]
                    class_ref.private_data_members = data_references[1]
                    class_ref.protected_data_members = data_references[2]
                    class_ref.type_members = type_references
                    class_references.append(class_ref)
                    function_references = [[], [], []]
                    data_references = [[], [], []]
                    type_references = []
                class_ref = ClassReference()
                class_ref.name = item[key] + ' Class Reference'
                if '@brief' in item:
                    class_ref.brief = item['@brief']
                if '@det' in item:
                    class_ref.detailed = item['@det'].split('\n')
            elif key == '@fn':
                full_fun_name = item[key].split('(')[0].split()[-1]
                access_spec = getAccessSpecifiers(file_path, parsed_file, ['method', 'constructor', 'destructor'], full_fun_name)
                if access_spec is not False:
                    fun_ref = FunctionReference()
                    fun_ref.name = item[key]
                    if '@brief' in item:
                        fun_ref.brief = item['@brief']
                    if '@param' in item:
                        fun_ref.params = item['@param'].split('\n')
                        for i in range(len(fun_ref.params)):
                            new_i = fun_ref.params[i].split()
                            if len(new_i) > 1:
                                fun_ref.params[i] = '<b> ' + new_i[0] + ' </b> ' + ' '.join(new_i[1:])
                            else:
                                fun_ref.params[i] = '<b> ' + fun_ref.params[i] + ' </b>'
                    if '@return' in item:
                        fun_ref.returns = item['@return']
                    if '@det' in item:
                        fun_ref.detailed = item['@det'].split('\n')
                    if access_spec == 'PRIVATE':
                        function_references[1].append(fun_ref)
                    elif access_spec == 'PROTECTED':
                        function_references[2].append(fun_ref)
                    else:
                        function_references[0].append(fun_ref)
                # if global function:
                access_spec = getAccessSpecifiers(file_path, parsed_file, ['function'], full_fun_name)
                if access_spec is not False:
                    fun_ref = FunctionReference()
                    fun_ref.name = item[key]
                    if '@brief' in item:
                        fun_ref.brief = item['@brief']
                    if '@param' in item:
                        fun_ref.params = item['@param'].split('\n')
                        for i in range(len(fun_ref.params)):
                            new_i = fun_ref.params[i].split()
                            if len(new_i) > 1:
                                fun_ref.params[i] = '<b> ' + new_i[0] + ' </b> ' + ' '.join(new_i[1:])
                            else:
                                fun_ref.params[i] = '<b> ' + fun_ref.params[i] + ' </b>'
                    if '@return' in item:
                        fun_ref.returns = item['@return']
                    if '@det' in item:
                        fun_ref.detailed = item['@det'].split('\n')
                    global_function_references.append(fun_ref)
            elif key == '@var':
                full_var_name = item[key].split()[-1]
                access_spec = getAccessSpecifiers(file_path, parsed_file, ['variable', 'field'], full_var_name)
                if access_spec is not False:
                    var_ref = Reference()
                    var_ref.name = item[key]
                    if '@brief' in item:
                        var_ref.brief = item['@brief']
                    if '@det' in item:
                        var_ref.detailed = item['@det'].split('\n')
                    if access_spec == 'PRIVATE':
                        data_references[1].append(var_ref)
                    elif access_spec == 'PROTECTED':
                        data_references[2].append(var_ref)
                    else:
                        data_references[0].append(var_ref)
            elif key == '@typedef':
                full_type_name = item[key].split()[-1]
                access_spec = getAccessSpecifiers(file_path, parsed_file, ['typedef'], full_type_name)
                if access_spec is not False:
                    type_ref = Reference()
                    type_ref.name = item[key]
                    if '@brief' in item:
                        type_ref.brief = item['@brief']
                    if '@det' in item:
                        type_ref.detailed = item['@det'].split('\n')
                    type_references.append(type_ref)
    if class_ref.name != '':
        class_ref.public_methods = function_references[0]
        class_ref.private_methods = function_references[1]
        class_ref.protected_methods = function_references[2]
        class_ref.public_data_members = data_references[0]
        class_ref.private_data_members = data_references[1]
        class_ref.protected_data_members = data_references[2]
        class_ref.type_members = type_references
        class_references.append(class_ref)
    if global_function_references:
        global_ref.global_functions = global_function_references
        class_references.append(global_ref)
    return class_references
