from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.application.services.product_service import ProductService


RECOMMENDED_PRODUCTS = [
    {'name': 'NVIDIA Corporation', 'symbol': 'NVDA', 'asset_type': 'Stock', 'source': 'manual', 'currency': 'USD', 'note': 'Recommended'},
    {'name': 'Apple Inc.', 'symbol': 'AAPL', 'asset_type': 'Stock', 'source': 'manual', 'currency': 'USD', 'note': 'Recommended'},
    {'name': 'Microsoft Corporation', 'symbol': 'MSFT', 'asset_type': 'Stock', 'source': 'manual', 'currency': 'USD', 'note': 'Recommended'},
    {'name': 'Amazon.com, Inc.', 'symbol': 'AMZN', 'asset_type': 'Stock', 'source': 'manual', 'currency': 'USD', 'note': 'Recommended'},
    {'name': 'Tesla, Inc.', 'symbol': 'TSLA', 'asset_type': 'Stock', 'source': 'manual', 'currency': 'USD', 'note': 'Recommended'},
    {'name': 'SPDR S&P 500 ETF Trust', 'symbol': 'SPY', 'asset_type': 'ETF', 'source': 'manual', 'currency': 'USD', 'note': 'Recommended'},
    {'name': 'Invesco QQQ Trust', 'symbol': 'QQQ', 'asset_type': 'ETF', 'source': 'manual', 'currency': 'USD', 'note': 'Recommended'},
]


class AddProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Add Product')
        self.resize(560, 520)
        self.product_service = ProductService()
        self.recommended_added = False

        root = QVBoxLayout(self)

        root.addWidget(QLabel('Recommended Products'))
        for item in RECOMMENDED_PRODUCTS:
            row = QHBoxLayout()
            label = QLabel(f"{item['name']} ({item['symbol']}) - {item['asset_type']}")
            button = QPushButton('Add')
            button.clicked.connect(lambda checked=False, p=item: self.add_recommended(p))
            row.addWidget(label)
            row.addStretch()
            row.addWidget(button)
            container = QWidget()
            container.setLayout(row)
            root.addWidget(container)

        root.addWidget(QLabel('Manual Add'))

        form_widget = QWidget()
        layout = QFormLayout(form_widget)

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

        root.addWidget(form_widget)

        self.status_label = QLabel('')
        self.status_label.setAlignment(Qt.AlignLeft)
        root.addWidget(self.status_label)

    def add_recommended(self, product_data):
        self.product_service.create_product(**product_data)
        self.recommended_added = True
        self.status_label.setText(f"Added: {product_data['symbol']}")

    def get_data(self):
        return {
            'name': self.name_input.text(),
            'symbol': self.symbol_input.text(),
            'asset_type': self.asset_type_input.currentText(),
            'source': self.source_input.text(),
            'currency': self.currency_input.text(),
            'note': self.note_input.toPlainText(),
        }
