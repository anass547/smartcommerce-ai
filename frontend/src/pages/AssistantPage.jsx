import { useEffect, useState } from "react";
import { getAssistantQuestions, askAssistant } from "../services/api";

export default function AssistantPage() {
  const [questions, setQuestions] = useState([]);
  const [answer, setAnswer] = useState(null);

  useEffect(() => {
    getAssistantQuestions().then((data) => setQuestions(data.questions)).catch(console.error);
  }, []);

  const handleAsk = async (questionId) => {
    const result = await askAssistant(questionId);
    setAnswer(result.answer);
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Assistant décisionnel</h1>
      <div className="flex flex-col gap-2 mb-6">
        {questions.map((q) => (
          <button
            key={q.id}
            onClick={() => handleAsk(q.id)}
            className="text-left bg-white shadow rounded-lg px-4 py-2 hover:bg-slate-50"
          >
            {q.label}
          </button>
        ))}
      </div>
      {answer && (
        <div className="bg-slate-100 border-l-4 border-slate-900 p-4 rounded">
          <p>{answer}</p>
        </div>
      )}
      {/* TODO: intégrer AnomalyAlert (module 4) en haut de page */}
    </div>
  );
}
