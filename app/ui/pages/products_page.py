from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class ProductsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('Products Page'))
        layout.addWidget(QLabel('Manage tracked products and view product details.'))
