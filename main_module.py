import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QDockWidget,
    QHBoxLayout,
    QTextEdit,
    QListWidget,
    QMessageBox,
    QMenu,
    QAction,
    QActionGroup,
    QDialog,
)
from PyQt5.QtCore import Qt
from subprocess import Popen, CREATE_NEW_CONSOLE
import re
from Configs.python_syntax import PythonSyntaxHighlighter  # Относительный импорт класса PythonSyntaxHighlighter
from Configs.BotSettingsDialog import BotSettingsDialog
from Configs.BotSettings import config

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.text_edit = QTextEdit()  # Создание экземпляра QTextEdit
        self.setup_syntax_highlighting()

        self.config = config
        
        # Создаем контекстное меню
        self.context_menu = QMenu(self)
        copy_action = QAction("Копировать имя функции", self)
        copy_action.triggered.connect(self.copy_function_name)
        self.context_menu.addAction(copy_action)

        # Создаем менюбар
        menu_bar = self.menuBar()

        # Создаем меню "Файл"
        file_menu = menu_bar.addMenu("Файл")

        # Создаем подменю "Открыть"
        open_menu = QMenu("Открыть", self)
        file_menu.addMenu(open_menu)

        # Создаем действие "Открыть файл"
        open_file_action = QAction("Открыть файл", self)
        open_menu.addAction(open_file_action)

        # Создаем действие "Открыть папку"
        open_folder_action = QAction("Открыть папку", self)
        open_menu.addAction(open_folder_action)

        # Добавляем разделитель
        file_menu.addSeparator()

        # Создаем действие "Сохранить"
        save_action = QAction("Сохранить", self)
        file_menu.addAction(save_action)

        # Добавляем разделитель
        file_menu.addSeparator()
        
        # Создаем меню "Вид"
        view_menu = menu_bar.addMenu("Вид")

        # Создаем группу действий для кнопок переключения
        view_action_group = QActionGroup(self)

        # Создаем действие "Отображение всех элементов"
        show_all_action = QAction("Отображение всех элементов", self)
        show_all_action.setCheckable(True)
        view_action_group.addAction(show_all_action)

        # Создаем действие "Скрытие всех элементов"
        hide_all_action = QAction("Скрытие всех элементов", self)
        hide_all_action.setCheckable(True)
        view_action_group.addAction(hide_all_action)
        
        # Добавляем действия в меню "Вид"
        view_menu.addAction(show_all_action)
        view_menu.addAction(hide_all_action)
        
        # Создаем действие "Выход"
        exit_action = QAction("Выход", self)
        file_menu.addAction(exit_action)

        # Создаем меню "Настройки"
        settings_menu = menu_bar.addMenu("Настройки")

        # Создаем действие "Настройки приложения"
        app_settings_action = QAction("Настройки приложения", self)
        settings_menu.addAction(app_settings_action)
        
        # Создаем действие "Настройки Бота"
        show_bot_settings = QAction("Настройки бота", self)
        show_bot_settings.triggered.connect(self.show_bot_settings)  # Правильное подключение слот-функции
        settings_menu.addAction(show_bot_settings)

        # Подключаем сигналы к слотам
        open_file_action.triggered.connect(self.open_file)
        open_folder_action.triggered.connect(self.open_folder)
        save_action.triggered.connect(self.save)
        exit_action.triggered.connect(self.exit)
        app_settings_action.triggered.connect(self.app_settings)
        show_all_action.triggered.connect(self.show_all)
        hide_all_action.triggered.connect(self.hide_all)

        
        # Устанавливаем размер окна
        self.resize(800, 600)
        self.setWindowTitle("Приложение для редактирования бота от Doctor Oz")

        # Создаем виджет вкладок
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Создаем вкладку 1
        self.tab1 = QWidget()
        self.tab_widget.addTab(self.tab1, "Вкладка 1")

        # Создаем панель с кнопками на вкладке 1
        layout1 = QVBoxLayout()
        label1 = QLabel("Содержимое вкладки 1")
        layout1.addWidget(label1)

        # Создаем QListWidget для отображения списка команд
        self.list_widget = QListWidget()
        layout1.addWidget(self.list_widget)

        # Загружаем команды из файла main.py
        with open("Main/main.py", "r", encoding='utf-8') as file:
            commands = file.read()
            pattern = r'@bot\.command\(\)\s+async\s+def\s+(\w+)'
            commands_list = re.findall(pattern, commands)

        # Добавляем команды в QListWidget
        for command in commands_list:
            self.list_widget.addItem(command)

        # Подключаем слот-функцию к сигналу выбора команды в списке
        self.list_widget.itemClicked.connect(self.show_command_code)

        # Устанавливаем контекстное меню для QListWidget
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_context_menu)

        # Создаем кнопку "Создать новую команду"
        create_command_button = QPushButton("Создать новую команду", self)
        create_command_button.clicked.connect(self.create_new_command)
        layout1.addWidget(create_command_button)

        # Создаем кнопку "Перезагрузить команды"
        reload_commands_button = QPushButton("Перезагрузить команды", self)
        reload_commands_button.clicked.connect(self.reload_commands)
        layout1.addWidget(reload_commands_button)

        self.tab1.setLayout(layout1)

        # Создаем кнопку для запуска команды
        button = QPushButton("Запустить команду")

        # Подключаем слот-функцию к сигналу нажатия кнопки
        button.clicked.connect(self.start_cmd)
        
        # Создаем кнопку "Сохранить команду"
        save_button = QPushButton("Сохранить команду")
        save_button.clicked.connect(self.save_command)
        dock_layout = QVBoxLayout()
        dock_layout.addWidget(self.text_edit)
        dock_layout.addWidget(save_button)
        dock_widget = QWidget()
        dock_widget.setLayout(dock_layout)
        dock = QDockWidget("Текст команды", self)
        dock.setWidget(dock_widget)
        dock.setAllowedAreas(Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)

        # Устанавливаем главный виджет в качестве центрального виджета окна
        self.setCentralWidget(self.tab_widget)
        
        # Создаем панель с кнопками внизу
        buttons_panel = QDockWidget("Панель с кнопками", self)
        buttons_panel.setWidget(QWidget())
        buttons_layout = QHBoxLayout()
        buttons_panel.widget().setLayout(buttons_layout)
        buttons_layout.addWidget(QPushButton("Кнопка 5"))
        buttons_layout.addWidget(QPushButton("Кнопка 6"))
        button_cmd = QPushButton("Запустить командную строку", self)
        button_cmd.clicked.connect(self.start_cmd)
        buttons_layout.addWidget(button_cmd)
        buttons_panel.setFixedHeight(100)
        buttons_panel.setFeatures(QDockWidget.DockWidgetFloatable)
        buttons_panel.setAllowedAreas(Qt.BottomDockWidgetArea)
        self.addDockWidget(Qt.BottomDockWidgetArea, buttons_panel)
        
    def show_command_code(self, item):
        """Отображает код выбранной команды в текстовом редакторе"""
        selected_command = item.text()
        with open("Main/main.py", "r", encoding='utf-8') as file:
            commands = file.read()
            pattern = r'@bot\.command\(\)\s+async\s+def\s+{}\(.*?\)(?=\n@bot\.command\(|$)'.format(selected_command)
            match = re.search(pattern, commands, re.DOTALL)
            if match:
                command_code = match.group(0)
                command_code = re.sub(r'#---End Command---#.*', '', command_code, flags=re.DOTALL)  # Удаляем текст после "#---End Command---#"
                self.text_edit.setPlainText(command_code)
                
    def start_cmd(self):
        # Вызываем командную строку с командой python Main/main
        cmd = "python Main/main"
        Popen(cmd, creationflags=CREATE_NEW_CONSOLE)
        
    def setup_syntax_highlighting(self):
        """
        Метод для настройки подсветки синтаксиса в QTextEdit
        """
        self.highlighter = PythonSyntaxHighlighter(self.text_edit.document())

    def open_file(self):
        print("Открыть файл")

    def open_folder(self):
        print("Открыть папку")

    def save(self):
        print("Сохранить")

    def exit(self):
        print("Выход")

    def app_settings(self):
        print("Настройки приложения")
        
    def show_all(self):
        # Обработчик действия "Отображение всех элементов"
        print("Отображение всех элементов")

    def hide_all(self):
        # Обработчик действия "Скрытие всех элементов"
        print("Скрытие всех элементов")
        
    def create_new_command(self):
        # Обработчик события нажатия кнопки "Создать новую команду"
        command_name = f"название_команды_{self.list_widget.count() + 1}"
        command_code = f"@bot.command()\nasync def {command_name}(ctx):\n    #---End Command---#"
        with open("Main/main.py", "r+", encoding='utf-8') as file:
            # Читаем содержимое файла
            commands = file.read()
    
            # Ищем позицию, после которой нужно добавить элементы
            position = commands.find('#---End Command---#') + len('#---End Command---#')
    
            # Перемещаем указатель в нужное место
            file.seek(position)
    
            # Выполняем операцию записи
            file.write('\n@bot.command()\nasync def название_команды_(число)(ctx):\n#---End Command---#')
        self.list_widget.addItem(command_name)
        QMessageBox.information(self, "Информация", f"Команда '{command_name}' успешно создана и добавлена в список.")

    def reload_commands(self):
        # Обработчик события нажатия кнопки "Перезагрузить команды"
        self.list_widget.clear()

        # Загружаем команды из файла main.py
        with open("Main/main.py", "r", encoding='utf-8') as file:
            commands = file.read()
            pattern = r'@bot\.command\(\)\s+async\s+def\s+(\w+)'
            commands_list = re.findall(pattern, commands)

        # Добавляем команды в QListWidget
        for command in commands_list:
            self.list_widget.addItem(command)

    def save_command(self):
        # Обработчик события нажатия кнопки "Сохранить команду"
        command_name = self.list_widget.currentItem().text()
        command_code = self.text_edit.toPlainText()

        # Проверяем наличие существующей команды
        with open("Main/main.py", "r", encoding='utf-8') as file:
            commands = file.read()
            pattern = fr'@bot\.command\(\)\s+async\s+def\s+{command_name}\(ctx\):\s+#---End Command---#'
            if re.search(pattern, commands, flags=re.DOTALL):
                # Если команда уже существует, выводим предупреждение
                result = QMessageBox.question(self, "Предупреждение",
                                            f"Команда '{command_name}' уже существует. Вы хотите её заменить?",
                                            QMessageBox.Ok | QMessageBox.Cancel)
                if result == QMessageBox.Ok:
                    # Если нажата кнопка "ОК", удаляем старую команду
                    commands = re.sub(pattern, "", commands, flags=re.DOTALL)
                else:
                    # Если нажата кнопка "Отмена", выходим из функции
                    return

            # Записываем код команды в файл main.py
            replacement = f"@bot.command()\nasync def {command_name}(ctx):\n{command_code}\n    #---End Command---#\n\n"
            commands = commands.strip()  # Удаляем лишние пробелы и переносы строк в конце файла
            # Ищем строку "bot.run(config['token'])" и добавляем сохранение перед нею
            bot_run_pattern = r'bot\.run\(config\[\'token\'\]\)'
            bot_run_match = re.search(bot_run_pattern, commands, flags=re.DOTALL)
            if bot_run_match:
                bot_run_start = bot_run_match.start()
                commands = commands[:bot_run_start] + f"\n{replacement}\n" + commands[bot_run_start:]
            else:
                # Если строка "bot.run(config['token'])" не найдена, то добавляем сохранение в конец файла
                commands += f"\n{replacement}"
            file.seek(0)
            file.write(commands)

        QMessageBox.information(self, "Сохранение команды", "Команда успешно сохранена!")

        # Перезагружаем список команд
        self.reload_commands()

        
    # Слот-функция для отображения контекстного меню
    def show_context_menu(self, pos):
        self.context_menu.exec_(self.list_widget.mapToGlobal(pos))

    # Слот-функция для копирования имени функции
    def copy_function_name(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            function_name = selected_item.text()
            # Выполняем операцию копирования имени функции в буфер обмена
            QApplication.clipboard().setText(function_name)
            
    # Слот-функция для отображения окна настроек бота
    def show_bot_settings(self):
        # Использование атрибута config для доступа к значениям настроек
        bot_settings_dialog = BotSettingsDialog()  # Передаем config в конструктор BotSettingsDialog
        bot_settings_dialog.token_edit.setText(self.config['token'])
        bot_settings_dialog.prefix_edit.setText(self.config['prefix'])

        bot_settings_dialog.exec_()

            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())