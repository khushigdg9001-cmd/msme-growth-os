from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_inventory():
    return [
        {
            "id": 1,
            "product": "Black Oversized Tee",
            "stock": 18,
            "forecast": 147,
            "supplier": "Metro Textile",
            "status": "Restock",
        },
        {
            "id": 2,
            "product": "Blue Denim Jacket",
            "stock": 62,
            "forecast": 40,
            "supplier": "Urban Denim",
            "status": "Healthy",
        },
        {
            "id": 3,
            "product": "White Hoodie",
            "stock": 12,
            "forecast": 86,
            "supplier": "Classic Cotton",
            "status": "Urgent",
        },
        {
            "id": 4,
            "product": "Cargo Pants",
            "stock": 34,
            "forecast": 91,
            "supplier": "Denim Works",
            "status": "Healthy",
        },
        {
            "id": 5,
            "product": "Premium Polo Shirt",
            "stock": 8,
            "forecast": 115,
            "supplier": "Elite Fashion",
            "status": "Restock",
        },
    ]