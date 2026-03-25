from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class PortfolioPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('Portfolio Page'))
        layout.addWidget(QLabel('Show current positions, market value, and profit/loss.'))
