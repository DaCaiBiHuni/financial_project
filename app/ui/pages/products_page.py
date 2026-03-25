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

from app.application.services.market_service import MarketService
from app.application.services.product_service import ProductService
from app.ui.pages.add_product_dialog import AddProductDialog
from app.ui.widgets.price_chart_widget import PriceChartWidget


class ProductsPage(QWidget):
    def __init__(self, on_data_changed=None):
        super().__init__()
        self.service = ProductService()
        self.market_service = MarketService()
        self.on_data_changed = on_data_changed

        layout = QVBoxLayout(self)

        top_bar = QHBoxLayout()
        title = QLabel('Products')
        self.provider_label = QLabel(f"Provider: {self.market_service.get_provider_name()}")
        self.add_button = QPushButton('Add Product')
        self.add_button.clicked.connect(self.open_add_dialog)
        self.refresh_button = QPushButton('Refresh Prices')
        self.refresh_button.clicked.connect(self.refresh_prices)
        top_bar.addWidget(title)
        top_bar.addWidget(self.provider_label)
        top_bar.addStretch()
        top_bar.addWidget(self.refresh_button)
        top_bar.addWidget(self.add_button)

        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels(['Name', 'Symbol', 'Type', 'Source', 'Currency', 'Price', 'Updated', 'Note'])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.itemSelectionChanged.connect(self.show_selected_product_detail)

        self.detail_label = QLabel('Product Detail: select a product to view details')
        self.history_label = QLabel('Trend Preview: no data yet')
        self.status_label = QLabel('')
        self.chart_widget = PriceChartWidget(self)

        layout.addLayout(top_bar)
        layout.addWidget(self.table)
        layout.addWidget(self.detail_label)
        layout.addWidget(self.history_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.chart_widget)

        self.refresh_table()

    def refresh_table(self):
        self.provider_label.setText(f"Provider: {self.market_service.get_provider_name()}")
        products = self.service.get_all_products()
        self.table.setRowCount(len(products))
        for row, product in enumerate(products):
            self.table.setItem(row, 0, QTableWidgetItem(product.name))
            self.table.setItem(row, 1, QTableWidgetItem(product.symbol))
            self.table.setItem(row, 2, QTableWidgetItem(product.asset_type))
            self.table.setItem(row, 3, QTableWidgetItem(product.source))
            self.table.setItem(row, 4, QTableWidgetItem(product.currency))
            self.table.setItem(row, 5, QTableWidgetItem(f"{product.current_price:.2f}"))
            self.table.setItem(row, 6, QTableWidgetItem(product.last_updated))
            self.table.setItem(row, 7, QTableWidgetItem(product.note))
            self.table.item(row, 0).setData(256, product.id)

    def refresh_prices(self):
        results = self.market_service.refresh_all_prices()
        self.refresh_table()
        self.show_selected_product_detail()
        if results:
            latest_message = results[-1]['message']
            self.status_label.setText(f"Refresh result: {latest_message}")
        else:
            self.status_label.setText('Refresh result: no products to refresh')
        if self.on_data_changed:
            self.on_data_changed()

    def show_selected_product_detail(self):
        items = self.table.selectedItems()
        if not items:
            self.detail_label.setText('Product Detail: select a product to view details')
            self.history_label.setText('Trend Preview: no data yet')
            self.chart_widget.plot_prices([])
            return
        row = items[0].row()
        product_id = self.table.item(row, 0).data(256)
        product = self.service.get_product(product_id)
        if not product:
            return
        self.detail_label.setText(
            f"Product Detail | Name: {product.name} | Symbol: {product.symbol} | Type: {product.asset_type} | Price: {product.current_price:.2f} {product.currency} | Updated: {product.last_updated}"
        )
        history = self.market_service.get_price_history(product_id, limit=8)
        if history:
            trend = ' -> '.join(f"{price:.2f}" for price, _ts in history)
            self.history_label.setText(f"Trend Preview: {trend}")
        else:
            self.history_label.setText('Trend Preview: no data yet')
        self.chart_widget.plot_prices(history)

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
