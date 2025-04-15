import asyncio
import sys
import os
from datetime import datetime

# Asegura que se pueda importar desde la raíz del microservicio
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import inventory_collection

async def seed_inventory():
    await inventory_collection.delete_many({})  # Limpia la colección si existe

    # Inventario de productos ya existentes en product_db.products
    inventory_data = [
        {"product_id": 1, "stock": 25, "updated_at": datetime.utcnow()},
        {"product_id": 2, "stock": 10, "updated_at": datetime.utcnow()},
        {"product_id": 3, "stock": 0,  "updated_at": datetime.utcnow()},
    ]

    await inventory_collection.insert_many(inventory_data)
    print("Inventario insertado correctamente.")

if __name__ == "__main__":
    asyncio.run(seed_inventory())
