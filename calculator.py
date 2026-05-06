import tkinter as tk
from tkinter import font
import math

class ModernCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Красивый калькулятор")
        self.root.geometry("360x550")
        self.root.resizable(False, False)
        self.root.configure(bg='#2C3E50')
        
        # Установка иконки (опционально)
        try:
            self.root.iconbitmap('calculator.ico')
        except:
            pass
        
        # Переменные
        self.current_expression = ""
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        self.history_var = tk.StringVar()
        
        # Настройка сетки
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.setup_ui()
        self.bind_keys()
    
    def setup_ui(self):
        # Главный контейнер
        main_frame = tk.Frame(self.root, bg='#2C3E50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Дисплей истории
        history_frame = tk.Frame(main_frame, bg='#34495E', height=40)
        history_frame.pack(fill=tk.X, pady=(0, 5))
        history_frame.pack_propagate(False)
        
        history_label = tk.Label(
            history_frame,
            textvariable=self.history_var,
            font=('Segoe UI', 11),
            bg='#34495E',
            fg='#95A5A6',
            anchor='e',
            padx=15
        )
        history_label.pack(fill=tk.BOTH, expand=True)
        
        # Дисплей результата
        display_frame = tk.Frame(main_frame, bg='#34495E', height=80)
        display_frame.pack(fill=tk.X, pady=(0, 15))
        display_frame.pack_propagate(False)
        
        result_label = tk.Label(
            display_frame,
            textvariable=self.result_var,
            font=('Segoe UI', 36, 'bold'),
            bg='#34495E',
            fg='#ECF0F1',
            anchor='e',
            padx=15
        )
        result_label.pack(fill=tk.BOTH, expand=True)
        
        # Кнопки
        buttons_frame = tk.Frame(main_frame, bg='#2C3E50')
        buttons_frame.pack(fill=tk.BOTH, expand=True)
        
        # Конфигурация кнопок
        buttons = [
            ['C', '⌫', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['±', '0', '.', '=']
        ]
        
        # Цвета для разных типов кнопок
        colors = {
            'default': {'bg': '#4A6FA5', 'fg': '#ECF0F1', 'hover': '#5B8BC7'},
            'operator': {'bg': '#E67E22', 'fg': '#ECF0F1', 'hover': '#F39C12'},
            'function': {'bg': '#3D5A80', 'fg': '#ECF0F1', 'hover': '#4F7096'},
            'equals': {'bg': '#27AE60', 'fg': '#ECF0F1', 'hover': '#2ECC71'}
        }
        
        for i, row in enumerate(buttons):
            buttons_frame.grid_rowconfigure(i, weight=1)
            for j, btn_text in enumerate(row):
                buttons_frame.grid_columnconfigure(j, weight=1)
                
                # Определяем тип кнопки
                if btn_text in ['/', '*', '-', '+']:
                    color_type = 'operator'
                elif btn_text in ['C', '⌫', '%', '±']:
                    color_type = 'function'
                elif btn_text == '=':
                    color_type = 'equals'
                else:
                    color_type = 'default'
                
                btn = tk.Button(
                    buttons_frame,
                    text=btn_text,
                    font=('Segoe UI', 16, 'bold'),
                    bg=colors[color_type]['bg'],
                    fg=colors[color_type]['fg'],
                    bd=0,
                    cursor='hand2',
                    activebackground=colors[color_type]['hover'],
                    activeforeground='#ECF0F1'
                )
                
                # Привязка команды
                if btn_text == '=':
                    btn.configure(command=self.calculate)
                elif btn_text == 'C':
                    btn.configure(command=self.clear)
                elif btn_text == '⌫':
                    btn.configure(command=self.backspace)
                elif btn_text == '±':
                    btn.configure(command=self.negate)
                else:
                    btn.configure(command=lambda x=btn_text: self.add_to_expression(x))
                
                btn.grid(row=i, column=j, padx=2, pady=2, sticky='nsew')
                
                # Анимация наведения
                btn.bind("<Enter>", lambda e, b=btn, c=color_type: b.configure(bg=colors[c]['hover']))
                btn.bind("<Leave>", lambda e, b=btn, c=color_type: b.configure(bg=colors[c]['bg']))
    
    def add_to_expression(self, value):
        current = self.result_var.get()
        
        if current == "0" or current == "Ошибка":
            if value in ['.', '00']:
                self.result_var.set("0" + value)
            else:
                self.result_var.set(value)
        else:
            if value == '%':
                self.result_var.set(current + "/100")
            else:
                self.result_var.set(current + value)
        
        # Обновляем историю
        self.history_var.set(self.result_var.get() if '=' not in self.result_var.get() else "")
    
    def calculate(self):
        try:
            expression = self.result_var.get()
            
            # Замена символов для вычисления
            expression = expression.replace('×', '*').replace('÷', '/')
            
            # Сохраняем выражение в историю
            self.history_var.set(expression + " =")
            
            # Вычисляем результат
            result = eval(expression)
            
            # Форматируем результат
            if isinstance(result, float):
                if abs(result) >= 1e10 or (abs(result) < 1e-10 and result != 0):
                    result = f"{result:.10e}"
                else:
                    # Округляем до 10 знаков после запятой и убираем лишние нули
                    result = f"{result:.10f}".rstrip('0').rstrip('.')
                    if len(result) > 15:
                        result = f"{float(result):.8e}"
            
            self.result_var.set(str(result))
            
        except ZeroDivisionError:
            self.result_var.set("Ошибка")
            self.history_var.set("Деление на ноль")
        except:
            self.result_var.set("Ошибка")
            self.history_var.set("Неверное выражение")
    
    def clear(self):
        self.result_var.set("0")
        self.history_var.set("")
    
    def backspace(self):
        current = self.result_var.get()
        if len(current) > 1:
            self.result_var.set(current[:-1])
        else:
            self.result_var.set("0")
        self.history_var.set("")
    
    def negate(self):
        current = self.result_var.get()
        if current and current != "0" and current != "Ошибка":
            if current.startswith('-'):
                self.result_var.set(current[1:])
            else:
                self.result_var.set('-' + current)
    
    def bind_keys(self):
        # Привязка клавиш клавиатуры
        self.root.bind('<Key>', self.key_press)
        self.root.bind('<Return>', lambda e: self.calculate())
        self.root.bind('<BackSpace>', lambda e: self.backspace())
        self.root.bind('<Escape>', lambda e: self.clear())
    
    def key_press(self, event):
        key = event.char
        allowed_keys = '0123456789+-*/.%'
        
        if key in allowed_keys:
            self.add_to_expression(key)
        elif event.keysym in ['equal', 'KP_Enter']:
            self.calculate()

def main():
    root = tk.Tk()
    
    # Центрирование окна
    window_width = 360
    window_height = 550
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    app = ModernCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
