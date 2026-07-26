from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import inspect

from app.database import get_db
from app.assistant.rules import RULES

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
def ask_assistant(payload: AssistantQuestion, db: Session = Depends(get_db)):
    """
    Combine statistiques + règles métier + templates pour générer une réponse.
    """
    question_id = payload.question_id
    if question_id not in RULES:
        return {
            "question_id": question_id,
            "answer": "Question non reconnue par l'assistant.",
        }

    try:
        rule_func = RULES[question_id]
        
        # Check if the rule function expects a 'db' parameter
        sig = inspect.signature(rule_func)
        if "db" in sig.parameters:
            answer = rule_func(db)
        else:
            answer = rule_func()
    except Exception:
        # Fallback message on failure as requested
        answer = "Je n'ai pas pu générer de réponse pour cette question."

    return {
        "question_id": question_id,
        "answer": answer,
    }
