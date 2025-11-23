BASE_URL = "http://shop2.qatl.ru/shop"

TEST_PRODUCTS = [
    {
        "category_id": 1,
        "title": "Test Product Alpha",
        "content": "High quality test product",
        "price": 1999,
        "old_price": 2499,
        "status": 1,
        "keywords": "test, alpha, quality",
        "description": "Test product alpha description",
        "hit": 1
    },
    {
        "category_id": 2,
        "title": "Test Product Beta",
        "content": "Another test product",
        "price": 999,
        "old_price": 1299,
        "status": 0,
        "keywords": "test, beta",
        "description": "Test product beta description",
        "hit": 0
    },
    {
        "category_id": 3,
        "title": "Test Product Gamma",
        "content": "Third test product",
        "price": 3499,
        "old_price": 3999,
        "status": 1,
        "keywords": "test, gamma, premium",
        "description": "Premium test product",
        "hit": 1
    }
]

INVALID_TEST_CASES = [
    {
        "name": "negative_price",
        "data": {
            "category_id": 1,
            "title": "Invalid Price Product",
            "content": "Test",
            "price": -100,
            "status": 1
        }
    },
    {
        "name": "invalid_category",
        "data": {
            "category_id": 999,
            "title": "Invalid Category",
            "content": "Test",
            "price": 100,
            "status": 1
        }
    },
    {
        "name": "empty_title",
        "data": {
            "category_id": 1,
            "title": "",
            "content": "Test",
            "price": 100,
            "status": 1
        }
    }
]

EXPECTED_FIELDS = [
    "id", "category_id", "title", "alias", "content", 
    "price", "old_price", "status", "keywords", "description", "hit"
]