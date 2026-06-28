from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_compliance():
    return {

        "gstStatus": "Filed",

        "licenses": 5,

        "expiringSoon": 2,

        "pendingDocuments": 4,

        "riskScore": "Low",

        "complianceRate": 96,

        "recommendation": {
    "title": "Renew Expiring Business Licenses",
    "reason": (
        "GST return has been filed successfully. "
        "However, the Trade License expires in 18 days. "
        "AI recommends completing the renewal immediately "
        "to maintain uninterrupted business operations."
    ),
    "confidence": "99%"
},

        "documents": [

            {
                "document": "GST Return",
                "status": "Filed",
                "dueDate": "15 Jul 2026"
            },

            {
                "document": "Trade License",
                "status": "Expiring",
                "dueDate": "18 Jul 2026"
            },

            {
                "document": "MSME Certificate",
                "status": "Valid",
                "dueDate": "12 Dec 2027"
            },

            {
                "document": "Fire NOC",
                "status": "Pending",
                "dueDate": "25 Jul 2026"
            },

            {
                "document": "Shop License",
                "status": "Valid",
                "dueDate": "15 Jan 2027"
            }

        ]
    }