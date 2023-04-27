import flask
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QVBoxLayout
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QInputDialog
import untitled, datetime
import requests


class Messenger(untitled.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.sender.pressed.connect(self.send_message)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_message)
        self.timer.start(1000)
        self.after = 0
        self.serv = ""
        self.action.triggered.connect(self.showDialog)

    def showDialog(self):

        text, ok = QInputDialog.getText(self, 'Input Dialog',
                                        'Enter server host:')

        if ok:
            self.serv = str(text)

    def print_message(self, message):
        t = message['time']
        dt = datetime.datetime.fromtimestamp(t)
        dt = dt.strftime('%H:%M:%S')
        self.textBrowser.append(dt + " " + message['name'])
        self.textBrowser.append(message['text'])
        self.textBrowser.append("")

    def get_message(self):
        try:
            response = requests.get(f"{self.serv}/messages", params={'after': self.after})
            messages = response.json()['messages']
            for message in messages:
                self.print_message(message)
                self.after = message['time']
        except:
            return

    def send_message(self):
        name = self.lineEdit.text()
        text = self.textEdit.toPlainText()
        try:
            response = requests.post(f'{self.serv}/send', json={
                'name': name,
                'text': text})
        except:
            self.textBrowser.append('Сервер недоступен')
            self.textBrowser.append("")
            return

        if response.status_code != 200:
            self.textBrowser.append("Проверьте имя и текст")
            self.textBrowser.append("")

        self.textEdit.setText("")


class LoginRegisterWindow(QWidget):
    def __init__(self, servip):
        super().__init__()
        self.serverip = servip

        self.initUI()

    def initUI(self):
        self.username_label = QLabel("Имя пользователя")
        self.username_edit = QLineEdit()
        self.password_label = QLabel("Пароль")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Войти")
        self.register_button = QPushButton("Зарегистрироваться")
        self.logged = False

        vbox = QVBoxLayout()
        vbox.addWidget(self.username_label)
        vbox.addWidget(self.username_edit)
        vbox.addWidget(self.password_label)
        vbox.addWidget(self.password_edit)
        vbox.addWidget(self.login_button)
        vbox.addWidget(self.register_button)
        self.setLayout(vbox)

        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)

    def login(self):
        try:
            username = self.username_edit.text()
            password = self.password_edit.text()
            response = requests.post(f'{self.serverip}/login', json={
                'login': username,
                'pass': password})
            print(response.json())
            # проверка имени пользователя и пароля
            if response.json()["ok"]:
                print("Вход выполнен успешно")
                self.logged = True
                self.close()
            else:
                print("Неверное имя пользователя или пароль")
        except Exception as a:
            print(a)

    def register(self):
        try:
            username = self.username_edit.text()
            password = self.password_edit.text()
            if username != "" and password != "":
                print("вы зарегестрированы")
                response = requests.post(f'{self.serverip}/register', json={
                    'login': username,
                    'pass': password})
                print(response.json())
                self.logged = True
                self.close()
            else:
                print("Ошибка")
        except Exception as s:
            print(s)


fl = True
app1 = QApplication(sys.argv)

while fl:
    a = input("Введите адрес сервера:")
    try:
        response = requests.get(a)
        fl = False
    except:
        fl = True
login_register_window = LoginRegisterWindow(a)
login_register_window.show()
app1.exec()
if login_register_window.logged:
    app = QtWidgets.QApplication([])
    window = Messenger()
    window.show()
    app.exec()
