import axios from "axios";

const API = "http://127.0.0.1:8000/api/v1";

export async function getWhatsApp() {
    const response = await axios.get(`${API}/whatsapp`);
    return response.data;
}