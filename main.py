import subprocess
import datetime
import os

def run_command(command):
    """Запуск linux команд и возврат их результата"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result
    except Exception as e:
        return f'Ошибка {e}'


def main():
    """Основная функция сбора информации"""
    print("🔍 Запуск сбора информации о системе...")

    # 1. Отчёт с текущей датой
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = []
    report.append('=' * 50)
    report.append(f'ОТЧЕТ О СИСТЕМЕ | {current_time}')
    report.append('=' * 50)

    # 2. Базовая информация о системе
    report.append('\n📋 БАЗОВАЯ ИНФОРМАЦИЯ:')
    report.append('-' * 30)
    # Имя пользователя
    report.append(f'Пользователь: {run_command('whoiam')}')
    # Местоположение пользователя
    report.append(f'Текущая папка: {run_command('pwd')}')
    # Информация о системе
    report.append(f'Имя хоста: {run_command('hostname')}')
    report.append(f'Версия ядра: {run_command('uname -r')}')
    report.append(f'Вся информация о системе: {run_command('uname -a')}')

    # 3. Информация о ресурсах
    report.append("\n💾 ИСПОЛЬЗОВАНИЕ РЕСУРСОВ:")
    report.append("-" * 30)

    # Память
    report.append("Оперативная память:")
    report.append(str(run_command("free -h")))

    # Дисковое пространство
    report.append("\nДисковое пространство:")
    report.append(str(run_command("df -h | grep -E '^(Filesystem|/dev/)'")))

    # Загрузка процессора
    report.append("\nЗагрузка процессора:")
    report.append(str(run_command('uptime')))

    # 4. Сетевые интерфейсы
    report.append("\n🌐 СЕТЕВЫЕ ИНТЕРФЕЙСЫ:")
    report.append("-" * 30)
    report.append(str(run_command("ip addr show | grep 'inet ' | grep -v '127.0.0.1'")))

    # 5. Активные процессы (топ-5 по памяти)
    report.append("\n🔥 ТОП-5 ПРОЦЕССОВ ПО ПАМЯТИ:")
    report.append("-" * 30)
    top_mem = run_command('ps aux --sort=-%mem | head -6')
    report.append(str(top_mem))


    file_name = f'system_report_{datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S")}.txt'
    with open(file=file_name, mode='w', encoding='utf-8') as f:
        f.write('\n'.join(report))

    print(f"\n✅ Отчёт сохранён в файл: {file_name}")
    print(f"\n📊 Краткая сводка:")
    print(f"   Пользователь: {run_command('whoami')}")
    print(f"   Система: {run_command('uname -s')} {run_command('uname -r')}")
    print(f"   Память свободно: {run_command('free -h | grep Mem | awk "{print $4}"')}")
    print(f"   Диск свободно: {run_command('df -h / | tail -1 | awk "{print $4}"')}")

    print(f"\n📁 Полный отчёт здесь: {os.path.abspath(file_name)}")

if __name__ == "__main__":
    main()


