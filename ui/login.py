from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton,
                               QDialog, QMessageBox, QApplication)
from PySide6.QtCore import Signal, Qt
from core import auth


class SignupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create customer account")
        self.name = QLineEdit()
        self.phone = QLineEdit()
        self.email = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        form = QFormLayout()
        form.addRow("Full name", self.name)
        form.addRow("Phone", self.phone)
        form.addRow("Email", self.email)
        form.addRow("Password", self.password)
        btn = QPushButton("Create account")
        btn.clicked.connect(self.submit)
        lay = QVBoxLayout(self)
        lay.addLayout(form)
        lay.addWidget(btn)

    def submit(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            auth.signup_customer(self.email.text(), self.password.text(),
                                 self.name.text(), self.phone.text())
        except auth.AuthError as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, "Signup", str(e))
            return
        QApplication.restoreOverrideCursor()
        QMessageBox.information(self, "Signup", "Account created. You can log in now.")
        self.accept()


class LoginWindow(QWidget):
    logged_in = Signal(dict)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SS STEEL SOLUTIONS - Login")
        self.setFixedWidth(380)

        title = QLabel("SS STEEL SOLUTIONS")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold; padding: 10px;")
        sub = QLabel("Iron & Steel Management System")
        sub.setAlignment(Qt.AlignCenter)

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.returnPressed.connect(self.do_login)
        self.error = QLabel("")
        self.error.setStyleSheet("color: #c0392b;")
        self.error.setWordWrap(True)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.do_login)
        signup_btn = QPushButton("Create customer account")
        signup_btn.clicked.connect(lambda: SignupDialog(self).exec())

        lay = QVBoxLayout(self)
        for w in (title, sub, self.email, self.password, self.error, login_btn, signup_btn):
            lay.addWidget(w)

    def reset(self):
        self.password.clear()
        self.error.setText("")

    def do_login(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            user = auth.login(self.email.text(), self.password.text())
        except auth.AuthError as e:
            QApplication.restoreOverrideCursor()
            self.error.setText(str(e))
            return
        QApplication.restoreOverrideCursor()
        self.reset()
        self.logged_in.emit(user)
