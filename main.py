import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import webbrowser


class ToolTip:
    #Инициализация
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    #Отображение всплывающей подсказки при наведении курсора
    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tip_window = tk.Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)
        self.tip_window.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tip_window, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    #Скрытие всплывающей подсказки
    def hide_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
        self.tip_window = None


class TextProcessorEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Лексер")
        self.root.geometry("800x600")

        self.filename = None
        self.saved_text = ""  # Для отслеживания сохраненного состояния
        self.modified = False

        self.new_img = None
        self.open_img = None
        self.save_img = None
        self.back_img = None
        self.forward_img = None
        self.copy_img = None
        self.cut_img = None
        self.insert_img = None
        self.run_img = None
        self.help_img = None
        self.about_img = None
        #Создание основного меню программы
        self.create_menu()

        self.load_images()
        #Создание панели инструментов
        self.create_toolbar()

        #Создание области ввода/редактирования текста
        self.create_text_area()

        #Создание области результатов (с запретом ввода)
        self.create_output_area()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)



    def load_images(self):
        try:

            self.new_img = tk.PhotoImage(file="new.png")
            self.open_img = tk.PhotoImage(file="open.png")
            self.save_img = tk.PhotoImage(file="save.png")
            self.back_img = tk.PhotoImage(file="back.png")
            self.forward_img = tk.PhotoImage(file="forward.png")
            self.copy_img = tk.PhotoImage(file="copy.png")
            self.cut_img = tk.PhotoImage(file="cut.png")
            self.insert_img = tk.PhotoImage(file="insert.png")
            self.run_img = tk.PhotoImage(file="play.png")
            self.help_img = tk.PhotoImage(file="balloon.png")
            self.about_img = tk.PhotoImage(file="property.png")

        except Exception as e:

            print(f"Ошибка загрузки изображений: {e}")


    def create_menu(self):
        menu_bar = tk.Menu(self.root)

        # Меню Файл
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Создать", command=self.new_file)
        file_menu.add_command(label="Открыть", command=self.open_file)
        file_menu.add_command(label="Сохранить", command=self.save_file)
        file_menu.add_command(label="Сохранить как", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        menu_bar.add_cascade(label="Файл", menu=file_menu)

        # Меню Правка
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Отменить", command=lambda: self.text_area.event_generate("<<Undo>>"))
        edit_menu.add_command(label="Повторить", command=lambda: self.text_area.event_generate("<<Redo>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Вырезать", command=lambda: self.text_area.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Копировать", command=lambda: self.text_area.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Вставить", command=lambda: self.text_area.event_generate("<<Paste>>"))
        edit_menu.add_command(label="Удалить", command=lambda: self.text_area.delete("sel.first", "sel.last"))
        edit_menu.add_command(label="Выделить все", command=lambda: self.text_area.tag_add("sel", "1.0", "end"))
        menu_bar.add_cascade(label="Правка", menu=edit_menu)

        # Меню Текст
        text_menu = tk.Menu(menu_bar, tearoff=0)
        # Все пункты меню "Текст" выводят одинаковое сообщение
        text_menu.add_command(label="Постановка задачи",
                              command=lambda: messagebox.showinfo("Информация",
                                                                  "Реализовано в последующих лабораторных работах"))
        text_menu.add_command(label="Грамматика",
                              command=lambda: messagebox.showinfo("Информация",
                                                                  "Реализовано в последующих лабораторных работах"))
        text_menu.add_command(label="Классификация грамматики",
                              command=lambda: messagebox.showinfo("Информация",
                                                                  "Реализовано в последующих лабораторных работах"))
        text_menu.add_command(label="Метод анализа",
                              command=lambda: messagebox.showinfo("Информация",
                                                                  "Реализовано в последующих лабораторных работах"))
        text_menu.add_command(label="Диагностика ошибок",
                              command=lambda: messagebox.showinfo("Информация",
                                                                  "Реализовано в последующих лабораторных работах"))
        text_menu.add_command(label="Тестовый пример",
                              command=lambda: messagebox.showinfo("Информация",
                                                                  "Реализовано в последующих лабораторных работах"))
        text_menu.add_command(label="Список литературы",
                              command=lambda: messagebox.showinfo("Информация",
                                                                  "Реализовано в последующих лабораторных работах"))
        text_menu.add_command(label="Исходный код",
                              command=lambda: messagebox.showinfo("Информация",
                                                                  "Реализовано в последующих лабораторных работах"))
        menu_bar.add_cascade(label="Текст", menu=text_menu)

        # Меню Справка
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Справка", command=self.open_help)
        help_menu.add_command(label="О программе", command=self.show_about)
        menu_bar.add_cascade(label="Справка", menu=help_menu)

        self.root.config(menu=menu_bar)

    def create_toolbar(self):
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)

        # Создаем кнопки с изображениями или текстом
        buttons = [
            ("Новый", self.new_img, self.new_file, "Создать новый файл (Ctrl+N)", "<Control-n>"),
            ("Открыть", self.open_img, self.open_file, "Открыть файл (Ctrl+O)", "<Control-o>"),
            ("Сохранить", self.save_img, self.save_file, "Сохранить файл (Ctrl+S)", "<Control-s>"),
            ("Назад", self.back_img, self.navigate_back, "Назад (Alt+Left)", "<Alt-Left>"),
            ("Вперед", self.forward_img, self.navigate_forward, "Вперед (Alt+Right)", "<Alt-Right>"),
            ("Вырезать", self.cut_img, self.cut_text, "Вырезать (Ctrl+X)", "<Control-x>"),
            ("Копировать", self.copy_img, self.copy_text, "Копировать (Ctrl+C)", "<Control-c>"),
            ("Вставить", self.insert_img, self.paste_text, "Вставить (Ctrl+V)", "<Control-v>"),
            ("Анализ", self.run_img, self.run_analysis, "Пуск (F5)", "<F5>"),
            ("Справка", self.help_img, self.open_help, "Вызов справки (F1)", "<F1>"),
            ("О программе", self.about_img, self.show_about, "О программе", None)  # None для hotkey
        ]

        for text, img, command, tooltip, hotkey in buttons:
            if img:
                btn = tk.Button(toolbar, image=img, command=command, relief=tk.FLAT)
                btn.image = img  # Сохраняем ссылку на изображение
            else:
                btn = tk.Button(toolbar, text=text, command=command)

            if hotkey:
                self.root.bind(hotkey, lambda e, cmd=command: cmd())

            ToolTip(btn, tooltip)
            btn.pack(side=tk.LEFT, padx=2, pady=2)

        toolbar.pack(side=tk.TOP, fill=tk.X)


    def new_file(self):
        if self.check_unsaved_changes():
            self.text_area.delete(1.0, tk.END)
            self.filename = None
            self.saved_text = ""
            self.modified = False
            self.clear_output()
            self.add_output("Создан новый документ")

    def open_file(self):
        if not self.check_unsaved_changes():
            return

        file_path = filedialog.askopenfilename(filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.text_area.delete("1.0", tk.END)
                    self.text_area.insert(tk.END, content)
                self.filename = file_path
                self.saved_text = content
                self.modified = False
                self.add_output(f"Документ открыт: {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть файл: {e}")
    def save_file(self):
        if self.filename:
            try:
                content = self.text_area.get("1.0", tk.END)
                with open(self.filename, "w", encoding="utf-8") as file:
                    file.write(content)
                self.saved_text = content
                self.modified = False
                self.add_output(f"Документ сохранен: {self.filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.text_area.get("1.0", tk.END))
                self.filename = file_path
                self.add_output(f"Документ сохранен как: {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")
    def navigate_back(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", self.history[self.history_index])
            self.add_output("Отменено последнее действие")

    def navigate_forward(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", self.history[self.history_index])
            self.add_output("Повторено последнее действие")

    def update_history(self):
        current_text = self.text_area.get("1.0", tk.END)
        if not self.history or current_text != self.history[self.history_index]:
            self.history = self.history[:self.history_index + 1]
            self.history.append(current_text)
            self.history_index = len(self.history) - 1
            if len(self.history) > 100:  # Ограничиваем историю
                self.history.pop(0)
                self.history_index -= 1

    # Методы работы с буфером обмена
    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")
        self.add_output("Текст скопирован в буфер обмена")

    def cut_text(self):
        self.text_area.event_generate("<<Cut>>")
        self.modified = True
        self.add_output("Текст вырезан в буфер обмена")

    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")
        self.modified = True
        self.add_output("Текст вставлен из буфера обмена")

    def run_analysis(self):
        messagebox.showinfo("Информация",
                            "Реализовано в последующих лабораторных работах")
    def create_text_area(self):
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True)

        self.text_area = scrolledtext.ScrolledText(
            frame,
            wrap=tk.WORD,
            undo=True,
            font=('Arial', 12)
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

    def create_output_area(self):
        frame = tk.Frame(self.root, height=150)
        frame.pack(fill=tk.X, side=tk.BOTTOM)

        tk.Label(frame, text="Результаты обработки:").pack(anchor=tk.W)

        self.output_area = tk.Text(
            frame,
            bg="#f0f0f0",
            state=tk.DISABLED,
            font=('Arial', 10)
        )
        scroll = tk.Scrollbar(frame, command=self.output_area.yview)
        self.output_area.configure(yscrollcommand=scroll.set)

        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_area.pack(fill=tk.BOTH, expand=True)



    def add_output(self, text):
        self.output_area.config(state=tk.NORMAL)
        self.output_area.insert(tk.END, text + "\n")
        self.output_area.config(state=tk.DISABLED)
        self.output_area.see(tk.END)

    def clear_output(self):
        self.output_area.config(state=tk.NORMAL)
        self.output_area.delete(1.0, tk.END)
        self.output_area.config(state=tk.DISABLED)

    def show_text(self, title):
        self.add_output(f"Выбран раздел: {title}")

    def open_help(self):
        try:
            webbrowser.open("help.html")
            self.add_output("Открыто руководство пользователя")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть справку: {e}")

    def show_about(self):
        about_text = "Лексический анализатор\nВерсия 1.0\n\nАвтор: Анастасия Евдокимова"
        messagebox.showinfo("О программе", about_text)
        self.add_output("Показана информация о программе")

    def check_unsaved_changes(self):
        """Проверяет наличие несохраненных изменений и предлагает сохранить"""
        current_text = self.text_area.get("1.0", tk.END)
        if self.modified or (self.saved_text != current_text):
            response = messagebox.askyesnocancel(
                "Несохраненные изменения",
                "У вас есть несохраненные изменения. Хотите сохранить перед продолжением?"
            )
            if response is None:  # Нажата "Отмена"
                return False
            elif response:  # Нажата "Да"
                self.save_file()
                return True
            else:  # Нажата "Нет"
                return True
        return True

    def on_closing(self):
        """Обработчик закрытия окна"""
        if self.check_unsaved_changes():
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TextProcessorEditor(root)
    root.mainloop()