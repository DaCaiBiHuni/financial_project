from app.domain.models.product import Product
from app.infrastructure.db.repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self):
        self.repo = ProductRepository()

    def create_product(self, name: str, symbol: str, asset_type: str, source: str, currency: str, note: str = '') -> int:
        product = Product(
            id=None,
            name=name.strip(),
            symbol=symbol.strip(),
            asset_type=asset_type.strip(),
            source=source.strip(),
            currency=currency.strip(),
            note=note.strip(),
        )
        return self.repo.add_product(product)

    def get_all_products(self) -> list[Product]:
        return self.repo.list_products()
