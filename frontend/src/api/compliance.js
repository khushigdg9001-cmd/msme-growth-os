const API_URL = "http://127.0.0.1:8000/api/v1";

export async function getCompliance() {

    const response = await fetch(`${API_URL}/compliance`);

    if (!response.ok) {

        throw new Error("Failed to fetch Compliance Data");

    }

    return await response.json();

}