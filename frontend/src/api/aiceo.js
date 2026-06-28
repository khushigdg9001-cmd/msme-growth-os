const API_URL = "http://127.0.0.1:8000/api/v1";

export async function getAICEO() {

    const response = await fetch(`${API_URL}/aiceo`);

    if (!response.ok) {
        throw new Error("Failed to fetch AI CEO");
    }

    return await response.json();

}