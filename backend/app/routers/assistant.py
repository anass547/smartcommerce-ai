from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class AssistantQuestion(BaseModel):
    question_id: str  # ex: "why_sales_dropped", "stock_risk", "at_risk_customers"


@router.get("/questions")
def get_available_questions():
    """
    Liste des questions prédéfinies proposées à l'utilisateur.
    """
    return {
        "questions": [
            {"id": "why_sales_dropped", "label": "Pourquoi les ventes baissent ?"},
            {"id": "stock_risk", "label": "Quels produits risquent la rupture de stock ?"},
            {"id": "at_risk_customers", "label": "Quels clients présentent un risque de désengagement ?"},
        ]
    }


@router.post("/ask")
def ask_assistant(payload: AssistantQuestion):
    """
    Combine statistiques + règles métier + templates pour générer une réponse.
    TODO: implémenter app.assistant.rules pour router vers la bonne logique.
    """
    return {
        "question_id": payload.question_id,
        "answer": "Réponse générée automatiquement (à implémenter).",
    }
