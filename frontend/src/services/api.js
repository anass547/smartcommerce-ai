import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api",
});

export const getKpisSummary = () => api.get("/kpis/summary").then((res) => res.data);
export const getSalesEvolution = () => api.get("/kpis/sales-evolution").then((res) => res.data);
export const getForecast = (horizon = "week") =>
  api.get(`/forecast/sales?horizon=${horizon}`).then((res) => res.data);
export const getSegments = () => api.get("/segments/").then((res) => res.data);
export const getAnomalies = () => api.get("/anomalies/").then((res) => res.data);
export const getAssistantQuestions = () =>
  api.get("/assistant/questions").then((res) => res.data);
export const askAssistant = (questionId) =>
  api.post("/assistant/ask", { question_id: questionId }).then((res) => res.data);

export default api;
