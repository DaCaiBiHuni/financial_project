from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('Settings Page'))
        layout.addWidget(QLabel('Configure data source, refresh settings, and preferences.'))
