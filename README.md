# SmartCommerce AI

Plateforme intelligente d'analyse, de prédiction et d'aide à la décision pour le e-commerce.

## MVP (5 modules)
1. Dashboard analytique
2. Prévision des ventes (Prophet)
3. Segmentation clients (RFM + K-Means)
4. Détection d'anomalies
5. Assistant décisionnel léger

Voir [`docs/vision_produit.md`](docs/vision_produit.md) pour la vision produit complète et [`docs/architecture.md`](docs/architecture.md) pour l'architecture détaillée.

## Stack
- **Frontend** : React, Tailwind CSS, Chart.js
- **Backend / IA** : FastAPI (Python)
- **Base de données** : PostgreSQL
- **Machine Learning** : Prophet, Scikit-learn

## Structure du repo
```
smartcommerce-ai/
├── frontend/        # Application React
├── backend/          # API FastAPI + logique ML
├── data/              # Dataset (raw/processed) + notebooks
├── database/          # Script SQL d'initialisation
└── docs/              # Vision produit, architecture
```

## Démarrage rapide

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sous Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Base de données
```bash
psql -U postgres -d smartcommerce -f database/init.sql
```

## Dataset
[Olist Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) — à placer dans `data/raw/`.

## Auteurs
Projet de fin d'études (PFA) — 2026
