import language_check

tool = language_check.LanguageTool('en-US')


def check_capital(data):
    word_list = data.split(' ')
    error_list = []
    for word in word_list[1:]:
        if (not word.islower()) and (not word.isupper()):
            error_list.append('Capitalization error: {}'.format(word))
    return error_list


def check_space(data):
    error_list = []
    if '){' in data:
        error_list.append('Space error: {}'.format('){'))

    for i in range(len(data)):

        if data[i] in ['=', '+']:
            if data[i-1] != ' ' or data[i+1] != ' ':
                error_list.append('Space error: {}'.format(data[i-1: i+2]))

        if data[i] == ',':
            if data[i+1] != ' ' and data[i+1] != '\\':
                error_list.append('Space error: {}'.format(data[i-1: i+1]))

    return error_list


def check_comment(data):
    error_list = []
    if 'tslint' in data:
        error_list.append('Comment error: {}'.format('tslint'))

    return error_list


line_num = 0
with open('test_code.txt', 'r') as fin:

    for line in fin:
        print('\x1b[1;33;50mCode Line #{}: {}\x1b[0m'.format(line_num, line.replace('\n', '')))

        if line == '\n':
            print('              ^^^^ Error: Empty line!')

        start_quote = None
        end_quote = None

        find_start = False
        find_end = False

        for space_mistake in check_space(line):
            print(space_mistake)

        for comment_mistake in check_comment(line):
            print(comment_mistake)

        for i in range(len(line)):
            if line[i] == "'":
                if not find_start:
                    start_quote = i
                    find_start = True
                elif find_start:
                    end_quote = i
                    find_end = True

            if find_start and find_end:
                sen = (line[start_quote + 1: end_quote])
                sen += '.'
                for mistake in tool.check(sen):
                    print(mistake)

                for cap_mistake in check_capital(sen):
                    print(cap_mistake)

                find_start = False
                find_end = False

        line_num += 1
