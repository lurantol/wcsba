import sys
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QTabWidget, QComboBox, QInputDialog

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Пример интерфейса")
        self.setGeometry(100, 100, 400, 300)

        # Создаем виджет вкладок
        self.tab_widget = QTabWidget()

        # Вкладка "Main"
        self.tab_main = QWidget()
        self.tab_widget.addTab(self.tab_main, "Main")
        self.setup_main_tab()

        # Вкладка "Competitions"
        self.tab_competitions = QWidget()
        self.tab_widget.addTab(self.tab_competitions, "Competitions")
        self.setup_competitions_tab()

        # Вкладка "Pro Show"
        self.tab_pro_show = QWidget()
        self.tab_widget.addTab(self.tab_pro_show, "Pro Show")
        self.setup_pro_show_tab()

        # Вкладка "Custom options"
        self.tab_custom_options = QWidget()
        self.tab_widget.addTab(self.tab_custom_options, "Custom options")
        self.setup_custom_options_tab()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab_widget)
        self.setLayout(main_layout)

    def setup_main_tab(self):
        layout = QVBoxLayout()

        label1 = QLabel("Leader:")
        layout.addWidget(label1)

        self.entry1 = QLineEdit()
        layout.addWidget(self.entry1)

        label2 = QLabel("Follower:")
        layout.addWidget(label2)

        self.entry2 = QLineEdit()
        layout.addWidget(self.entry2)

        self.apply_button = QPushButton("Применить")
        self.apply_button.clicked.connect(self.apply_changes)

        self.clear_button = QPushButton("Очистить")
        self.clear_button.clicked.connect(self.clear_file)

        self.exit_button = QPushButton("Выход")
        self.exit_button.clicked.connect(self.exit_application)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.apply_button)
        buttons_layout.addWidget(self.clear_button)
        buttons_layout.addWidget(self.exit_button)

        layout.addLayout(buttons_layout)
        self.tab_main.setLayout(layout)

    def setup_competitions_tab(self):
        layout = QVBoxLayout()

        # Выпадающий список Type
        label_type = QLabel("Type:")
        layout.addWidget(label_type)

        self.type_combo = QComboBox()
        self.type_combo.addItem("")  # Пустое значение по умолчанию
        self.type_combo.addItems(["Jack&Jill", "Strictly"])
        self.type_combo.currentIndexChanged.connect(self.update_division_stage_availability)
        layout.addWidget(self.type_combo)

        # Выпадающий список Division
        label_division = QLabel("Division:")
        layout.addWidget(label_division)

        self.division_combo = QComboBox()
        self.division_combo.addItem("")  # Пустое значение по умолчанию
        self.division_combo.addItems(["Sophisticated", "Newcomer", "Novice", "Intermediate", "Advanced", "All-Stars", "Champions"])
        layout.addWidget(self.division_combo)

        # Выпадающий список Stage
        label_stage = QLabel("Stage:")
        layout.addWidget(label_stage)

        self.stage_combo = QComboBox()
        self.stage_combo.addItem("")
        self.stage_combo.addItems(["All Skate", "Prelims 1/16", "Prelims 1/8", "Prelims 1/4", "Prelims 1/2", "Finals"])
        layout.addWidget(self.stage_combo)

        # Кнопки Применить и Очистить
        self.apply_comp_button = QPushButton("Применить")
        self.apply_comp_button.clicked.connect(self.apply_competition_changes)

        self.clear_comp_button = QPushButton("Очистить")
        self.clear_comp_button.clicked.connect(self.clear_file)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.apply_comp_button)
        buttons_layout.addWidget(self.clear_comp_button)

        layout.addLayout(buttons_layout)
        self.tab_competitions.setLayout(layout)

        # Изначально делаем списки Division и Stage недоступными
        self.division_combo.setEnabled(False)
        self.stage_combo.setEnabled(False)

    def setup_pro_show_tab(self):
        layout = QVBoxLayout()

        # Выпадающий список для Pro Show
        label_pro_show = QLabel("Выберите:")
        layout.addWidget(label_pro_show)

        self.pro_show_combo = QComboBox()
        self.update_pro_show_combo()
        layout.addWidget(self.pro_show_combo)

        # Кнопки Применить и Очистить
        self.apply_pro_show_button = QPushButton("Применить")
        self.apply_pro_show_button.clicked.connect(self.apply_pro_show_changes)

        self.clear_pro_show_button = QPushButton("Очистить")
        self.clear_pro_show_button.clicked.connect(self.clear_file)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.apply_pro_show_button)
        buttons_layout.addWidget(self.clear_pro_show_button)

        layout.addLayout(buttons_layout)
        self.tab_pro_show.setLayout(layout)

    def setup_custom_options_tab(self):
        layout = QVBoxLayout()

        # Редактирование списка Type
        self.edit_type_button = QPushButton("Редактировать Type")
        self.edit_type_button.clicked.connect(lambda: self.edit_list(self.type_combo, "Type"))
        layout.addWidget(self.edit_type_button)

        # Редактирование списка Division
        self.edit_division_button = QPushButton("Редактировать Division")
        self.edit_division_button.clicked.connect(lambda: self.edit_list(self.division_combo, "Division"))
        layout.addWidget(self.edit_division_button)

        # Редактирование списка Stage
        self.edit_stage_button = QPushButton("Редактировать Stage")
        self.edit_stage_button.clicked.connect(lambda:            self.edit_list(self.stage_combo, "Stage"))
        layout.addWidget(self.edit_stage_button)

        self.tab_custom_options.setLayout(layout)

    def update_pro_show_combo(self):
        try:
            with open('pro_show.txt', 'r') as file:
                lines = file.readlines()
                self.pro_show_combo.clear()
                self.pro_show_combo.addItems([line.strip() for line in lines])
        except FileNotFoundError:
            self.show_message("Файл pro_show.txt не найден")

    def update_division_stage_availability(self):
        type_selected = self.type_combo.currentText()
        division_enabled = bool(type_selected)
        stage_enabled = bool(type_selected) and (division_enabled or bool(self.division_combo.currentText()))

        self.division_combo.setEnabled(division_enabled)
        self.stage_combo.setEnabled(stage_enabled)

    def edit_list(self, combo, title):
        items = [combo.itemText(i) for i in range(combo.count())]
        text, ok = QInputDialog.getText(self, f"Edit {title}", f"Enter {title} items separated by commas:", text=", ".join(items))
        if ok and text:
            combo.clear()
            combo.addItems([item.strip() for item in text.split(",")])

    def apply_changes(self):
        value1 = self.entry1.text()
        value2 = self.entry2.text()

        # Проверка на пустые поля
        if not value1 and not value2:
            self.show_message("Введите номер участника")
            return
        
        # Валидация номеров участников
        if not self.validate_participant_numbers(value1) or not self.validate_participant_numbers(value2):
            self.show_message("Номер участника должен состоять только из цифр")
            return
        
        # Проверка на пустое поле 1
        if not value1:
            self.show_message("Введите номер участника в поле Leader")
            return
        
        # Проверка на пустое поле 2
        if not value2:
            self.show_message("Введите номер участника в поле Follower")
            return
        
        # Переменные для отслеживания наличия совпадений
        found1 = False
        found2 = False
        data1 = ""
        data2 = ""
        
        # Чтение данных из файла Data.csv и запись соответствующих данных в output.txt
        try:
            with open('Data.csv', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row and row[0] == value1:
                        data1 = row[1]
                        found1 = True
                    elif row and row[0] == value2:
                        data2 = row[1]
                        found2 = True

            # Проверяем, найдены ли оба значения
            if not found1 or not found2:
                self.show_message("Некорректные номера")
            else:
                with open('output.txt', 'w') as output_file:
                    output_file.write(f"{data1} - {data2}")
                self.show_message(f"На танцполе сейчас {data1} - {data2}")
        except FileNotFoundError:
            self.show_message("Файл Data.csv не найден")
        except Exception as e:
            self.show_message(f"Произошла ошибка при чтении или записи файла: {e}")

    def validate_participant_numbers(self, number):
        return number.isdigit()

    def apply_competition_changes(self):
        type_selected = self.type_combo.currentText()
        division_selected = self.division_combo.currentText()
        stage_selected = self.stage_combo.currentText()
        
        try:
            with open('output.txt', 'w') as output_file:
                output_file.write(f"{type_selected} {division_selected} {stage_selected}")
            with open('output.txt', 'r') as output_file:
                data = output_file.read()
            self.show_message(f"На танцполе сейчас {data}")
        except Exception as e:
            self.show_message(f"Произошла ошибка при записи файла: {e}")
    
    def apply_pro_show_changes(self):
        pro_show_selected = self.pro_show_combo.currentText()
        
        try:
            with open('output.txt', 'w') as output_file:
                output_file.write(pro_show_selected)
            with open('output.txt', 'r') as output_file:
                data = output_file.read()
            self.show_message(f"На танцполе сейчас {data}")
        except Exception as e:
            self.show_message(f"Произошла ошибка при записи файла: {e}")

    def clear_file(self):
        try:
            with open('output.txt', 'w') as output_file:
                output_file.write("")
            self.show_message("Файл теперь пустой")
        except Exception as e:
            self.show_message(f"Произошла ошибка при очистке файла: {e}")
    
    def exit_application(self):
        QApplication.quit()
        
    def show_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information if "успешно" in message.lower() or "пустой" in message.lower() else QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle("Сообщение")
        msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

