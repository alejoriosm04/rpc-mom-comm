def get_products():
    return [
        {
            "id": 1,
            "title": "Product C",
            "price": 100.0,
            "description": "Description A",
            "category": {
                "id": 1,
                "name": "Category A",
                "image": "https://example.com/image.jpg",
                "slug": "category-a"
            },
            "images": ["https://example.com/image.jpg"]
        }
    ]
