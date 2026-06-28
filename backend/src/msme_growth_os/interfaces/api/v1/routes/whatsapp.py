from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_whatsapp():

    return [

        {
            "id":1,
            "sender":"Metro Textile Pvt. Ltd.",
            "type":"supplier",
            "message":"Purchase Order PO-2026-4832 received. Dispatch scheduled for 30 Jun.",
            "time":"09:42 AM IST",
            "status":"read"
        },

        {
            "id":2,
            "sender":"Elite Fashion",
            "type":"supplier",
            "message":"Premium Polo Shirts are available for immediate dispatch.",
            "time":"10:08 AM IST",
            "status":"delivered"
        },

        {
            "id":4,
            "sender":"Classic Cotton",
            "type":"supplier",
            "message":"GST Invoice uploaded successfully.",
            "time":"10:31 AM IST",
            "status":"read"
        },

        {
            "id":5,
            "sender":"UrbanThreads Sales",
            "type":"customer",
            "message":"27 VIP customers will receive retention campaign today.",
            "time":"10:45 AM IST",
            "status":"read"
        }

    ]