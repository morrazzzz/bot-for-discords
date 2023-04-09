from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTabWidget, QWidget
import sys
from Configs.BotSettings import config

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
        channels_tab.layout().addWidget(QLabel("Здесь находятся настройки каналов"))

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

    def show_bot_settings(self):
        # Используем значения атрибутов класса для настроек
        self.prefix_edit.setText(self.config['prefix'])
        self.token_edit.setText(self.config['token'])

        result = self.exec_()

        if result == QDialog.Accepted:
            # Сохраняем значения токена и префикса из виджетов в атрибуты класса
            self.config['prefix'] = self.prefix_edit.text()
            self.config['token'] = self.token_edit.text()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Создаем диалоговое окно настроек бота
    dialog = BotSettingsDialog()

    dialog.show_bot_settings()

    sys.exit(app.exec_())
