from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('Dashboard Page'))
        layout.addWidget(QLabel('Show portfolio summary, performance, and highlights.'))
