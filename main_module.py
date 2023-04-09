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
)
from PyQt5.QtCore import Qt
from subprocess import Popen, CREATE_NEW_CONSOLE
import re
from Configs.python_syntax import PythonSyntaxHighlighter  # Относительный импорт класса PythonSyntaxHighlighter

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.text_edit = QTextEdit()  # Создание экземпляра QTextEdit
        self.setup_syntax_highlighting()

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

        self.tab1.setLayout(layout1)

        # Создаем кнопку для запуска команды
        button = QPushButton("Запустить команду")

        # Подключаем слот-функцию к сигналу нажатия кнопки
        button.clicked.connect(self.start_cmd)
        
        # Создаем панель с текстовым редактором справа от списка команд
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setMinimumWidth(300)
        dock = QDockWidget("Текст команды", self)
        dock.setWidget(self.text_edit)
        dock.setAllowedAreas(Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        
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
            pattern = r'@bot\.command\(\)\s+async\s+def\s+{}\((.*?)\)(?=\n@bot\.command|$)'.format(selected_command)
            match = re.search(pattern, commands, re.DOTALL)
            if match:
                command_code = match.group(0)
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
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())