# coding: utf-8
"""
    Модуль для работы с процессами
"""
import os
import signal

class CreatePIDFileException(Exception): pass


def check_running(process_id):
    """
        Проверяет запущен ли в системе процесс с указанным идентификатором
    """
    try:
        process_id = int(process_id)
        os.kill(process_id, signal.SIG_DFL)
        return True
    except OSError:
        return False

def create_file(path):
    """
        Создает pid-файл для текущего процесса.
        Если pid-файл уже существет и в системе запущен процесс с таким id, генерируется исключение
    """
    current_pid = str(os.getpid())

    # проверим нет ли уже pid-файла
    if os.path.isfile(path):
        lines = file(path, 'r').readlines()
        if lines:
            exist_pid = lines[0]
            if check_running(exist_pid):
                raise CreatePIDFileException('Process with id %s (%s) still work in system' % (exist_pid, path))

    pid_file = file(path, 'w')
    pid_file.write(current_pid)
    pid_file.close()