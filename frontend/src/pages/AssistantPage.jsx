import { useEffect, useState } from "react";
import { getAssistantQuestions, askAssistant, getAnomalies } from "../services/api";
import AnomalyAlert from "../components/anomalies/AnomalyAlert";

export default function AssistantPage() {
  const [questions, setQuestions] = useState([]);
  const [anomalies, setAnomalies] = useState([]);
  const [answer, setAnswer] = useState(null);
  const [askingId, setAskingId] = useState(null);

  useEffect(() => {
    getAssistantQuestions().then((data) => setQuestions(data.questions)).catch(console.error);
    getAnomalies().then((data) => setAnomalies(data.anomalies)).catch(console.error);
  }, []);

  const handleAsk = async (questionId) => {
    setAskingId(questionId);
    try {
      const result = await askAssistant(questionId);
      setAnswer(result.answer);
    } catch (err) {
      console.error(err);
    } finally {
      setAskingId(null);
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Assistant décisionnel</h1>
      
      <AnomalyAlert anomalies={anomalies} />

      <div className="flex flex-col gap-2 mb-6">
        {questions.map((q) => {
          const isAskingThis = askingId === q.id;
          return (
            <button
              key={q.id}
              onClick={() => handleAsk(q.id)}
              disabled={askingId !== null}
              className={`text-left bg-white shadow rounded-lg px-4 py-3 border border-slate-100 flex items-center justify-between hover:bg-slate-50 transition-colors ${
                askingId !== null ? "opacity-50 cursor-not-allowed" : ""
              }`}
            >
              <span className="font-medium text-slate-700">{q.label}</span>
              {isAskingThis ? (
                <span className="text-sm font-semibold text-slate-500 animate-pulse">
                  Génération de la réponse...
                </span>
              ) : (
                <svg className="h-5 w-5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" />
                </svg>
              )}
            </button>
          );
        })}
      </div>

      {answer && (
        <div className="bg-slate-50 border-l-4 border-slate-800 p-4 rounded shadow-sm border border-slate-100">
          <p className="text-slate-700 text-sm font-medium leading-relaxed">{answer}</p>
        </div>
      )}
    </div>
  );
}

