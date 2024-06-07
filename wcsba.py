import sys
import csv
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QHBoxLayout, QMessageBox, QTabWidget, 
                             QComboBox, QInputDialog)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("West Coast Swing Broadcast App")
        self.setGeometry(100, 100, 400, 300)

        # Словарь для хранения переводов
        self.translations = {
            "Leader:": {"ru": "Лидер:", "en": "Leader:"},
            "Follower:": {"ru": "Партнер:", "en": "Follower:"},
            "Применить": {"ru": "Применить", "en": "Apply"},
            "Очистить": {"ru": "Очистить", "en": "Clear"},
            "Выход": {"ru": "Выход", "en": "Exit"},
            "Type:": {"ru": "Тип:", "en": "Type:"},
            "Division:": {"ru": "Дивизион:", "en": "Division:"},
            "Stage:": {"ru": "Этап:", "en": "Stage:"},
            "Выберите:": {"ru": "Выберите:", "en": "Select:"},
            "Редактировать Type": {"ru": "Редактировать Тип", "en": "Edit Type"},
            "Редактировать Division": {"ru": "Редактировать Дивизион", "en": "Edit Division"},
            "Редактировать Stage": {"ru": "Редактировать Этап", "en": "Edit Stage"},
            "Файл pro_show.txt не найден": {"ru": "Файл pro_show.txt не найден", "en": "File pro_show.txt not found"},
            "Edit Type": {"ru": "Редактировать Тип", "en": "Edit Type"},
            "Edit Division": {"ru": "Редактировать Дивизион", "en": "Edit Division"},
            "Edit Stage": {"ru": "Редактировать Этап", "en": "Edit Stage"},
            "Enter Type items separated by commas:": {"ru": "Введите элементы Типа, разделенные запятыми:", "en": "Enter Type items separated by commas:"},
            "Enter Division items separated by commas:": {"ru": "Введите элементы Дивизиона, разделенные запятыми:", "en": "Enter Division items separated by commas:"},
            "Enter Stage items separated by commas:": {"ru": "Введите элементы Этапа, разделенные запятыми:", "en": "Enter Stage items separated by commas:"},
            "Введите номер участника": {"ru": "Введите номер участника", "en": "Enter participant number"},
            "Номер участника должен состоять только из цифр": {"ru": "Номер участника должен состоять только из цифр", "en": "Participant number should consist only of digits"},
            "Введите номер участника в поле Leader": {"ru": "Введите номер участника в поле Лидер", "en": "Enter participant number in Leader field"},
            "Введите номер участника в поле Follower": {"ru": "Введите номер участника в поле Партнер", "en": "Enter participant number in Follower field"},
            "Некорректные номера": {"ru": "Некорректные номера", "en": "Invalid numbers"},
            "Файл Data.csv не найден": {"ru": "Файл Data.csv не найден", "en": "File Data.csv not found"},
            "Произошла ошибка при чтении или записи файла:": {"ru": "Произошла ошибка при чтении или записи файла:", "en": "An error occurred while reading or writing the file:"},
            "На танцполе сейчас": {"ru": "На танцполе сейчас", "en": "On the dance floor now"},
            "Файл теперь пустой": {"ru": "Файл теперь пустой", "en": "File is now empty"},
            "Произошла ошибка при очистке файла:": {"ru": "Произошла ошибка при очистке файла:", "en": "An error occurred while clearing the file:"},
            "Сообщение": {"ru": "Сообщение", "en": "Message"}
        }

        # Установка перевода по умолчанию
        self.current_language = "en"

        self.setup_tabs()

        # Основной макет
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab_widget)
        self.setLayout(main_layout)

    def setup_tabs(self):
        # Добавляем вкладки
        self.tab_widget = QTabWidget()
        self.tab_main = QWidget()
        self.tab_competitions = QWidget()
        self.tab_pro_show = QWidget()
        self.tab_custom_options = QWidget()

        self.tab_widget.addTab(self.tab_main, self.translate("Main"))
        self.setup_main_tab()

        self.tab_widget.addTab(self.tab_competitions, self.translate("Competitions"))
        self.setup_competitions_tab()

        self.tab_widget.addTab(self.tab_pro_show, self.translate("Pro Show"))
        self.setup_pro_show_tab()

        self.tab_widget.addTab(self.tab_custom_options, self.translate("Custom options"))
        self.setup_custom_options_tab()

    def setup_main_tab(self):
        layout = QVBoxLayout()

        # Поля ввода и метки
        layout.addWidget(QLabel(self.translate("Leader:")))
        self.entry1 = QLineEdit()
        layout.addWidget(self.entry1)

        layout.addWidget(QLabel(self.translate("Follower:")))
        self.entry2 = QLineEdit()
        layout.addWidget(self.entry2)

        # Кнопки
        self.apply_button = QPushButton(self.translate("Применить"))
        self.apply_button.clicked.connect(self.apply_changes)

        self.clear_button = QPushButton(self.translate("Очистить"))
        self.clear_button.clicked.connect(self.clear_file)

        self.exit_button = QPushButton(self.translate("Выход"))
        self.exit_button.clicked.connect(self.exit_application)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.apply_button)
        buttons_layout.addWidget(self.clear_button)
        buttons_layout.addWidget(self.exit_button)

        layout.addLayout(buttons_layout)
        self.tab_main.setLayout(layout)

