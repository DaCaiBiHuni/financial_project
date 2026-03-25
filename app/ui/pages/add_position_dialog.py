from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
)


class AddPositionDialog(QDialog):
    def __init__(self, products, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Add Position')
        self.resize(420, 220)

        layout = QFormLayout(self)

        self.product_input = QComboBox()
        self.product_map = {}
        for product in products:
            label = f"{product.name} ({product.symbol})"
            self.product_input.addItem(label)
            self.product_map[label] = product.id

        self.quantity_input = QDoubleSpinBox()
        self.quantity_input.setMaximum(1_000_000_000)
        self.quantity_input.setDecimals(4)

        self.cost_input = QDoubleSpinBox()
        self.cost_input.setMaximum(1_000_000_000)
        self.cost_input.setDecimals(4)

        layout.addRow('Product', self.product_input)
        layout.addRow('Quantity', self.quantity_input)
        layout.addRow('Average Cost', self.cost_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_data(self):
        label = self.product_input.currentText()
        return {
            'product_id': self.product_map[label],
            'quantity': self.quantity_input.value(),
            'average_cost': self.cost_input.value(),
        }
