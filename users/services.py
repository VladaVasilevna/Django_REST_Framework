import stripe
from config.settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY  # ключ из .env и settings.py


def create_stripe_product(course):
    """Создает продукт в Stripe."""
    product = stripe.Product.create(name=course)
    return product


def create_stripe_price(amount):
    """
    Создает цену для продукта в Stripe.
    amount - сумма в копейках.
    """
    return stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product_data={"name": "Payment"},
    )


def create_stripe_session(price):
    """Создает сессию оплаты в Stripe и возвращает объект сессии."""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )

    return session.get("id"), session.get("url")
