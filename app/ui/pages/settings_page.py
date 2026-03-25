from PySide6.QtWidgets import QComboBox, QLabel, QPushButton, QVBoxLayout, QWidget

from app.application.services.settings_service import SettingsService


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = SettingsService()

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('Settings'))
        layout.addWidget(QLabel('Market Data Provider'))

        self.provider_combo = QComboBox()
        self.provider_combo.addItems(['mock', 'yahoo'])
        current = self.service.get_market_provider()
        idx = self.provider_combo.findText(current)
        if idx >= 0:
            self.provider_combo.setCurrentIndex(idx)

        self.save_button = QPushButton('Save Settings')
        self.status_label = QLabel(f'Current provider: {current}')
        self.save_button.clicked.connect(self.save_settings)

        layout.addWidget(self.provider_combo)
        layout.addWidget(self.save_button)
        layout.addWidget(self.status_label)
        layout.addStretch()

    def save_settings(self):
        provider = self.provider_combo.currentText()
        self.service.set_market_provider(provider)
        self.status_label.setText(f'Market provider saved: {provider}')
