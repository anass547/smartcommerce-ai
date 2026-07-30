import { useEffect, useState } from "react";
import { getAssistantQuestions, askAssistant, getAnomalies } from "../services/api";
import AnomalyAlert from "../components/anomalies/AnomalyAlert";
import { Sparkles, ChevronRight, MessageSquareCode } from "lucide-react";

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
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-slate-800 mb-6">Assistant décisionnel</h1>
      
      <AnomalyAlert anomalies={anomalies} />

      <div className="bg-white rounded-lg shadow-sm border border-slate-100 p-6 mb-6">
        <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4 flex items-center gap-2">
          <MessageSquareCode className="h-4.5 w-4.5 text-slate-500" />
          Scénarios d'analyse prédéfinis
        </h3>
        
        <div className="flex flex-col gap-2.5">
          {questions.map((q) => {
            const isAskingThis = askingId === q.id;
            return (
              <button
                key={q.id}
                onClick={() => handleAsk(q.id)}
                disabled={askingId !== null}
                className={`text-left bg-white border border-slate-100 hover:border-slate-200 hover:bg-slate-50/50 shadow-sm rounded-lg px-4 py-3.5 flex items-center justify-between transition-all duration-200 ${
                  askingId !== null ? "opacity-50 cursor-not-allowed" : ""
                }`}
              >
                <span className="font-semibold text-slate-700 text-sm leading-snug">{q.label}</span>
                {isAskingThis ? (
                  <span className="text-xs font-bold text-indigo-600 bg-indigo-50 border border-indigo-100 px-2 py-0.5 rounded-md animate-pulse flex items-center gap-1">
                    <svg className="animate-spin h-3 w-3 text-indigo-600" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                    </svg>
                    Génération...
                  </span>
                ) : (
                  <ChevronRight className="h-4 w-4 text-slate-400" />
                )}
              </button>
            );
          })}
        </div>
      </div>

      {answer && (
        <div className="bg-indigo-50/30 border border-indigo-100/60 border-l-4 border-l-indigo-600 p-5 rounded-r-lg shadow-sm flex items-start gap-4 transition-all hover:shadow-md duration-300 animate-fade-in">
          <div className="flex-shrink-0 p-2 bg-indigo-100 text-indigo-600 rounded-lg border border-indigo-200/20">
            <Sparkles className="h-5 w-5 stroke-[2]" />
          </div>
          <div>
            <h4 className="font-bold text-indigo-950 text-xs mb-1 uppercase tracking-wide">
              Analyse générée
            </h4>
            <p className="text-slate-700 text-sm font-semibold leading-relaxed">
              {answer}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
