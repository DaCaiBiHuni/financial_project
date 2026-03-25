from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.application.services.product_service import ProductService
from app.ui.pages.add_product_dialog import AddProductDialog


class ProductsPage(QWidget):
    def __init__(self, on_data_changed=None):
        super().__init__()
        self.service = ProductService()
        self.on_data_changed = on_data_changed

        layout = QVBoxLayout(self)

        top_bar = QHBoxLayout()
        title = QLabel('Products')
        self.add_button = QPushButton('Add Product')
        self.add_button.clicked.connect(self.open_add_dialog)
        top_bar.addWidget(title)
        top_bar.addStretch()
        top_bar.addWidget(self.add_button)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(['Name', 'Symbol', 'Type', 'Source', 'Currency', 'Note'])
        self.table.horizontalHeader().setStretchLastSection(True)

        layout.addLayout(top_bar)
        layout.addWidget(self.table)

        self.refresh_table()

    def refresh_table(self):
        products = self.service.get_all_products()
        self.table.setRowCount(len(products))
        for row, product in enumerate(products):
            self.table.setItem(row, 0, QTableWidgetItem(product.name))
            self.table.setItem(row, 1, QTableWidgetItem(product.symbol))
            self.table.setItem(row, 2, QTableWidgetItem(product.asset_type))
            self.table.setItem(row, 3, QTableWidgetItem(product.source))
            self.table.setItem(row, 4, QTableWidgetItem(product.currency))
            self.table.setItem(row, 5, QTableWidgetItem(product.note))

    def open_add_dialog(self):
        dialog = AddProductDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            if not data['name'].strip() or not data['symbol'].strip():
                QMessageBox.warning(self, 'Validation Error', 'Name and Symbol are required.')
                return
            self.service.create_product(**data)
            self.refresh_table()
            if self.on_data_changed:
                self.on_data_changed()
