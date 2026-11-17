"""Weight calculator tab, shared by Admin and Customer windows."""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QComboBox,
                               QDoubleSpinBox, QSpinBox, QLabel, QPushButton)
from core.weight_calculator import calculate

# steel type -> (display name, [(parameter, label, unit)])
TYPES = {
    "plate": ("Plate / Sheet", [("length_mm", "Length", "mm"), ("width_mm", "Width", "mm"),
                                ("thickness_mm", "Thickness", "mm")]),
    "round_bar": ("Round bar", [("diameter_mm", "Diameter", "mm"), ("length_m", "Length", "m")]),
    "rebar": ("Rebar", [("diameter_mm", "Diameter", "mm"), ("length_m", "Length", "m")]),
    "square_bar": ("Square bar", [("side_mm", "Side", "mm"), ("length_m", "Length", "m")]),
    "flat_bar": ("Flat bar", [("width_mm", "Width", "mm"), ("thickness_mm", "Thickness", "mm"),
                              ("length_m", "Length", "m")]),
    "pipe": ("Pipe", [("outer_diameter_mm", "Outer diameter", "mm"),
                      ("wall_thickness_mm", "Wall thickness", "mm"), ("length_m", "Length", "m")]),
    "angle": ("Angle", [("leg1_mm", "Leg 1", "mm"), ("leg2_mm", "Leg 2", "mm"),
                        ("thickness_mm", "Thickness", "mm"), ("length_m", "Length", "m")]),
    "beam": ("Beam / Channel", [("kg_per_metre", "Weight per metre", "kg/m"), ("length_m", "Length", "m")]),
}


class CalculatorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.inputs = {}

        self.type_box = QComboBox()
        for key, (label, _) in TYPES.items():
            self.type_box.addItem(label, key)
        self.type_box.currentIndexChanged.connect(self.build_fields)

        self.form = QFormLayout()
        self.qty = QSpinBox()
        self.qty.setRange(1, 1_000_000)
        self.price = QDoubleSpinBox()
        self.price.setRange(0, 10_000_000)
        self.price.setDecimals(2)
        self.price.setPrefix("Rs ")
        self.price.setSuffix(" / kg")

        btn = QPushButton("Calculate")
        btn.clicked.connect(self.run)
        self.result = QLabel("")
        self.result.setWordWrap(True)
        self.result.setStyleSheet("font-size: 15px; padding: 8px;")

        top = QFormLayout()
        top.addRow("Steel type", self.type_box)
        layout = QVBoxLayout(self)
        layout.addLayout(top)
        layout.addLayout(self.form)
        bottom = QFormLayout()
        bottom.addRow("Quantity (pieces)", self.qty)
        bottom.addRow("Price (optional)", self.price)
        layout.addLayout(bottom)
        layout.addWidget(btn)
        layout.addWidget(self.result)
        layout.addStretch()
        self.build_fields()

    def build_fields(self):
        while self.form.rowCount():
            self.form.removeRow(0)
        self.inputs = {}
        key = self.type_box.currentData()
        for param, label, unit in TYPES[key][1]:
            box = QDoubleSpinBox()
            box.setRange(0, 1_000_000)
            box.setDecimals(3)
            box.setSuffix(f" {unit}")
            self.inputs[param] = box
            self.form.addRow(label, box)
        self.result.setText("")

    def run(self):
        key = self.type_box.currentData()
        dims = {p: b.value() for p, b in self.inputs.items()}
        try:
            one = calculate(key, **dims)
            total = calculate(key, qty=self.qty.value(), **dims)
        except ValueError as e:
            self.result.setStyleSheet("font-size: 15px; padding: 8px; color: #c0392b;")
            self.result.setText(f"Check your values: {e}")
            return
        self.result.setStyleSheet("font-size: 15px; padding: 8px;")
        text = (f"Weight per piece: {one:,.3f} kg\n"
                f"Total weight: {total:,.3f} kg  ({total / 1000:,.3f} tons)")
        if self.price.value() > 0:
            text += f"\nEstimated cost: Rs {total * self.price.value():,.2f}"
        self.result.setText(text)
