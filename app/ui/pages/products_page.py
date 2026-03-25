from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
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

        content_layout = QHBoxLayout()

        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel('Tracked Products'))
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(['Name', 'Symbol', 'Type', 'Price', 'Updated'])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.itemSelectionChanged.connect(self.show_selected_product_detail)
        left_panel.addWidget(self.table)

        right_panel = QVBoxLayout()
        right_panel.addWidget(QLabel('Product Detail'))

        detail_card = QFrame()
        detail_card.setFrameShape(QFrame.StyledPanel)
        detail_layout = QGridLayout(detail_card)
        self.name_value = QLabel('-')
        self.symbol_value = QLabel('-')
        self.type_value = QLabel('-')
        self.source_value = QLabel('-')
        self.currency_value = QLabel('-')
        self.price_value = QLabel('-')
        self.updated_value = QLabel('-')
        self.note_value = QLabel('-')

        detail_layout.addWidget(QLabel('Name'), 0, 0)
        detail_layout.addWidget(self.name_value, 0, 1)
        detail_layout.addWidget(QLabel('Symbol'), 1, 0)
        detail_layout.addWidget(self.symbol_value, 1, 1)
        detail_layout.addWidget(QLabel('Type'), 2, 0)
        detail_layout.addWidget(self.type_value, 2, 1)
        detail_layout.addWidget(QLabel('Source'), 3, 0)
        detail_layout.addWidget(self.source_value, 3, 1)
        detail_layout.addWidget(QLabel('Currency'), 4, 0)
        detail_layout.addWidget(self.currency_value, 4, 1)
        detail_layout.addWidget(QLabel('Current Price'), 5, 0)
        detail_layout.addWidget(self.price_value, 5, 1)
        detail_layout.addWidget(QLabel('Updated'), 6, 0)
        detail_layout.addWidget(self.updated_value, 6, 1)
        detail_layout.addWidget(QLabel('Note'), 7, 0)
        detail_layout.addWidget(self.note_value, 7, 1)

        self.history_label = QLabel('Trend Preview: no data yet')
        self.status_label = QLabel('')
        self.chart_widget = PriceChartWidget(self)

        right_panel.addWidget(detail_card)
        right_panel.addWidget(self.history_label)
        right_panel.addWidget(self.status_label)
        right_panel.addWidget(self.chart_widget)

        content_layout.addLayout(left_panel, 5)
        content_layout.addLayout(right_panel, 4)

        root_layout.addLayout(header_layout)
        root_layout.addLayout(content_layout)

        self.refresh_table()

    def refresh_table(self):
        self.provider_label.setText(f"Provider: {self.market_service.get_provider_name()}")
        products = self.service.get_all_products()
        self.table.setRowCount(len(products))
        for row, product in enumerate(products):
            self.table.setItem(row, 0, QTableWidgetItem(product.name))
            self.table.setItem(row, 1, QTableWidgetItem(product.symbol))
            self.table.setItem(row, 2, QTableWidgetItem(product.asset_type))
            self.table.setItem(row, 3, QTableWidgetItem(f"{product.current_price:.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(product.last_updated))
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

        self.name_value.setText(product.name)
        self.symbol_value.setText(product.symbol)
        self.type_value.setText(product.asset_type)
        self.source_value.setText(product.source)
        self.currency_value.setText(product.currency)
        self.price_value.setText(f"{product.current_price:.2f}")
        self.updated_value.setText(product.last_updated)
        self.note_value.setText(product.note or '-')

        history = self.market_service.get_price_history(product_id, limit=12)
        if history:
            trend = ' -> '.join(f"{price:.2f}" for price, _ts in history)
            self.history_label.setText(f"Trend Preview: {trend}")
        else:
            self.history_label.setText('Trend Preview: no data yet')
        self.chart_widget.plot_prices(history)

    def _clear_detail(self):
        self.name_value.setText('-')
        self.symbol_value.setText('-')
        self.type_value.setText('-')
        self.source_value.setText('-')
        self.currency_value.setText('-')
        self.price_value.setText('-')
        self.updated_value.setText('-')
        self.note_value.setText('-')
        self.history_label.setText('Trend Preview: no data yet')
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
