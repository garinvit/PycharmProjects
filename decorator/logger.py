import datetime


def logger(func):
    def new_function(*args, **kwargs):
        old_function = func(*args, **kwargs)
        log_line = f'{datetime.datetime.now()} функция: {func.__name__}; аргументы: {str(args)}, {str(kwargs)}; вернула результат:{str(old_function)}.\n'
        with open(f'log_{datetime.datetime.today().strftime("%d_%m_%Y")}.txt', 'a') as log_file:
            log_file.write(log_line)
        return old_function
    return new_function


def param_logger(path, echo=False, mode='a'):
    def decorator(func):
        def new_function(*args, **kwargs):
            old_function = func(*args, **kwargs)
            log_line = f'{datetime.datetime.now()} функция: {func.__name__}; аргументы: {str(args)}, {str(kwargs)}; вернула результат:{str(old_function)}.\n'
            with open(path,  mode) as log_file:
                log_file.write(log_line)
            if echo:
                print(log_line)
            return old_function
        return new_function
    return decorator


@param_logger('log.txt')
def adv_print(*args, **kwargs):
    start = '\n'
    result = ''
    sep = ' '
    end = '\n'
    in_file = False
    max_line = 300
    for key in kwargs.keys():
        if key == 'start':
            start = kwargs[key]
        elif key == 'max_line':
            max_line = kwargs[key]+1
        elif key == 'in_file':
            in_file = True
        elif key == 'sep':
            sep = kwargs[key]
        elif key == 'end':
            end = kwargs[key]
    result = sep.join([str(x) for x in args])
    if len(result) > max_line:
        for i in range(0, int(len(result)+int(len(result)/(max_line-1))), max_line):
            result = result[:i] + '\n' + result[i:]
    result = start + result + end
    if in_file:
        with open('print_out.txt', 'w') as out:
            out.write(result)
    print(result)


@logger
def test_f(*args, **kwargs):
    return args, kwargs


@param_logger('log.txt', echo=True)
def test_2(*args, **kwargs):
    return args, kwargs


@param_logger('log.txt')
def main():
    test_f(1, 'a', 3, test='word', abc=123)
    test_2(1, 'a', 3, test='word', abc=123)
    adv_print(1, '+', 2, '=', 3, start='Пример:\n', end='\nКонец.')


if __name__ == '__main__':
    main()
    ‘good’ if 2 > 1 else ‘bad’: