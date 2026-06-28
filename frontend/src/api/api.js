import axios from "axios";

const api = axios.create({
  baseURL: "https://msme-growth-os.onrender.com/api/v1",
});

export default api;
