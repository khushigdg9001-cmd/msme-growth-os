const API_URL = "http://127.0.0.1:8000/api/v1";

export async function getFinance() {

    const response = await fetch(`${API_URL}/finance`);

    if (!response.ok) {
        throw new Error("Failed to fetch Finance Data");
    }

    return await response.json();

}