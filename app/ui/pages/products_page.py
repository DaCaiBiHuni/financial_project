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
from PySide6.QtCore import Qt, QObject, QThread, Signal

from app.application.services.market_service import MarketService
from app.application.services.product_service import ProductService
from app.ui.pages.add_product_dialog import AddProductDialog
from app.ui.widgets.price_chart_widget import PriceChartWidget


class RefreshWorker(QObject):
    finished = Signal(list)
    failed = Signal(str)

    def __init__(self, mode: str):
        super().__init__()
        self.mode = mode

    def run(self):
        try:
            service = MarketService()
            if self.mode == 'price':
                results = service.refresh_all_prices()
            else:
                results = service.refresh_all_histories()
            self.finished.emit(results)
        except Exception as e:
            self.failed.emit(str(e))


class ProductsPage(QWidget):
    def __init__(self, on_data_changed=None):
        super().__init__()
        self.service = ProductService()
        self.market_service = MarketService()
        self.on_data_changed = on_data_changed
        self.refresh_thread = None
        self.refresh_worker = None
        self.refresh_mode = None

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
        self.loading_label = QLabel('')
        self.loading_label.setAlignment(Qt.AlignRight)
        self.chart_widget = PriceChartWidget(self)

        bottom_layout.addWidget(self.product_title)
        bottom_layout.addWidget(self.product_meta)
        bottom_layout.addWidget(self.chart_widget)
        bottom_layout.addWidget(self.status_label)
        bottom_layout.addWidget(self.loading_label)

        splitter.addWidget(top_container)
        splitter.addWidget(bottom_container)
        splitter.setSizes([220, 560])

        root_layout.addLayout(header_layout)
        root_layout.addWidget(splitter)

        self.refresh_table()

    def _set_loading(self, text: str = ''):
        self.loading_label.setText(text)

    def _start_refresh(self, mode: str, loading_text: str):
        if self.refresh_thread is not None:
            return
        self.refresh_mode = mode
        self._set_loading(loading_text)
        self.refresh_price_button.setEnabled(False)
        self.refresh_trend_button.setEnabled(False)

        self.refresh_thread = QThread()
        self.refresh_worker = RefreshWorker(mode)
        self.refresh_worker.moveToThread(self.refresh_thread)
        self.refresh_thread.started.connect(self.refresh_worker.run)
        self.refresh_worker.finished.connect(self._on_refresh_finished)
        self.refresh_worker.failed.connect(self._on_refresh_failed)
        self.refresh_worker.finished.connect(self.refresh_thread.quit)
        self.refresh_worker.failed.connect(self.refresh_thread.quit)
        self.refresh_worker.finished.connect(self.refresh_worker.deleteLater)
        self.refresh_worker.failed.connect(self.refresh_worker.deleteLater)
        self.refresh_thread.finished.connect(self.refresh_thread.deleteLater)
        self.refresh_thread.finished.connect(self._cleanup_refresh)
        self.refresh_thread.start()

    def _cleanup_refresh(self):
        self.refresh_thread = None
        self.refresh_worker = None
        self.refresh_price_button.setEnabled(True)
        self.refresh_trend_button.setEnabled(True)
        self._set_loading('')

    def _on_refresh_finished(self, results):
        self.refresh_table()
        self.show_selected_product_detail()
        if not results:
            self.status_label.setText(f'{self.refresh_mode} refresh: no products to refresh')
        else:
            failed = [r for r in results if not r.get('ok')]
            if failed:
                prefix = 'Price' if self.refresh_mode == 'price' else 'Trend'
                self.status_label.setText(f"{prefix} refresh failed: {failed[-1]['message']}")
            else:
                prefix = 'Price' if self.refresh_mode == 'price' else 'Trend'
                self.status_label.setText(f"{prefix} refresh success: {results[-1]['message']}")
        if self.on_data_changed:
            self.on_data_changed()

    def _on_refresh_failed(self, error_text: str):
        prefix = 'Price' if self.refresh_mode == 'price' else 'Trend'
        self.status_label.setText(f'{prefix} refresh crashed: {error_text}')

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
        self._start_refresh('price', 'Loading price…')

    def refresh_trends(self):
        provider = self.market_service.get_provider_name()
        text = 'Loading 1Y trend…'
        if provider == 'alphavantage':
            text = 'Loading 1Y trend… (with retry)'
        self._start_refresh('trend', text)

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
