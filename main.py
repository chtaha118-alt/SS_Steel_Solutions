import sys
from PySide6.QtWidgets import QApplication
from core import auth
from ui.login import LoginWindow
from ui.admin_window import AdminWindow
from ui.customer_window import CustomerWindow


class AppController:
    def __init__(self):
        self.main = None
        self.login = LoginWindow()
        self.login.logged_in.connect(self.open_main)

    def start(self):
        self.login.show()

    def open_main(self, user):
        self.login.hide()
        if user["role"] in ("admin", "staff"):
            self.main = AdminWindow(user)
        else:
            self.main = CustomerWindow(user)
        self.main.logout_requested.connect(self.on_logout)
        self.main.show()

    def on_logout(self):
        auth.logout()
        self.login.show()          # show login first so the app never has zero windows
        self.main.close()
        self.main = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = AppController()
    controller.start()
    sys.exit(app.exec())
