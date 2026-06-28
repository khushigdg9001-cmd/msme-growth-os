from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_finance():
    return {
        "revenue": 235000,
        "expenses": 142000,
        "profit": 93000,
        "cash": 185000,
        "pendingPayments": 38000,
        "monthlyGrowth": 18,
        "recommendation": {
    "title": "Approve ₹52,000 Inventory Procurement Budget",
    "reason": (
        "Monthly revenue has grown by 18% while maintaining a healthy cash "
        "balance of ₹185,000. AI recommends allocating ₹52,000 to replenish "
        "high-demand products and maximize next month's sales."
    ),
    "confidence": "96%"
}
    }