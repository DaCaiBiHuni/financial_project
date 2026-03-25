from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.ui.pages.dashboard_page import DashboardPage
from app.ui.pages.products_page import ProductsPage
from app.ui.pages.portfolio_page import PortfolioPage
from app.ui.pages.settings_page import SettingsPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Investment Tracker')
        self.resize(1200, 800)

        container = QWidget()
        self.setCentralWidget(container)

        root_layout = QHBoxLayout(container)

        self.nav_list = QListWidget()
        self.nav_list.addItems(['Dashboard', 'Products', 'Portfolio', 'Settings'])
        self.nav_list.setFixedWidth(180)

        self.stack = QStackedWidget()
        self.stack.addWidget(DashboardPage())
        self.stack.addWidget(ProductsPage())
        self.stack.addWidget(PortfolioPage())
        self.stack.addWidget(SettingsPage())

        root_layout.addWidget(self.nav_list)
        root_layout.addWidget(self.stack)

        self.nav_list.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.nav_list.setCurrentRow(0)
