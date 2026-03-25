from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QTextEdit,
)


class AddProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Add Product')
        self.resize(420, 320)

        layout = QFormLayout(self)

        self.name_input = QLineEdit()
        self.symbol_input = QLineEdit()
        self.asset_type_input = QComboBox()
        self.asset_type_input.addItems(['Stock', 'ETF', 'Fund', 'Crypto', 'Bond', 'Commodity', 'Custom'])
        self.source_input = QLineEdit('manual')
        self.currency_input = QLineEdit('USD')
        self.note_input = QTextEdit()
        self.note_input.setFixedHeight(80)

        layout.addRow('Name', self.name_input)
        layout.addRow('Symbol', self.symbol_input)
        layout.addRow('Asset Type', self.asset_type_input)
        layout.addRow('Source', self.source_input)
        layout.addRow('Currency', self.currency_input)
        layout.addRow('Note', self.note_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_data(self):
        return {
            'name': self.name_input.text(),
            'symbol': self.symbol_input.text(),
            'asset_type': self.asset_type_input.currentText(),
            'source': self.source_input.text(),
            'currency': self.currency_input.text(),
            'note': self.note_input.toPlainText(),
        }
