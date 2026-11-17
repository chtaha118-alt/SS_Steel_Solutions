"""Product / stock table. Admin gets an 'Add product' form, customers see read-only."""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
                               QHeaderView, QPushButton, QGroupBox, QFormLayout, QLineEdit,
                               QComboBox, QDoubleSpinBox, QSpinBox, QMessageBox, QAbstractItemView)
from PySide6.QtCore import Qt
from core import stock

COLUMNS = [("id", "ID"), ("name", "Name"), ("category", "Category"), ("size_label", "Size"),
           ("grade", "Grade"), ("price_per_kg", "Price / kg"), ("stock_pieces", "Pieces"),
           ("stock_kg", "Stock (kg)")]


class ProductsTab(QWidget):
    def __init__(self, can_edit=False):
        super().__init__()
        self.table = QTableWidget(0, len(COLUMNS))
        self.table.setHorizontalHeaderLabels([c[1] for c in COLUMNS])
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        refresh = QPushButton("Refresh")
        refresh.clicked.connect(self.refresh)

        layout = QVBoxLayout(self)
        bar = QHBoxLayout()
        bar.addStretch()
        bar.addWidget(refresh)
        layout.addLayout(bar)
        layout.addWidget(self.table)

        if can_edit:
            layout.addWidget(self.build_add_form())
        self.refresh()

    def build_add_form(self):
        box = QGroupBox("Add product")
        form = QFormLayout(box)
        self.f_name = QLineEdit()
        self.f_cat = QComboBox()
        self.f_cat.addItems(stock.CATEGORIES)
        self.f_size = QLineEdit()
        self.f_grade = QLineEdit()
        self.f_price = QDoubleSpinBox()
        self.f_price.setRange(0, 10_000_000)
        self.f_pieces = QSpinBox()
        self.f_pieces.setRange(0, 10_000_000)
        self.f_kg = QDoubleSpinBox()
        self.f_kg.setRange(0, 100_000_000)
        self.f_kg.setDecimals(3)
        for label, w in [("Name", self.f_name), ("Category", self.f_cat), ("Size", self.f_size),
                         ("Grade", self.f_grade), ("Price per kg", self.f_price),
                         ("Pieces in stock", self.f_pieces), ("Stock (kg)", self.f_kg)]:
            form.addRow(label, w)
        add = QPushButton("Add product")
        add.clicked.connect(self.add_product)
        form.addRow(add)
        return box

    def refresh(self):
        try:
            rows = stock.list_products()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not load products:\n{e}")
            return
        self.table.setRowCount(len(rows))
        for r, p in enumerate(rows):
            for c, (key, _) in enumerate(COLUMNS):
                value = p.get(key)
                item = QTableWidgetItem("" if value is None else str(value))
                if key in ("price_per_kg", "stock_pieces", "stock_kg"):
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table.setItem(r, c, item)

    def add_product(self):
        try:
            stock.add_product(self.f_name.text(), self.f_cat.currentText(), self.f_size.text(),
                              self.f_grade.text(), self.f_price.value(),
                              self.f_pieces.value(), self.f_kg.value())
        except Exception as e:
            QMessageBox.warning(self, "Could not add product", str(e))
            return
        self.f_name.clear()
        self.f_size.clear()
        self.f_grade.clear()
        self.refresh()
