import re  # Подключаем модуль для работы с регулярными выражениями
from collections import defaultdict  # Подключаем defaultdict, чтобы удобно работать с подсчётом

# Функция для парсинга строки из лога
def parse_log_line(line):
    # Определяем шаблон для IP-адреса (4 группы чисел, разделенные точками)
    ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

    # Шаблон для определения операционной системы в User-Agent (находится в круглых скобках)
    os_pattern = r'\(([^;]+);'

    # Ищем IP-адрес в строке
    ip_match = re.search(ip_pattern, line)
    
    # Ищем операционную систему в строке
    os_match = re.search(os_pattern, line)

    # Если нашли IP, то сохраняем его
    ip = ip_match.group(0) if ip_match else None
    
    # Если нашли ОС, то сохраняем её, если нет — записываем 'ОС Неизвестна'
    os = os_match.group(1).strip() if os_match else 'ОС Неизвестна'

    return ip, os  # Возвращаем найденные IP и ОС

# Функция для обработки лог-файла
def process_log(filename):
    # Используем defaultdict для хранения статистики по IP и ОС
    stats = defaultdict(lambda: defaultdict(int))

    # Открываем файл для чтения контентынм менеджером with
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:  # Читаем файл построчно
            ip, os = parse_log_line(line)  # Парсим строку

            if ip:  # Если IP-адрес найден
                stats[ip][os] += 1  # Увеличиваем счётчик для IP и ОС

    return stats  # Возвращаем статистику

# Функция для записи статистики в файл
def write_statistics(stats, output_filename):
    # Открываем файл для записи
    with open(output_filename, 'w', encoding='utf-8') as f:
        for ip, os_dict in stats.items():  # Проходимся по каждому IP
            for os, count in os_dict.items():  # Проходимся по каждой ОС для IP
                f.write(f'{ip}: {os}: {count}\n')  # Записываем в файл

# Основной блок программы
if __name__ == '__main__':
    log_filename = 'nginx.log'  # Имя лог-файла, который нужно обработать
    output_filename = 'log_stat.txt'  # Имя файла, куда запишем результаты

    stats = process_log(log_filename)  # Обрабатываем лог-файл
    write_statistics(stats, output_filename)  # Записываем статистику
