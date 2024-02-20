def parseComments(file_path):
    output = []
    current_block = dict()
    is_block = False
    is_same_attr = False
    attribute = ''
    with open(file_path) as f:
        lines = f.read().split('\n')
        for line in lines:
            for word in line.split():
                if word == '*/':
                    is_block = False
                    attribute = ''
                    output.append(current_block)
                    current_block = dict()
                if is_block and word in ['@file', '@class', '@struct', '@brief', '@fn', '@param', '@return', '@det', '@var', '@typedef']:
                    attribute = word
                    if attribute in current_block:
                        is_same_attr = True
                elif word == '/*!':
                    is_block = True
                elif attribute != '':
                    prefix = ' '
                    if is_same_attr:
                        prefix = '\n'
                        is_same_attr = False
                    if current_block.get(attribute):
                        current_block[attribute] += prefix + word
                    else:
                        current_block[attribute] = word
    return output


def addEmptyComments(parsed_file, parsed_comments):
    name_types = ['@class', '@struct', '@typedef', '@fn', '@var']
    converter = {'structure': '@struct', 'typedef': '@typedef', 'class': '@class', 'function': '@fn',
                 'constructor': '@fn', 'destructor': '@fn', 'method': '@fn', 'field': '@var', 'variable': '@var'}
    commented_declarations = []
    classes = {}
    additional_index = 0

    for index, block in enumerate(parsed_comments):
        for key in block:
            if key in name_types:
                if key in ['@class', '@struct']:
                    classes[block[key]] = index+1

                if key == '@fn':
                    commented_declarations.append(block[key].split('(')[0].split()[-1])
                elif key == '@var':
                    commented_declarations.append(block[key].split()[-1])
                else:
                    commented_declarations.append(block[key])
                break

    for value in parsed_file.values():
        for declaration in value:
            if declaration[2] not in commented_declarations:
                if '::' not in declaration[2]:
                    parsed_comments.insert(0, {converter[declaration[1]]: declaration[2], '@brief': '-'})
                    additional_index += 1
                else:
                    decl = '::'.join(declaration[2].split('::')[:-1])
                    if decl in classes:
                        parsed_comments.insert(classes[decl] + additional_index, {converter[declaration[1]]: declaration[2], '@brief': '-'})
                        additional_index += 1
                    else:
                        parsed_comments.insert(0, {converter[declaration[1]]: declaration[2], '@brief': '-'})
                        additional_index += 1
