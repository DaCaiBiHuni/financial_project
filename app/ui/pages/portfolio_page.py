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

from app.application.services.portfolio_service import PortfolioService
from app.application.services.product_service import ProductService
from app.ui.pages.add_position_dialog import AddPositionDialog


class PortfolioPage(QWidget):
    def __init__(self, on_data_changed=None):
        super().__init__()
        self.portfolio_service = PortfolioService()
        self.product_service = ProductService()
        self.on_data_changed = on_data_changed

        layout = QVBoxLayout(self)

        top_bar = QHBoxLayout()
        self.summary_label = QLabel('Portfolio Summary')
        self.add_button = QPushButton('Add Position')
        self.add_button.clicked.connect(self.open_add_dialog)
        top_bar.addWidget(self.summary_label)
        top_bar.addStretch()
        top_bar.addWidget(self.add_button)

        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels([
            'Product', 'Quantity', 'Avg Cost', 'Current Price', 'Market Value', 'P/L', 'P/L %'
        ])
        self.table.horizontalHeader().setStretchLastSection(True)

        layout.addLayout(top_bar)
        layout.addWidget(self.table)

        self.refresh_table()

    def refresh_table(self):
        positions = self.portfolio_service.get_all_positions()
        summary = self.portfolio_service.get_portfolio_summary()
        self.summary_label.setText(
            'Portfolio Summary | '
            f"Positions: {summary['position_count']} | "
            f"Cost: {summary['total_cost']:.2f} | "
            f"Value: {summary['total_market_value']:.2f} | "
            f"P/L: {summary['total_profit_loss']:.2f} ({summary['total_profit_loss_rate']:.2f}%)"
        )
        self.table.setRowCount(len(positions))
        for row, position in enumerate(positions):
            self.table.setItem(row, 0, QTableWidgetItem(position.product_name))
            self.table.setItem(row, 1, QTableWidgetItem(str(position.quantity)))
            self.table.setItem(row, 2, QTableWidgetItem(f"{position.average_cost:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{position.current_price:.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{position.market_value:.2f}"))
            self.table.setItem(row, 5, QTableWidgetItem(f"{position.profit_loss:.2f}"))
            self.table.setItem(row, 6, QTableWidgetItem(f"{position.profit_loss_rate:.2f}%"))

    def open_add_dialog(self):
        products = self.product_service.get_all_products()
        if not products:
            QMessageBox.warning(self, 'No Products', 'Please add at least one product first.')
            return

        dialog = AddPositionDialog(products, self)
        if dialog.exec():
            data = dialog.get_data()
            if data['quantity'] <= 0 or data['average_cost'] <= 0:
                QMessageBox.warning(self, 'Validation Error', 'Quantity and Average Cost must be greater than 0.')
                return
            self.portfolio_service.create_position(**data)
            self.refresh_table()
            if self.on_data_changed:
                self.on_data_changed()
