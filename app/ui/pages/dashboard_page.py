from PySide6.QtWidgets import QGridLayout, QLabel, QVBoxLayout, QWidget

from app.application.services.dashboard_service import DashboardService


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = DashboardService()

        layout = QVBoxLayout(self)
        title = QLabel('Dashboard')
        subtitle = QLabel('Portfolio overview and key summary metrics')

        self.product_count_label = QLabel()
        self.position_count_label = QLabel()
        self.total_cost_label = QLabel()
        self.total_market_value_label = QLabel()
        self.total_profit_loss_label = QLabel()
        self.total_profit_loss_rate_label = QLabel()

        grid = QGridLayout()
        grid.addWidget(QLabel('Tracked Products'), 0, 0)
        grid.addWidget(self.product_count_label, 0, 1)
        grid.addWidget(QLabel('Portfolio Positions'), 1, 0)
        grid.addWidget(self.position_count_label, 1, 1)
        grid.addWidget(QLabel('Total Cost'), 2, 0)
        grid.addWidget(self.total_cost_label, 2, 1)
        grid.addWidget(QLabel('Total Market Value'), 3, 0)
        grid.addWidget(self.total_market_value_label, 3, 1)
        grid.addWidget(QLabel('Profit / Loss'), 4, 0)
        grid.addWidget(self.total_profit_loss_label, 4, 1)
        grid.addWidget(QLabel('Profit / Loss %'), 5, 0)
        grid.addWidget(self.total_profit_loss_rate_label, 5, 1)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(grid)
        layout.addStretch()

        self.refresh_summary()

    def refresh_summary(self):
        summary = self.service.get_dashboard_summary()
        self.product_count_label.setText(str(summary['product_count']))
        self.position_count_label.setText(str(summary['position_count']))
        self.total_cost_label.setText(f"{summary['total_cost']:.2f}")
        self.total_market_value_label.setText(f"{summary['total_market_value']:.2f}")
        self.total_profit_loss_label.setText(f"{summary['total_profit_loss']:.2f}")
        self.total_profit_loss_rate_label.setText(f"{summary['total_profit_loss_rate']:.2f}%")
