from app.infrastructure.db.repositories.settings_repository import SettingsRepository


class SettingsService:
    def __init__(self):
        self.repo = SettingsRepository()

    def get_market_provider(self) -> str:
        return self.repo.get('market_provider', 'mock')

    def set_market_provider(self, provider: str):
        self.repo.set('market_provider', provider)
