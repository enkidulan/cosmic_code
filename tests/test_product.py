import domain


def test_product():
    product = domain.Product(sku=1)
    assert product.sku == 1
