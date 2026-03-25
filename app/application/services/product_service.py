from datetime import datetime

from app.domain.models.product import Product
from app.infrastructure.db.repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self):
        self.repo = ProductRepository()

    def create_product(self, name: str, symbol: str, asset_type: str, source: str, currency: str, note: str = '') -> int:
        existing = self.repo.get_by_symbol(symbol.strip())
        if existing:
            return existing.id
        product = Product(
            id=None,
            name=name.strip(),
            symbol=symbol.strip(),
            asset_type=asset_type.strip(),
            source=source.strip(),
            currency=currency.strip(),
            current_price=0.0,
            last_updated=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            note=note.strip(),
        )
        return self.repo.add_product(product)

    def get_all_products(self) -> list[Product]:
        return self.repo.list_products()

    def get_product(self, product_id: int):
        return self.repo.get_product(product_id)
