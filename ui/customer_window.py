from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTabWidget
from PySide6.QtCore import Signal
from ui.products_tab import ProductsTab
from ui.calculator_widget import CalculatorWidget


class CustomerWindow(QMainWindow):
    logout_requested = Signal()

    def __init__(self, user):
        super().__init__()
        self.setWindowTitle("SS STEEL SOLUTIONS - Customer Portal")
        self.resize(900, 650)

        title = QLabel("SS STEEL SOLUTIONS")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        who = QLabel(user["full_name"])
        out = QPushButton("Logout")
        out.clicked.connect(self.logout_requested.emit)

        header = QHBoxLayout()
        header.addWidget(title)
        header.addStretch()
        header.addWidget(who)
        header.addWidget(out)

        tabs = QTabWidget()
        tabs.addTab(ProductsTab(can_edit=False), "Catalog")
        tabs.addTab(CalculatorWidget(), "Weight Calculator")
        # Next step: My Orders

        root = QWidget()
        lay = QVBoxLayout(root)
        lay.addLayout(header)
        lay.addWidget(tabs)
        self.setCentralWidget(root)
