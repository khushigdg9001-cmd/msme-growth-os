from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_crm():

    return {
"customers": 286,

"activeCustomers": 214,

"newLeads": 27,

"conversionRate": 68,

"followUps": 14,

        "recommendation": {

    "title": "Launch VIP Customer Retention Campaign",

    "reason": (
        "AI identified 27 inactive premium customers. "
        "Priority follow-up should focus on Sneha Verma (₹22,500) "
        "and Priya Jain (₹19,800) using personalized WhatsApp offers "
        "to improve retention and increase repeat purchases."
    ),

    "confidence": "96%"

},
        "customerList": [

            {
                "id": 1,
                "name": "Rahul Sharma",
                "company": "Metro Textile",
                "lastPurchase": "12 Jun 2026",
                "status": "Active",
                "value": "₹48,000"
            },

            {
                "id": 2,
                "name": "Sneha Verma",
                "company": "Elite Fashion",
                "lastPurchase": "02 Jun 2026",
                "status": "Inactive",
                "value": "₹22,500"
            },

            {
                "id": 3,
                "name": "Amit Singh",
                "company": "Classic Cotton",
                "lastPurchase": "18 Jun 2026",
                "status": "Active",
                "value": "₹73,000"
            },

            {
                "id": 4,
                "name": "Priya Jain",
                "company": "Urban Denim",
                "lastPurchase": "29 May 2026",
                "status": "Follow-up",
                "value": "₹19,800"
            },

            {
                "id": 5,
                "name": "Karan Mehta",
                "company": "Denim Works",
                "lastPurchase": "21 Jun 2026",
                "status": "Active",
                "value": "₹58,900"
            }

        ]

    }