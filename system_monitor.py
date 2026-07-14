#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# system_monitor.py
# Мониторинг системы с цветным выводом, сохранением отчёта и графиком CPU.

import psutil
import time
import argparse
from colorama import init, Fore, Style

init(autoreset=True)

def get_cpu_graph(percent):
    bar_len = 30
    filled = int(bar_len * percent / 100)
    bar = '█' * filled + '░' * (bar_len - filled)
    return bar

def main():
    parser = argparse.ArgumentParser(description="мониторинг системы")
    parser.add_argument("-o", "--output", help="сохранить отчёт в файл")
    parser.add_argument("-n", "--count", type=int, default=5, help="количество итераций")
    parser.add_argument("--interval", type=float, default=1.0, help="интервал между замерами")
    args = parser.parse_args()

    for i in range(args.count):
        cpu = psutil.cpu_percent(interval=args.interval, percpu=True)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        load = psutil.getloadavg()

        avg_cpu = sum(cpu) / len(cpu)

        # цветной вывод
        if avg_cpu < 30:
            cpu_color = Fore.GREEN
        elif avg_cpu < 70:
            cpu_color = Fore.YELLOW
        else:
            cpu_color = Fore.RED

        mem_color = Fore.GREEN if mem.percent < 50 else Fore.YELLOW if mem.percent < 80 else Fore.RED

        print(f"{Fore.CYAN}=== Замер {i+1} ==={Style.RESET_ALL}")
        print(f"CPU: {cpu_color}{avg_cpu:.1f}%{Style.RESET_ALL}")
        for core, val in enumerate(cpu):
            print(f"  Ядро {core}: {get_cpu_graph(val)} {val:.1f}%")
        print(f"Память: {mem_color}{mem.percent}%{Style.RESET_ALL} ({mem.used/1024**3:.1f} ГБ из {mem.total/1024**3:.1f} ГБ)")
        print(f"Диск: {disk.percent}% ({disk.used/1024**3:.1f} ГБ из {disk.total/1024**3:.1f} ГБ)")
        print(f"Нагрузка: {load[0]:.2f} {load[1]:.2f} {load[2]:.2f}")

        # сохранение в файл
        if args.output:
            with open(args.output, 'a') as f:
                f.write(f"{time.ctime()}: CPU={avg_cpu:.1f}%, MEM={mem.percent}%, DISK={disk.percent}%\n")

        time.sleep(1)

    print(f"{Fore.GREEN}Готово.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
