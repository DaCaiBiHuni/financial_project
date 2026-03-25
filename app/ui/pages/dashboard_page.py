from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QVBoxLayout, QWidget

from app.application.services.dashboard_service import DashboardService


class SummaryCard(QFrame):
    def __init__(self, title: str):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        layout = QVBoxLayout(self)
        self.title_label = QLabel(title)
        self.value_label = QLabel('-')
        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)

    def set_value(self, value: str):
        self.value_label.setText(value)


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = DashboardService()

        layout = QVBoxLayout(self)
        title = QLabel('Dashboard')
        subtitle = QLabel('Portfolio overview and key summary metrics')

        self.products_card = SummaryCard('Tracked Products')
        self.positions_card = SummaryCard('Portfolio Positions')
        self.cost_card = SummaryCard('Total Cost')
        self.value_card = SummaryCard('Total Market Value')
        self.pnl_card = SummaryCard('Profit / Loss')
        self.pnl_rate_card = SummaryCard('Profit / Loss %')

        cards_grid = QGridLayout()
        cards_grid.addWidget(self.products_card, 0, 0)
        cards_grid.addWidget(self.positions_card, 0, 1)
        cards_grid.addWidget(self.cost_card, 0, 2)
        cards_grid.addWidget(self.value_card, 1, 0)
        cards_grid.addWidget(self.pnl_card, 1, 1)
        cards_grid.addWidget(self.pnl_rate_card, 1, 2)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(cards_grid)
        layout.addStretch()

        self.refresh_summary()

    def refresh_summary(self):
        summary = self.service.get_dashboard_summary()
        self.products_card.set_value(str(summary['product_count']))
        self.positions_card.set_value(str(summary['position_count']))
        self.cost_card.set_value(f"{summary['total_cost']:.2f}")
        self.value_card.set_value(f"{summary['total_market_value']:.2f}")
        self.pnl_card.set_value(f"{summary['total_profit_loss']:.2f}")
        self.pnl_rate_card.set_value(f"{summary['total_profit_loss_rate']:.2f}%")
