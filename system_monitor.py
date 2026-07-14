import psutil
import time
import GPUtil

def main():
    try:
        while True:
            # Очищаем экран
            print("\033c", end="")
            print("=== МОНИТОР СИСТЕМЫ ===\n")

            # CPU
            cpu = psutil.cpu_percent(interval=1)
            if cpu > 80:
                print(f"⚠️ CPU: {cpu}% (ВЫСОКАЯ НАГРУЗКА)")
            else:
                print(f"CPU: {cpu}%")

            # Память
            mem = psutil.virtual_memory()
            mem_total_gb = mem.total / 1024**3
            mem_used_gb = mem.used / 1024**3
            if mem.percent > 80:
                print(f"⚠️ Память: всего {mem_total_gb:.2f} ГБ, использовано {mem_used_gb:.2f} ГБ ({mem.percent}%)")
            else:
                print(f"Память: всего {mem_total_gb:.2f} ГБ, использовано {mem_used_gb:.2f} ГБ ({mem.percent}%)")

            # Диск
            disk = psutil.disk_usage('/')
            disk_total_gb = disk.total / 1024**3
            disk_used_gb = disk.used / 1024**3
            if disk.percent > 90:
                print(f"⚠️ Диск /: всего {disk_total_gb:.2f} ГБ, использовано {disk_used_gb:.2f} ГБ ({disk.percent}%)")
            else:
                print(f"Диск /: всего {disk_total_gb:.2f} ГБ, использовано {disk_used_gb:.2f} ГБ ({disk.percent}%)")

            # GPU (если есть)
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    for i, gpu in enumerate(gpus):
                        print(f"\nGPU {i}: {gpu.name}")
                        print(f"  Загрузка: {gpu.load * 100:.1f}%")
                        print(f"  Память: {gpu.memoryUsed:.0f} / {gpu.memoryTotal:.0f} МБ ({gpu.memoryUtil * 100:.1f}%)")
                        print(f"  Температура: {gpu.temperature}°C")
                else:
                    print("\nGPU не найдены")
            except Exception as e:
                print(f"\nОшибка при получении данных GPU: {e}")

            print("\nНажми Ctrl+C для выхода")
            time.sleep(9)

    except KeyboardInterrupt:
        print("\nМониторинг остановлен.")

if __name__ == "__main__":
    main()
