from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTabWidget
from PySide6.QtCore import Signal
from ui.products_tab import ProductsTab
from ui.calculator_widget import CalculatorWidget


class AdminWindow(QMainWindow):
    logout_requested = Signal()

    def __init__(self, user):
        super().__init__()
        self.setWindowTitle("SS STEEL SOLUTIONS - Admin Panel")
        self.resize(1000, 700)

        title = QLabel("SS STEEL SOLUTIONS")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        who = QLabel(f"{user['full_name']}  ({user['role']})")
        out = QPushButton("Logout")
        out.clicked.connect(self.logout_requested.emit)

        header = QHBoxLayout()
        header.addWidget(title)
        header.addStretch()
        header.addWidget(who)
        header.addWidget(out)

        tabs = QTabWidget()
        tabs.addTab(ProductsTab(can_edit=True), "Stock")
        tabs.addTab(CalculatorWidget(), "Weight Calculator")
        # Next steps: Inward, Cutting, Ledger, Reports

        root = QWidget()
        lay = QVBoxLayout(root)
        lay.addLayout(header)
        lay.addWidget(tabs)
        self.setCentralWidget(root)
