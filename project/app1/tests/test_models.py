import pytest
from app1.models import Product, Category

@pytest.mark.django_db
def test_product_creation():
    # Create a category first
    category = Category.objects.create(name='Test Category')

    # Now create a product with the valid category
    product = Product.objects.create(
        name='Test Product',
        category=category,  # Ensure valid category reference
        price=100,
        description='Test Description'
    )

    # Check that the product is created
    assert product.name == 'Test Product'
    assert product.category.name == 'Test Category'
