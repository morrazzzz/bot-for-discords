from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTabWidget, QWidget
import sys
from Configs.BotSettings import config
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator

class BotSettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.config = config
        self.setFixedSize(600, 400)
        
        # Создаем компоновщики
        general_layout = QVBoxLayout()
        elements_layout_right = QVBoxLayout()

        # Создаем элемент "Префикс бота"
        prefix_label = QLabel("Сменить префикс бота:")
        self.prefix_edit = QLineEdit()
        elements_layout_right.addWidget(prefix_label)
        elements_layout_right.addWidget(self.prefix_edit)

        # Создаем элемент "Токен бота"
        token_label = QLabel("Сменить токен бота:")
        self.token_edit = QLineEdit()
        elements_layout_right.addWidget(token_label)
        elements_layout_right.addWidget(self.token_edit)

        # Создаем панели кнопок
        buttons_panel_left = QWidget()
        buttons_panel_left.setLayout(QVBoxLayout())

        elements_panel_right = QWidget()
        elements_panel_right.setLayout(elements_layout_right)

        # Создаем вкладку "Основные настройки" и добавляем на нее виджеты
        general_tab = QWidget()
        general_tab.setLayout(QVBoxLayout())
        general_tab.layout().addWidget(buttons_panel_left)
        general_tab.layout().addWidget(elements_panel_right)

        # Создаем вкладку "Настройки каналов" и добавляем на нее виджеты
        channels_tab = QWidget()
        channels_tab.setLayout(QVBoxLayout())
        
        # Получаем каналы из config
        welcome_channel_id = config['WelcomeChannel']
        goodbye_channel_id = config['GoodByeChannel']
        audit_channel_id = config['AuditChannel']
        
        # Создаем виджеты QLineEdit для отображения и редактирования значений каналов
        welcome_edit = QLineEdit()
        welcome_edit.setValidator(QRegExpValidator(QRegExp("[0-9]*")))  # Устанавливаем фильтр на вводимые символы (только цифры)
        welcome_edit.setText(welcome_channel_id)
        goodbye_edit = QLineEdit()
        goodbye_edit.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
        goodbye_edit.setText(goodbye_channel_id)
        audit_edit = QLineEdit()
        audit_edit.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
        audit_edit.setText(audit_channel_id)

        # Добавляем виджеты на вкладку
        channels_tab.layout().addWidget(QLabel("Канал для приветствий:"))
        channels_tab.layout().addWidget(welcome_edit)
        channels_tab.layout().addWidget(QLabel("Канал для прощаний:"))
        channels_tab.layout().addWidget(goodbye_edit)
        channels_tab.layout().addWidget(QLabel("Канал аудита:"))
        channels_tab.layout().addWidget(audit_edit)

        # Добавляем вкладки на виджет вкладок
        self.tabs = QTabWidget()
        self.tabs.addTab(general_tab, "Основные настройки")
        self.tabs.addTab(channels_tab, "Настройки каналов")

        # Создаем кнопку "ОК" и добавляем ее в диалоговое окно
        ok_button = QPushButton("OK", self)
        ok_button.clicked.connect(self.accept)

        # Создаем компоновщик и добавляем на него виджет вкладок и кнопку "ОК"
        layout = QVBoxLayout(self)
        layout.addWidget(self.tabs)
        layout.addWidget(ok_button)

        # Загружаем значения из config для инициализации виджетов prefix_edit и token_edit
        self.prefix_edit.setText(self.config['prefix'])
        self.token_edit.setText(self.config['token'])

    # Создаем слот для обработки нажатия на кнопку "ОК"
    def save_prefix_and_token():
        # Получаем значения из виджетов
        prefix = self.prefix_edit.text()
        token = self.token_edit.text()

        # Сохраняем значения в config
        self.config['prefix'] = prefix
        self.config['token'] = token

        # Показываем диалоговое окно с сообщением об успешном сохранении
        QMessageBox.information(self, "Сохранение", "Префикс и токен сохранены успешно.")

    # Создаем слот для обработки нажатия на кнопку "ОК"
    def save_channels():
        # Получаем значения из виджетов
        welcome_channel_id = welcome_edit.text()
        goodbye_channel_id = goodbye_edit.text()
        audit_channel_id = audit_edit.text()
    
        # Сохраняем значения в config
        config['WelcomeChannel'] = welcome_channel_id
        config['GoodByeChannel'] = goodbye_channel_id
        config['AuditChannel'] = audit_channel_id

        # Показываем диалоговое окно с сообщением об успешном сохранении
        QMessageBox.information(self, "Сохранение", "Настройки каналов сохранены успешно.")

        ok_button.clicked.connect(save_prefix_and_token)
        ok_button.clicked.connect(save_channels)
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Создаем диалоговое окно настроек бота
    dialog = BotSettingsDialog()

    dialog.show_bot_settings()

    sys.exit(app.exec_())
