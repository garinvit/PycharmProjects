from mystack import Stack


def brackets(str_brackets):
    stack_of_brackets = Stack()
    bkt_dict = {'(': ')', '[': ']', '{': '}', ')': '(', ']': '[', '}': '{'}
    for bkt in str_brackets:
        if bkt_dict[bkt] == stack_of_brackets.peek():
            stack_of_brackets.pop()
        else:
            stack_of_brackets.push(bkt)
    if stack_of_brackets.isEmpty():
        print('Сбалансировано')
    else:
        print('Несбалансировано')


test_cases =['(((([{}]))))',
    '[([])((([[[]]])))]{()}',
    '{{[()]}}',
    '}{}',
    '{{[(])]}}',
    '[[{())}]]', ]


if __name__ == '__main__':
    for test in test_cases:
        brackets(test)
