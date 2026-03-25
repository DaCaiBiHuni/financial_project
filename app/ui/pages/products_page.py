from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtCore import Qt

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

        root_layout = QVBoxLayout(self)

        header_layout = QHBoxLayout()
        title = QLabel('Products')
        self.provider_label = QLabel(f"Provider: {self.market_service.get_provider_name()}")
        self.refresh_price_button = QPushButton('Refresh Prices')
        self.refresh_price_button.clicked.connect(self.refresh_prices)
        self.refresh_trend_button = QPushButton('Refresh 1Y Trend')
        self.refresh_trend_button.clicked.connect(self.refresh_trends)
        self.add_button = QPushButton('Add Product')
        self.add_button.clicked.connect(self.open_add_dialog)
        header_layout.addWidget(title)
        header_layout.addWidget(self.provider_label)
        header_layout.addStretch()
        header_layout.addWidget(self.refresh_price_button)
        header_layout.addWidget(self.refresh_trend_button)
        header_layout.addWidget(self.add_button)

        splitter = QSplitter(Qt.Vertical)

        top_container = QWidget()
        top_layout = QVBoxLayout(top_container)
        top_layout.addWidget(QLabel('Tracked Products'))
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(['Name', 'Symbol', 'Price', 'Updated'])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.itemSelectionChanged.connect(self.show_selected_product_detail)
        top_layout.addWidget(self.table)

        bottom_container = QWidget()
        bottom_layout = QVBoxLayout(bottom_container)

        self.product_title = QLabel('No product selected')
        self.product_meta = QLabel('Select a product to view its latest trend')
        self.status_label = QLabel('')
        self.chart_widget = PriceChartWidget(self)

        bottom_layout.addWidget(self.product_title)
        bottom_layout.addWidget(self.product_meta)
        bottom_layout.addWidget(self.status_label)
        bottom_layout.addWidget(self.chart_widget)

        splitter.addWidget(top_container)
        splitter.addWidget(bottom_container)
        splitter.setSizes([220, 560])

        root_layout.addLayout(header_layout)
        root_layout.addWidget(splitter)

        self.refresh_table()

    def refresh_table(self):
        self.provider_label.setText(f"Provider: {self.market_service.get_provider_name()}")
        products = self.service.get_all_products()
        self.table.setRowCount(len(products))
        for row, product in enumerate(products):
            self.table.setItem(row, 0, QTableWidgetItem(product.name))
            self.table.setItem(row, 1, QTableWidgetItem(product.symbol))
            self.table.setItem(row, 2, QTableWidgetItem(f"{product.current_price:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(product.last_updated))
            self.table.item(row, 0).setData(256, product.id)

    def refresh_prices(self):
        results = self.market_service.refresh_all_prices()
        self.refresh_table()
        self.show_selected_product_detail()
        if not results:
            self.status_label.setText('Price refresh: no products to refresh')
        else:
            failed = [r for r in results if not r.get('ok')]
            if failed:
                self.status_label.setText(f"Price refresh failed: {failed[-1]['message']}")
            else:
                self.status_label.setText(f"Price refresh success: {results[-1]['message']}")
        if self.on_data_changed:
            self.on_data_changed()

    def refresh_trends(self):
        results = self.market_service.refresh_all_histories()
        self.show_selected_product_detail()
        if not results:
            self.status_label.setText('Trend refresh: no products to refresh')
        else:
            failed = [r for r in results if not r.get('ok')]
            if failed:
                self.status_label.setText(f"Trend refresh failed: {failed[-1]['message']}")
            else:
                self.status_label.setText(f"Trend refresh success: {results[-1]['message']}")

    def show_selected_product_detail(self):
        items = self.table.selectedItems()
        if not items:
            self._clear_detail()
            return
        row = items[0].row()
        product_id = self.table.item(row, 0).data(256)
        product = self.service.get_product(product_id)
        if not product:
            self._clear_detail()
            return

        self.product_title.setText(f"{product.name} ({product.symbol})")
        self.product_meta.setText(
            f"{product.asset_type} · {product.currency} · Current Price: {product.current_price:.2f} · Updated: {product.last_updated or '-'}"
        )

        history = self.market_service.get_price_history(product_id, limit=12)
        self.chart_widget.plot_prices(history)

    def _clear_detail(self):
        self.product_title.setText('No product selected')
        self.product_meta.setText('Select a product to view its latest trend')
        self.chart_widget.plot_prices([])

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
