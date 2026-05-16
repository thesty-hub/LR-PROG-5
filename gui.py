import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess   
import threading
import os
import time

class SimpleSortApp:
    def __init__(self, root):                                 # Конструктор класса, вызывается при создании объекта
        self.root = root                                      # Сохранение ссылки на главное окно
        self.root.title("Сортировка данных автопарка")        # Установка заголовка окна
        self.root.geometry("1000x750")                        # Установка размера окна
        
        self.file_path = None                                 # Переменная для пути к CSV файлу
        self.key_var = tk.StringVar(value="id")               # Переменная для выбранного ключа сортировки
        self.impl_var = tk.StringVar(value="Python")          # Переменная для выбранной реализации
        self.order_var = tk.StringVar(value="asc")            # Переменная для порядка
        self.lines_count_var = tk.StringVar(value="20")       # Переменная для количества строк для просмотра
        self.start_line_var = tk.StringVar(value="1")         # Переменная для начальной строки диапазона
        self.end_line_var = tk.StringVar(value="20")          # Переменная для конечной строки диапазона
        
        self.create_widgets()                                 # Вызов метода создания интерфейса
    
    def create_widgets(self):                                 # Функция создания всех элементов интерфейса
        # Секция выбора или генерации файла
        tk.Label(self.root, text="CSV файл:", font=('Arial', 10, 'bold')).pack(pady=5)
        self.file_label = tk.Label(self.root, text="Не выбран", bg='lightgray', relief='sunken')
        self.file_label.pack(fill='x', padx=20, pady=5)       # Размещение метки с растяжением по горизонтали
        
        btn_frame = tk.Frame(self.root)                       # Рамка для кнопок выбора/генерации
        btn_frame.pack(pady=5)                                # Размещение рамки с отступом
        tk.Button(btn_frame, text="Выбрать файл", command=self.select_file, font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Сгенерировать файл (>1 ГБ)", command=self.generate_file, font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        # == НОВАЯ СЕКЦИЯ: ВЫБОР ПОРЯДКА СОРТИРОВКИ
        order_frame = tk.Frame(self.root)                     # Рамка для выбора порядка сортировки
        order_frame.pack(pady=5)                              # Размещение рамки
        tk.Label(order_frame, text="Порядок сортировки:", font=('Arial', 10, 'bold')).pack(side='left', padx=5)  # Метка
        tk.Radiobutton(order_frame, text="По возрастанию", variable=self.order_var, value="asc", font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Radiobutton(order_frame, text="По убыванию", variable=self.order_var, value="desc", font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        tk.Label(self.root, text="Ключ сортировки:", font=('Arial', 10, 'bold')).pack(pady=5)
        keys_frame = tk.Frame(self.root)                     
        keys_frame.pack()
        for key in ['id', 'brand', 'model', 'price', 'horsepower', 'stock', 'vehicle_type']:  # Перебор всех полей
            tk.Radiobutton(keys_frame, text=key, variable=self.key_var, value=key, font=('Arial', 10, 'bold')).pack(side='left', padx=5)  # Создание радиокнопки для каждого поля
        
        tk.Label(self.root, text="Реализация:", font=('Arial', 10, 'bold')).pack(pady=5)
        impl_frame = tk.Frame(self.root)                      # Рамка для радиокнопок выбора реализации
        impl_frame.pack()                                     # Размещение рамки
        tk.Radiobutton(impl_frame, text="Python", variable=self.impl_var, value="Python", font=('Arial', 10, 'bold')).pack(side='left', padx=10)  # Радиокнопка выбора Python
        tk.Radiobutton(impl_frame, text="C++", variable=self.impl_var, value="C++", font=('Arial', 10, 'bold')).pack(side='left', padx=10)  # Радиокнопка выбора C++
        
        self.sort_btn = tk.Button(self.root, text="ЗАПУСТИТЬ СОРТИРОВКУ", command=self.run_sort, bg='green', fg='white', font=('Arial', 12, 'bold'))
        self.sort_btn.pack(pady=10)
        
        view_frame = tk.LabelFrame(self.root, text="Просмотр результата", font=('Arial', 10, 'bold'))
        view_frame.pack(fill='x', padx=10, pady=5)
        
        # Блок для отсортированного файла
        sorted_frame = tk.Frame(view_frame)      # Рамка для отсортированного файла
        sorted_frame.pack(pady=5, fill='x')      # Размещение рамки
        
        tk.Label(sorted_frame, text="Отсортированный файл:", font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        lines_frame = tk.Frame(sorted_frame)                  # Рамка для настройки количества строк
        lines_frame.pack(side='left', padx=20)                # Размещение рамки слева
        tk.Label(lines_frame, text="Показать строк:", font=('Arial', 10)).pack(side='left', padx=5) 
        tk.Entry(lines_frame, textvariable=self.lines_count_var, width=8, font=('Arial', 10)).pack(side='left', padx=5)
        
        for count in [20, 50, 100, 500, 1000]:                # Цикл создания кнопок быстрого выбора
            tk.Button(lines_frame, text=str(count), command=lambda c=count: self.lines_count_var.set(str(c)), width=3, font=('Arial', 9, 'bold')).pack(side='left', padx=2)  # Кнопка с числом для быстрой установки
        
        action_frame = tk.Frame(sorted_frame)                 # Рамка для кнопок действий просмотра
        action_frame.pack(side='left', padx=5)                # Размещение рамки слева
        tk.Button(action_frame, text="Показать первые N строк", command=self.show_custom_lines, bg='blue', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)  # Кнопка показа указанного количества строк
        tk.Button(action_frame, text="Весь результат", command=self.show_full_result, bg='purple', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)  # Кнопка показа всего файла
        
        # Блок для исходного файла
        source_frame = tk.Frame(view_frame)                   # Рамка для исходного файла
        source_frame.pack(pady=10, fill='x')                  # Размещение рамки\
        tk.Label(source_frame, text="Исходный файл:", font=('Arial', 10, 'bold')).pack(side='left', padx=5)  # Метка "Исходный файл:"
        
        range_frame = tk.Frame(source_frame)                  # Рамка для ввода диапазона строк
        range_frame.pack(side='left', padx=20)                # Размещение рамки слева
        tk.Label(range_frame, text="Строки с:", font=('Arial', 10)).pack(side='left', padx=2)
        tk.Entry(range_frame, textvariable=self.start_line_var, width=6, font=('Arial', 10)).pack(side='left', padx=2)  # Поле ввода начальной строки
        tk.Label(range_frame, text="по:", font=('Arial', 10)).pack(side='left', padx=2) 
        tk.Entry(range_frame, textvariable=self.end_line_var, width=6, font=('Arial', 10)).pack(side='left', padx=2)  # Поле ввода конечной строки
        
        tk.Button(range_frame, text="Показать диапазон строк", command=self.show_line_range, bg='teal', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=10)  # Кнопка показа диапазона строк
        
        # Секция кнопок управления
        control_frame = tk.Frame(self.root)                   # Рамка для кнопок управления
        control_frame.pack(pady=5)                            # Размещение рамки
        tk.Button(control_frame, text="Очистить лог", command=self.clear_log, bg='orange', font=('Arial', 10, 'bold')).pack(side='left', padx=5)  # Кнопка очистки лога
        tk.Button(control_frame, text="Закрыть программу", command=self.close_program, bg='red', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)  # Кнопка закрытия программы

        # Секция логов
        tk.Label(self.root, text="Лог выполнения:", font=('Arial', 10, 'bold')).pack() 
        self.log = scrolledtext.ScrolledText(self.root, height=16, font=('Courier', 9))  # Текстовое поле с прокруткой для лога
        self.log.pack(fill='both', expand=True, padx=10, pady=5)  # Размещение с растяжением во все стороны
        
        self.status_bar = tk.Label(self.root, text="Готов к работе", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=('Arial', 9))  # Строка состояния внизу окна
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)       # Размещение строки состояния внизу с растяжением
    
    def select_file(self):                                    # Метод выбора CSV файла
        fname = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])  # Открытие диалога выбора файла с фильтром CSV
        if fname:                                             # Если файл выбран
            self.file_path = fname                            # Сохранение пути к файлу
            size = os.path.getsize(fname) / (1024**3)         # Получение размера файла в гигабайтах
            self.file_label.config(text=f"{os.path.basename(fname)} ({size:.2f} ГБ)")  # Отображение имени и размера файла
            self.log_insert(f"Выбран файл: {fname} ({size:.2f} ГБ)")  # Запись в лог информации о выборе
    
    def generate_file(self):                                  # Метод генерации тестового файла
        def gen():                                            # Внутренняя функция для запуска в потоке
            self.log_insert("Генерация файла... (25 млн строк)")  # Запись в лог начала генерации
            self.status_bar.config(text="Генерация файла...")  # Обновление строки состояния
            import generate_csv                               # Импорт модуля генератора (здесь, чтобы избежать циклического импорта)
            generate_csv.generate_csv("data.csv", 25000000)   # Вызов функции генерации файла (25 млн строк)
            self.file_path = os.path.abspath("data.csv")      # Получение абсолютного пути к сгенерированному файлу
            size = os.path.getsize(self.file_path) / (1024**3)  # Получение размера файла в ГБ
            self.file_label.config(text=f"data.csv ({size:.2f} ГБ)")  # Отображение имени и размера
            self.log_insert(f"Генерация завершена! Размер: {size:.2f} ГБ")  # Запись в лог завершения
            self.status_bar.config(text="Файл сгенерирован")  # Обновление строки состояния
        
        threading.Thread(target=gen, daemon=True).start()     # Запуск генерации в отдельном потоке-демоне
    
    def show_line_range(self):                                # Показ диапазона строк из исходного файла
        if not self.file_path or not os.path.exists(self.file_path):  # Проверка существования файла
            messagebox.showinfo("Нет файла", "Сначала выберите или сгенерируйте файл")  # Вывод предупреждения
            return                                            # Выход из метода
        
        try:                                                  # Блок обработки исключений
            start = int(self.start_line_var.get())            # Получение начальной строки и преобразование в int
            end = int(self.end_line_var.get())                # Получение конечной строки и преобразование в int
            
            if start <= 0:                                    # Проверка: начальная строка должна быть положительной
                messagebox.showerror("Ошибка", "Начальная строка должна быть больше 0")  # Сообщение об ошибке
                return                                        # Выход из метода
            if end < start:                                   # Проверка: конечная строка должна быть больше начальной
                messagebox.showerror("Ошибка", "Конечная строка должна быть больше начальной")  # Сообщение об ошибке
                return                                        # Выход из метода
            if end - start > 10000:                           # Если диапазон больше 10000 строк
                if not messagebox.askyesno("Предупреждение", f"Вы хотите показать {end - start + 1} строк. Это может занять время. Продолжить?"):  # Запрос подтверждения
                    return                                    # Выход, если пользователь отказался
        except ValueError:                                    # Обработка ошибки преобразования в число
            messagebox.showerror("Ошибка", "Введите корректные номера строк")  # Сообщение об ошибке
            return                                            # Выход из метода
        
        def load_range():                                     # Внутренняя функция загрузки диапазона строк
            self.log_insert("\n" + "="*60)                    # Разделитель в логе (60 знаков)
            self.log_insert(f"СТРОКИ {start} - {end} ИЗ ИСХОДНОГО ФАЙЛА")  # Заголовок с диапазоном
            self.log_insert(f"Файл: {os.path.basename(self.file_path)}")  # Имя файла
            self.log_insert("="*60)                           # Разделитель
            
            try:                                              # Блок обработки исключений
                with open(self.file_path, 'r', encoding='utf-8') as f:  # Открытие файла для чтения
                    line_count = 0                            # Счётчик прочитанных строк
                    shown = 0                                 # Счётчик показанных строк
                    for line in f:                            # Построчное чтение файла
                        line_count += 1                       # Увеличение счётчика строк
                        if start <= line_count <= end:        # Если строка в нужном диапазоне
                            self.log_insert(f"{line_count:6d}. {line.strip()}")  # Вывод номера и содержимого строки
                            shown += 1                        # Увеличение счётчика показанных
                            if shown % 100 == 0:              # Каждые 100 строк
                                self.root.update()            # Обновление интерфейса
                        elif line_count > end:                # Если дошли до конца диапазона
                            break                             # Прерывание цикла
                    
                    if shown == 0:                            # Если строки не найдены
                        self.log_insert(f"Строки с {start} по {end} не найдены. В файле {line_count} строк.")  # Сообщение
                    else:                                     # Иначе
                        self.log_insert(f"\nПоказано строк: {shown}")  # Общее количество показанных строк
                
                self.log_insert("="*60 + "\n")                # Завершающий разделитель
                self.status_bar.config(text=f"Показаны строки {start}-{end}")  # Обновление строки состояния
                
            except Exception as e:                            # Обработка любых ошибок
                self.log_insert(f"Ошибка при загрузке: {e}")  # Запись ошибки в лог
        
        threading.Thread(target=load_range, daemon=True).start()  # Запуск загрузки в отдельном потоке
    
    def run_sort(self):                                       # Функция запуска сортировки
        if not self.file_path:                                # Проверка, выбран ли файл
            messagebox.showerror("Ошибка", "Выберите CSV файл")  # Сообщение об ошибке
            return                                            # Выход из метода
        
        self.sort_btn.config(state='disabled', text="СОРТИРОВКА ВЫПОЛНЯЕТСЯ...")  # Блокировка кнопки и смена текста
        self.status_bar.config(text="Сортировка в процессе...")  # Обновление строки состояния
        
        def task():                                           # Внутренняя функция для запуска в потоке
            key = self.key_var.get()                          # Получение выбранного ключа сортировки
            impl = self.impl_var.get()                        # Получение выбранной реализации
            order = self.order_var.get()                      # === Получение выбранного порядка сортированных строк
            
            # == Добавление порядка в логи
            self.log_insert(f"\n{'='*50}")                    # Разделитель в логе
            self.log_insert(f"Запуск сортировки | Ключ: {key} | Порядок: {'возрастание' if order == 'asc' else 'убывание'} | Реализация: {impl}")  # ==
            self.log_insert(f"{'='*50}\n")                    # Разделитель
            
            start_time = time.time()                          # Запись времени начала сортировки
            
            if impl == "Python":                              # Если выбрана Python реализация
                import external_sort                         # Импорт модуля сортировки
                # === передача параметра order в функцию сортировки
                external_sort.external_sort(self.file_path, "sorted.txt", key, order)
            else:                                             # Если выбрана C++ реализация
                exe = "./external_sort.exe" if os.name == 'nt' else "./external_sort"  # Путь к исполняемому файлу (Windows/Linux)
                # === Передаем параетр order в C++ программу
                sort_order = "desc" if order == "desc" else "asc"
                if not os.path.exists(exe):                   # Проверка существования файла
                    self.log_insert("ОШИБКА: C++ программа не скомпилирована!")  # Сообщение об ошибке
                    self.log_insert("Выполните: g++ -std=c++17 -O2 external_sort.cpp -o external_sort")  # Инструкция по компиляции
                else:                                         # Если файл существует
                    # == добавляем order в командную строку
                    sort_order = "desc" if order == "desc" else "asc"
                    proc = subprocess.Popen([exe, self.file_path, "sorted.txt", key, sort_order], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)  # ==
                    for line in proc.stdout:                  # Чтение вывода программы построчно
                        self.log_insert(line.strip())         # Запись вывода в лог
                    proc.wait()                               # Ожидание завершения процесса
            
            elapsed = time.time() - start_time                # Вычисление затраченного времени
            self.log_insert(f"\nСортировка завершена за {elapsed:.2f} секунд!")  # Сообщение о завершении со временем
            
            if os.path.exists("sorted.txt"):                  # Проверка существования выходного файла
                size = os.path.getsize("sorted.txt") / (1024**3)  # Получение размера в ГБ
                self.log_insert(f"Размер выходного файла: {size:.2f} ГБ")  # Вывод размера
            
            self.sort_btn.config(state='normal', text="ЗАПУСТИТЬ СОРТИРОВКУ")  # Разблокировка кнопки и восстановление текста
            self.status_bar.config(text="Сортировка завершена")  # Обновление строки состояния
        
        threading.Thread(target=task, daemon=True).start()    # Запуск сортировки в отдельном потоке
    
    def show_custom_lines(self):                              # Метод показа первых N строк отсортированного файла
        if not os.path.exists("sorted.txt"):                  # Проверка существования файла
            messagebox.showinfo("Нет файла", "Сначала выполните сортировку")  # Предупреждение
            return                                            # Выход из метода
        
        try:                                                  # Блок обработки исключений
            n = int(self.lines_count_var.get())               # Получение количества строк для показа
            if n <= 0:                                        # Проверка: число должно быть положительным
                messagebox.showerror("Ошибка", "Введите положительное число")  # Сообщение об ошибке
                return                                        # Выход из метода
            if n > 100000:                                    # Если нужно показать >100000 строк
                if not messagebox.askyesno("Предупреждение", f"Вы хотите показать {n} строк. Это может занять время. Продолжить?"):  # Запрос подтверждения
                    return                                    # Выход, если пользователь отказался
        except:                                               # Обработка ошибки преобразования
            messagebox.showerror("Ошибка", "Введите число")    # Сообщение об ошибке
            return                                            # Выход из методa
        
        def load():                                           # Внутренняя функция загрузки строк
            self.log_insert("\n" + "="*60)                    # Разделитель
            self.log_insert(f"ПЕРВЫЕ {n} СТРОК ОТСОРТИРОВАННОГО ФАЙЛА")  # Заголовок
            self.log_insert("="*60)                           # Разделитель
            
            with open("sorted.txt", 'r', encoding='utf-8') as f:  # Открытие отсортированного файла
                for i, line in enumerate(f):                  # Построчное чтение с нумерацией
                    if i >= n:                                # Если достигли нужного количества
                        total = self.get_total_lines()        # Получение общего количества строк
                        self.log_insert(f"\n... и ещё {total - n} строк ...")  # Сообщение о пропущенных строках
                        break                                 # Прерывание цикла
                    self.log_insert(f"{i+1:6d}. {line.strip()}")  # Вывод номера и строки
                    if (i+1) % 100 == 0:                      # Каждые 100 строк
                        self.root.update()                    # Обновление интерфейса
            
            self.log_insert("="*60 + "\n")                    # Завершающий разделитель
        
        threading.Thread(target=load, daemon=True).start()    # Запуск загрузки в отдельном потоке
    
    def show_full_result(self):                               # Метод показа всего отсортированного файла
        if not os.path.exists("sorted.txt"):                  # Проверка существования файла
            messagebox.showinfo("Нет файла", "Сначала выполните сортировку")  # Предупреждение
            return                                            # Выход из метода
        
        total_lines = self.get_total_lines()                  # Получение общего количества строк
        if not messagebox.askyesno("Подтверждение", f"Файл содержит {total_lines:,} строк.\nПоказать весь файл? Это может занять время."):  # Запрос подтверждения
            return                                            # Выход, если пользователь отказался
        
        def load():                                           # Внутренняя функция загрузки всего файла
            self.log_insert("\n" + "="*60)                    # Разделитель
            self.log_insert("ВЕСЬ ОТСОРТИРОВАННЫЙ ФАЙЛ")       # Заголовок
            self.log_insert("="*60)                           # Разделитель
            
            with open("sorted.txt", 'r', encoding='utf-8') as f:  # Открытие файла
                count = 0                                     # Счётчик строк
                for line in f:                                # Построчное чтение
                    self.log_insert(f"{count+1:6d}. {line.strip()}")  # Вывод номера и строки
                    count += 1                                # Увеличение счётчика
                    if count % 500 == 0:                      # Каждые 500 строк
                        self.root.update()                    # Обновление интерфейса
            
            self.log_insert(f"\nВСЕГО СТРОК: {count}")        # Общее количество строк
            self.log_insert("="*60 + "\n")                    # Завершающий разделитель
        
        threading.Thread(target=load, daemon=True).start()    # Запуск загрузки в отдельном потоке
    
    def get_total_lines(self):                                # Метод подсчёта строк в отсортированном файле
        try:                                                  # Блок обработки исключений
            with open("sorted.txt", 'r', encoding='utf-8') as f:  # Открытие файла
                return sum(1 for _ in f)                      # Подсчёт и возврат количества строк
        except:                                               # В случае ошибки
            return 0                                          # Возврат 0
    
    def clear_log(self):                                      # Метод очистки лога
        self.log.delete(1.0, tk.END)                          # Удаление всего содержимого лога
        self.log_insert("Лог очищен")                         # Запись сообщения об очистке
        self.status_bar.config(text="Лог очищен")             # Обновление строки состояния
    
    def close_program(self):                                  # Метод закрытия программы
        if messagebox.askokcancel("Выход", "Закрыть программу?"):  # Запрос подтверждения
            self.root.quit()                                  # Завершение главного цикла tkinter
            self.root.destroy()                               # Уничтожение окна
    
    def log_insert(self, msg):                                # Метод добавления сообщения в лог
        self.log.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {msg}\n")  # Вставка сообщения с временной меткой
        self.log.see(tk.END)                                  # Прокрутка вниз (показ последнего сообщения)
        self.root.update()                                    # Принудительное обновление интерфейса

if __name__ == "__main__":                                   # Проверка, что скрипт запущен напрямую
    root = tk.Tk()                                            # Создание главного окна tkinter
    app = SimpleSortApp(root)                                 # Создание экземпляра приложения
    root.protocol("WM_DELETE_WINDOW", app.close_program)      # Обработка закрытия окна через крестик
    root.mainloop()                                           # Запуск главного цикла обработки событий
