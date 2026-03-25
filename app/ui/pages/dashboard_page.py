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

        grid = QGridLayout()
        grid.addWidget(QLabel('Tracked Products'), 0, 0)
        grid.addWidget(self.product_count_label, 0, 1)
        grid.addWidget(QLabel('Portfolio Positions'), 1, 0)
        grid.addWidget(self.position_count_label, 1, 1)
        grid.addWidget(QLabel('Total Cost'), 2, 0)
        grid.addWidget(self.total_cost_label, 2, 1)

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
