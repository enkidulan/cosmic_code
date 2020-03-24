import models


def test_product():
    product = models.Product(sku=1)
    assert product.sku == 1
