from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import kpis, forecast, segments, anomalies, assistant

app = FastAPI(
    title="SmartCommerce AI API",
    description="API d'analyse, de prédiction et d'aide à la décision pour le e-commerce",
    version="0.1.0",
)

# CORS - à restreindre en production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(kpis.router, prefix="/api/kpis", tags=["Dashboard"])
app.include_router(forecast.router, prefix="/api/forecast", tags=["Forecast"])
app.include_router(segments.router, prefix="/api/segments", tags=["Segmentation"])
app.include_router(anomalies.router, prefix="/api/anomalies", tags=["Anomalies"])
app.include_router(assistant.router, prefix="/api/assistant", tags=["Assistant"])


@app.get("/")
def root():
    return {"status": "ok", "service": "SmartCommerce AI API"}
