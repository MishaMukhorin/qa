import pytest
import requests
from config import BASE_URL, TEST_PRODUCTS, INVALID_TEST_CASES, EXPECTED_FIELDS

class TestShopAPI:
    created_product_ids = []
    
    @classmethod
    def teardown_class(cls):
        for product_id in cls.created_product_ids:
            try:
                requests.get(f"{BASE_URL}/api/deleteproduct?id={product_id}")
            except:
                pass
    
    def verify_product_fields(self, product, expected_data):
        for field in EXPECTED_FIELDS:
            assert field in product, f"Missing field: {field}"
        
        if expected_data:
            assert product["category_id"] == expected_data["category_id"]
            assert product["title"] == expected_data["title"]
            assert product["content"] == expected_data["content"]
            assert product["price"] == expected_data["price"]
            assert product["status"] == expected_data["status"]
    
    @pytest.mark.parametrize("product_data", TEST_PRODUCTS)
    def test_add_product(self, product_data):
        response = requests.post(f"{BASE_URL}/api/addproduct", json=product_data)
        
        assert response.status_code == 201 or response.status_code == 200, \
            f"Failed to add product. Status: {response.status_code}, Response: {response.text}"
        
        product = response.json()
        assert "id" in product, "Product ID not returned"
        
        TestShopAPI.created_product_ids.append(product["id"])
        self.verify_product_fields(product, product_data)
    
    def test_add_product_with_all_fields(self):
        product_data = {
            "category_id": 5,
            "title": "Complete Test Product",
            "content": "Full product with all fields",
            "price": 5000,
            "old_price": 6000,
            "status": 1,
            "keywords": "complete, test, all fields",
            "description": "Full description for complete product",
            "hit": 1
        }
        
        response = requests.post(f"{BASE_URL}/api/addproduct", json=product_data)
        assert response.status_code in [200, 201]
        
        product = response.json()
        TestShopAPI.created_product_ids.append(product["id"])
        self.verify_product_fields(product, product_data)
        
        assert product["old_price"] == 6000
        assert product["keywords"] == product_data["keywords"]
        assert product["description"] == product_data["description"]
        assert product["hit"] == 1
    
    def test_get_all_products(self):
        response = requests.get(f"{BASE_URL}/api/products")
        
        assert response.status_code == 200, \
            f"Failed to get products. Status: {response.status_code}"
        
        products = response.json()
        assert isinstance(products, list), "Response should be a list"
        
        if products:
            self.verify_product_fields(products[0], None)
    
    def test_edit_product(self):
        add_data = {
            "category_id": 1,
            "title": "Product Before Edit",
            "content": "Original content",
            "price": 1000,
            "status": 1
        }
        
        add_response = requests.post(f"{BASE_URL}/api/addproduct", json=add_data)
        assert add_response.status_code in [200, 201]
        product = add_response.json()
        product_id = product["id"]
        TestShopAPI.created_product_ids.append(product_id)
        
        edit_data = {
            "id": product_id,
            "category_id": 2,
            "title": "Product After Edit",
            "content": "Updated content",
            "price": 1500,
            "old_price": 2000,
            "status": 0,
            "keywords": "edited, updated",
            "description": "Updated description",
            "hit": 1
        }
        
        edit_response = requests.post(f"{BASE_URL}/api/editproduct", json=edit_data)
        assert edit_response.status_code in [200, 201], \
            f"Failed to edit product. Status: {edit_response.status_code}"
        
        updated_product = edit_response.json()
        assert updated_product["id"] == product_id
        assert updated_product["title"] == "Product After Edit"
        assert updated_product["price"] == 1500
        assert updated_product["status"] == 0
    
    def test_delete_product(self):
        add_data = {
            "category_id": 1,
            "title": "Product To Delete",
            "content": "Will be deleted",
            "price": 500,
            "status": 1
        }
        
        add_response = requests.post(f"{BASE_URL}/api/addproduct", json=add_data)
        assert add_response.status_code in [200, 201]
        product_id = add_response.json()["id"]
        
        delete_response = requests.get(f"{BASE_URL}/api/deleteproduct?id={product_id}")
        assert delete_response.status_code == 200, \
            f"Failed to delete product. Status: {delete_response.status_code}"
        
        all_products = requests.get(f"{BASE_URL}/api/products").json()
        deleted_product = next((p for p in all_products if p["id"] == product_id), None)
        assert deleted_product is None, "Product still exists after deletion"
    
    def test_add_product_minimal_fields(self):
        minimal_data = {
            "category_id": 1,
            "title": "Minimal Product",
            "content": "Minimal",
            "price": 100,
            "status": 1
        }
        
        response = requests.post(f"{BASE_URL}/api/addproduct", json=minimal_data)
        assert response.status_code in [200, 201]
        
        product = response.json()
        TestShopAPI.created_product_ids.append(product["id"])
        assert product["title"] == "Minimal Product"
    
    def test_add_product_with_zero_price(self):
        data = {
            "category_id": 1,
            "title": "Free Product",
            "content": "Free item",
            "price": 0,
            "status": 1
        }
        
        response = requests.post(f"{BASE_URL}/api/addproduct", json=data)
        
        if response.status_code in [200, 201]:
            product = response.json()
            TestShopAPI.created_product_ids.append(product["id"])
            assert product["price"] == 0
    
    def test_edit_nonexistent_product(self):
        edit_data = {
            "id": 999999,
            "category_id": 1,
            "title": "Nonexistent",
            "content": "Should fail",
            "price": 100,
            "status": 1
        }
        
        response = requests.post(f"{BASE_URL}/api/editproduct", json=edit_data)
        assert response.status_code in [404, 400, 500], \
            "Should fail when editing nonexistent product"
    
    def test_delete_nonexistent_product(self):
        response = requests.get(f"{BASE_URL}/api/deleteproduct?id=999999")
        assert response.status_code in [404, 400, 200], \
            "Should handle deletion of nonexistent product gracefully"
    
    def test_alias_generation(self):
        data = {
            "category_id": 1,
            "title": "Test Alias Generation",
            "content": "Testing alias",
            "price": 100,
            "status": 1
        }
        
        response = requests.post(f"{BASE_URL}/api/addproduct", json=data)
        assert response.status_code in [200, 201]
        
        product = response.json()
        TestShopAPI.created_product_ids.append(product["id"])
        
        assert "alias" in product
        assert isinstance(product["alias"], str)
        assert len(product["alias"]) > 0
    
    def test_add_multiple_products_same_title(self):
        data = {
            "category_id": 1,
            "title": "Duplicate Title Product",
            "content": "First",
            "price": 100,
            "status": 1
        }
        
        response1 = requests.post(f"{BASE_URL}/api/addproduct", json=data)
        assert response1.status_code in [200, 201]
        product1 = response1.json()
        TestShopAPI.created_product_ids.append(product1["id"])
        
        data["content"] = "Second"
        response2 = requests.post(f"{BASE_URL}/api/addproduct", json=data)
        assert response2.status_code in [200, 201]
        product2 = response2.json()
        TestShopAPI.created_product_ids.append(product2["id"])
        
        assert product1["alias"] != product2["alias"], \
            "Aliases should be different for same title"