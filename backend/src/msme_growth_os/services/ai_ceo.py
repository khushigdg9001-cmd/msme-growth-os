def generate_ceo_decision(
    inventory,
    finance,
    crm,
    compliance,
):

    health = 100
    decisions = []

    urgent = sum(
        1
        for item in inventory
        if item["status"] in ["Urgent", "Restock"]
    )

    if urgent:
        health -= 15

        decisions.append({
            "agent": "Inventory",
            "priority": "High",
            "title": "Restock Black Oversized Tee & White Hoodie",
"reason": "Black Oversized Tee (18→147) and White Hoodie (12→86) require immediate replenishment.",
            "confidence": "96%",
        })

    if finance["monthlyGrowth"] >= 15:

        decisions.append({
            "agent": "Finance",
            "priority": "High",
            "title": finance["recommendation"]["title"],
            "reason": finance["recommendation"]["reason"],
            "confidence": finance["recommendation"]["confidence"],
        })

    if crm["followUps"] > 10:

        health -= 5

        decisions.append({
            "agent": "CRM",
            "priority": "Medium",
            "title": crm["recommendation"]["title"],
            "reason": crm["recommendation"]["reason"],
            "confidence": crm["recommendation"]["confidence"],
        })

    if compliance["expiringSoon"] > 0:

        health -= 10

        decisions.append({
            "agent": "Compliance",
            "priority": "High",
            "title": compliance["recommendation"]["title"],
            "reason": compliance["recommendation"]["reason"],
            "confidence": compliance["recommendation"]["confidence"],
        })

    return {
        "businessHealth": max(health, 0),
        "growthScore": finance["monthlyGrowth"] + 76,
        "expectedProfit": finance["profit"] + 15000,
        "inventoryStatus": "Attention Required" if urgent else "Healthy",
        "financeStatus": "Strong",
        "crmStatus": "Needs Follow-up" if crm["followUps"] > 10 else "Healthy",
        "complianceStatus": "Review Required" if compliance["expiringSoon"] > 0 else "Healthy",
        "decisions": decisions,
    }