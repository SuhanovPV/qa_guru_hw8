"""
Протестируйте классы из модуля homework/models.py
"""

import pytest
from models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def another_product():
    return Product("pen", 5, "Red pen", 100)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        assert product.check_quantity(0) is True
        assert product.check_quantity(500) is True
        assert product.check_quantity(1000) is True
        assert product.check_quantity(1001) is False

    def test_product_buy(self, product):
        product.buy(0)
        assert product.quantity == 1000
        product.buy(400)
        assert product.quantity == 600
        product.buy(600)
        assert product.quantity == 0

    def test_product_buy_more_than_available(self, product):
        with pytest.raises(ValueError, match="Product quantity less then required"):
            product.buy(1001)


class TestCart:
    """
    Тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product_to_empty_cart_quantity_specified(self, cart, product):
        """Проверка добавления продукта в пустую корзину с явным указанием количества"""
        cart.add_product(product, 15)

        assert len(cart.products) == 1
        assert product in cart.products
        assert cart.products[product] == 15

    def test_add_product_to_empty_cart_quantity_not_specified(self, cart, product):
        """Проверка добавления продукта в пустую корзину без указания количества"""
        cart.add_product(product)

        assert len(cart.products) == 1
        assert product in cart.products
        assert cart.products[product] == 1

    def test_add_same_product_to_cart(self, cart, product):
        """Проверка добавления в корзину продукта, который уже находится в ней"""
        cart.add_product(product, 20)
        cart.add_product(product, 10)

        assert len(cart.products) == 1
        assert product in cart.products
        assert cart.products[product] == 30

    def test_add_different_products_to_cart(self, cart, product, another_product):
        """Проверка добавления нескольких разных продуктов в корзину"""
        cart.add_product(product, 20)
        cart.add_product(another_product, 50)

        assert len(cart.products) == 2
        assert product in cart.products
        assert another_product in cart.products
        assert cart.products[product] == 20
        assert cart.products[another_product] == 50

    def test_remove_product_quantity_less_then_in_cart(self, cart, product):
        """Проверка удаления продукта из корзины. Количество продукта меньше количества в корзине"""
        cart.add_product(product, 50)
        cart.remove_product(product, 20)

        assert product in cart.products
        assert cart.products[product] == 30

    def test_remove_product_quantity_great_then_in_cart(self, cart, product):
        """Проверка удаления продукта из корзины. Количество продукта больше количества в корзине"""
        cart.add_product(product, 50)
        cart.remove_product(product, 51)

        assert len(cart.products) == 0

    def test_remove_product_quantity_equal_quantity_in_cart(self, cart, product):
        cart.add_product(product, 50)
        cart.remove_product(product, 50)

        assert len(cart.products) == 0

    def test_remove_product_quantity_not_specified(self, cart, product):
        """Проверка удаления продукта из корзины. Количество продукта не указано"""
        cart.add_product(product, 50)
        cart.remove_product(product)

        assert len(cart.products) == 0

    def test_remove_missing_product_from_cart_(self, cart, product, another_product):
        """Проверка удаления продукта, которого нет в корзине"""
        cart.add_product(product)
        with pytest.raises(ValueError, match="There is no product in the cart"):
            cart.remove_product(another_product)

    def test_clear_not_empty_cart(self, cart, product, another_product):
        """Проверка очистки не пустой корзины"""
        cart.add_product(product)
        cart.add_product(another_product)
        cart.clear()

        assert len(cart.products) == 0

    def test_clear_empty_cart(self, cart):
        """Проверка очистки пустой корзины"""
        cart.clear()

        assert len(cart.products) == 0

    def test_get_total_price_from_non_empty_cart(self, cart, product, another_product):
        """Проверка общей стоимости из корзины"""
        cart.add_product(product, 100)
        cart.add_product(another_product, 100)

        assert cart.get_total_price() == (product.price + another_product.price) * 100

    def test_get_total_price_from_empty_cart(self, cart):
        """Проверка получения общей стоимости из пустой корзины"""
        assert cart.get_total_price() == 0

    def test_buy_in_cart_one_product(self, cart, product):
        """Проверка покупки товара, в корзине один товар"""
        product_quantity = product.quantity
        cart.add_product(product, 100)
        cart.buy()

        assert len(cart.products) == 0
        assert product.quantity == product_quantity - 100

    def test_buy_in_cart_some_products(self, cart, product, another_product):
        product_quantity = product.quantity
        another_product_quantity = another_product.quantity
        cart.add_product(product, 100)
        cart.add_product(another_product, 100)
        cart.buy()

        assert len(cart.products) == 0
        assert product.quantity == product_quantity - 100
        assert another_product.quantity == another_product_quantity - 100

    def test_buy_empty_cart(self, cart):
        """Проверка покупки, корзина пуста"""
        cart.buy()
        assert len(cart.products) == 0

    def test_buy_product_quantity_in_cart_more_then_in_product(self, cart, product):
        """Проверка покупки, количество товара в корзине больше, чем на складе"""
        cart.add_product(product, 1200)
        with pytest.raises(ValueError, match="There is shortage of product on stock"):
            cart.buy()
