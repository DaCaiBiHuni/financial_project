from PySide6.QtWidgets import (
    QHBoxLayout,
    QListWidget,
    QMainWindow,
    QStackedWidget,
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

        self.dashboard_page = DashboardPage()
        self.products_page = ProductsPage(on_data_changed=self.refresh_all_pages)
        self.portfolio_page = PortfolioPage(on_data_changed=self.refresh_all_pages)
        self.settings_page = SettingsPage()

        self.stack = QStackedWidget()
        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.products_page)
        self.stack.addWidget(self.portfolio_page)
        self.stack.addWidget(self.settings_page)

        root_layout.addWidget(self.nav_list)
        root_layout.addWidget(self.stack)

        self.nav_list.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.nav_list.setCurrentRow(0)

    def refresh_all_pages(self):
        self.dashboard_page.refresh_summary()
        self.products_page.refresh_table()
        self.portfolio_page.refresh_table()