#test blahblah 1212121

    def setup_competitions_tab(self):
        layout = QVBoxLayout()

        # Выпадающие списки
        layout.addWidget(QLabel(self.translate("Type:")))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["", "Jack&Jill", "Strictly"])
        layout.addWidget(self.type_combo)

        layout.addWidget(QLabel(self.translate("Division:")))
        self.division_combo = QComboBox()
        self.division_combo.addItems(["", "Sophisticated", "Newcomer", "Novice", "Intermediate", "Advanced", "All-Stars", "Champions"])
        layout.addWidget(self.division_combo)

        layout.addWidget(QLabel(self.translate("Stage:")))
        self.stage_combo = QComboBox()
        self.stage_combo.addItems(["", "All Skate", "Prelims 1/16", "Prelims 1/8", "Prelims 1/4", "Prelims 1/2", "Finals"])
        layout.addWidget(self.stage_combo)

        # Кнопки
        self.apply_comp_button = QPushButton(self.translate("Применить"))
        self.apply_comp_button.clicked.connect(self.apply_competition_changes)

        self.clear_comp_button = QPushButton(self.translate("Очистить"))
        self.clear_comp_button.clicked.connect(self.clear_file)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.apply_comp_button)
        buttons_layout.addWidget(self.clear_comp_button)

        layout.addLayout(buttons_layout)
        self.tab_competitions.setLayout(layout)

    def setup_pro_show_tab(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel(self.translate("Выберите:")))
        self.pro_show_combo = QComboBox()
        self.update_pro_show_combo()
        layout.addWidget(self.pro_show_combo)

        self.apply_pro_show_button = QPushButton(self.translate("Применить"))
        self.apply_pro_show_button.clicked.connect(self.apply_pro_show_changes)

        self.clear_pro_show_button = QPushButton(self.translate("Очистить"))
        self.clear_pro_show_button.clicked.connect(self.clear_file)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.apply_pro_show_button)
        buttons_layout.addWidget(self.clear_pro_show_button)

        layout.addLayout(buttons_layout)
        self.tab_pro_show.setLayout(layout)

    def setup_custom_options_tab(self):
        layout = QVBoxLayout()

        self.language_label = QLabel(self.translate("Выберите язык:"))
        layout.addWidget(self.language_label)

        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "Русский"])
        self.language_combo.currentIndexChanged.connect(self.change_language)
        layout.addWidget(self.language_combo)

        self.edit_type_button = QPushButton(self.translate("Редактировать Type"))
        self.edit_type_button.clicked.connect(lambda: self.edit_list(self.type_combo, "Type"))
        layout.addWidget(self.edit_type_button)

        self.edit_division_button = QPushButton(self.translate("Редактировать Division"))
        self.edit_division_button.clicked.connect(lambda: self.edit_list(self.division_combo, "Division"))
        layout.addWidget(self.edit_division_button)

        self.edit_stage_button = QPushButton(self.translate("Редактировать Stage"))
        self.edit_stage_button.clicked.connect(lambda: self.edit_list(self.stage_combo, "Stage"))
        layout.addWidget(self.edit_stage_button)

        self.tab_custom_options.setLayout(layout)

    def update_pro_show_combo(self):
        try:
            with open('pro_show.txt', 'r') as file:
                lines = file.readlines()
                self.pro_show_combo.clear()
                self.pro_show_combo.addItems([line.strip() for line in lines])
        except FileNotFoundError:
            self.show_message(self.translate("Файл pro_show.txt не найден"))

    def edit_list(self, combo, title):
        items = [combo.itemText(i) for i in range(combo.count())]
        text, ok = QInputDialog.getText(self, f"{self.translate('Edit')} {title}", f"{self.translate('Enter')} {title} {self.translate('items separated by commas')}:",
                                        text=", ".join(items))
        if ok and text:
            combo.clear()
            combo.addItems([item.strip() for item in text.split(",")])

    def apply_changes(self):
        value1 = self.entry1.text()
        value2 = self.entry2.text()

        if not value1 and not value2:
            self.show_message(self.translate("Введите номер участника"))
            return

        if not self.validate_participant_numbers(value1) or not self.validate_participant_numbers(value2):
            self.show_message(self.translate("Номер участника должен состоять только из цифр"))
            return

        if not value1:
            self.show_message(self.translate("Введите номер участника в поле Leader"))
            return

        if not value2:
            self.show_message(self.translate("Введите номер участника в поле Follower"))
            return

        try:
            data1, data2, found1, found2 = "", "", False, False

            with open('Data.csv', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row and row[0] == value1:
                        data1 = row[1]
                        found1 = True
                    elif row and row[0] == value2:
                        data2 = row[1]
                        found2 = True

            if not found1 or not found2:
                self.show_message(self.translate("Некорректные номера"))
            else:
                with open('output.txt', 'w') as output_file:
                    output_file.write(f"{data1} - {data2}")
                self.show_message(f"{self.translate('На танцполе сейчас')} {data1} - {data2}")
        except FileNotFoundError:
            self.show_message(self.translate("Файл Data.csv не найден"))
        except Exception as e:
            self.show_message(f"{self.translate('Произошла ошибка при чтении или записи файла')}: {e}")

    def validate_participant_numbers(self, number):
        return number.isdigit()

    def apply_competition_changes(self):
        type_selected = self.type_combo.currentText()
        division_selected = self.division_combo.currentText()
        stage_selected = self.stage_combo.currentText()

        components = [type_selected, division_selected, stage_selected]
        result = " ".join([comp for comp in components if comp])

        try:
            with open('output.txt', 'w') as output_file:
                output_file.write(result)
            self.show_message(f"{self.translate('На танцполе сейчас')} {result}")
        except Exception as e:
            self.show_message(f"{self.translate('Произошла ошибка при записи файла')}: {e}")

    def apply_pro_show_changes(self):
        pro_show_selected = self.pro_show_combo.currentText()

        try:
            with open('output.txt', 'w') as output_file:
                output_file.write(pro_show_selected)
            self.show_message(f"{self.translate('На танцполе сейчас')} {pro_show_selected}")
        except Exception as e:
            self.show_message(f"{self.translate('Произошла ошибка при записи файла')}: {e}")

    def clear_file(self):
        try:
            with open('output.txt', 'w') as output_file:
                output_file.write("")
            self.show_message(self.translate("Файл теперь пустой"))
        except Exception as e:
            self.show_message(f"{self.translate('Произошла ошибка при очистке файла')}: {e}")

    def exit_application(self):
        QApplication.quit()

    def show_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information if "успешно" in message.lower() or "пустой" in message.lower() else QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle(self.translate("Сообщение"))
        msg.exec_()

    def translate(self, text):
        # Получаем перевод для текста на текущем языке, если перевод не найден, возвращаем исходный текст
        return self.translations.get(text, {}).get(self.current_language, text)

    def change_language(self, index):
        # Изменяем текущий язык в соответствии с выбранным индексом в выпадающем списке
        if index == 0:
            self.current_language = "en"
        else:
            self.current_language = "ru"
        # Переводим все текстовые элементы в соответствии с новым языком
        self.translate_ui()

    def translate_ui(self):
        # Переводим все текстовые элементы интерфейса
        self.setWindowTitle(self.translate("West Coast Swing Broadcast App"))
        self.tab_widget.setTabText(0, self.translate("Main"))
        self.tab_widget.setTabText(1, self.translate("Competitions"))
        self.tab_widget.setTabText(2, self.translate("Pro Show"))
        self.tab_widget.setTabText(3, self.translate("Custom options"))
        self.language_label.setText(self.translate("Выберите язык:"))
        self.edit_type_button.setText(self.translate("Редактировать Type"))
        self.edit_division_button.setText(self.translate("Редактировать Division"))
        self.edit_stage_button.setText(self.translate("Редактировать Stage"))
        self.apply_button.setText(self.translate("Применить"))
        self.clear_button.setText(self.translate("Очистить"))
        self.exit_button.setText(self.translate("Выход"))
        self.apply_comp_button.setText(self.translate("Применить"))
        self.clear_comp_button.setText(self.translate("Очистить"))
        self.apply_pro_show_button.setText(self.translate("Применить"))
        self.clear_pro_show_button.setText(self.translate("Очистить"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
