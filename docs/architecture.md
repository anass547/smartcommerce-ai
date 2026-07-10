# SmartCommerce AI — Architecture générale, Modules & Structure du repo

---

## 1. Architecture générale

Architecture simplifiée en **3 couches** (adaptée à un MVP 1 mois, sans microservices séparés) :

```
┌─────────────────────────────────────────────────────────┐
│                        FRONTEND                          │
│                    React + Tailwind + Chart.js            │
│                                                             │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌─────────┐│
│  │ Dashboard  │ │ Forecast   │ │ Segments   │ │ Assistant││
│  │   page     │ │   page     │ │   page     │ │   page   ││
│  └────────────┘ └────────────┘ └────────────┘ └─────────┘│
└───────────────────────┬───────────────────────────────────┘
                         │ REST API (JSON / Axios)
┌───────────────────────▼───────────────────────────────────┐
│                        BACKEND                             │
│                     FastAPI (Python)                       │
│                                                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────────┐│
│  │ /kpis    │ │/predict- │ │/customer-│ │ /anomalies    ││
│  │          │ │  sales   │ │ segments │ │ /assistant    ││
│  └──────────┘ └──────────┘ └──────────┘ └───────────────┘│
│                                                              │
│   Couche métier : ML pipeline, requêtes SQL, règles        │
└───────────────────────┬───────────────────────────────────┘
                         │ SQLAlchemy / psycopg2
┌───────────────────────▼───────────────────────────────────┐
│                     BASE DE DONNÉES                        │
│                       PostgreSQL                            │
│   Tables : orders, order_items, customers, products,       │
│            payments, forecasts (cache), anomalies (log)    │
└──────────────────────────────────────────────────────────┘
```

**Flux type** : le frontend appelle un endpoint FastAPI → FastAPI interroge PostgreSQL et/ou exécute un modèle ML déjà entraîné (chargé en mémoire ou depuis un fichier `.pkl`/`.json`) → renvoie du JSON → React affiche via Chart.js.

**Point important** : les modèles ML (Prophet, K-Means) sont **entraînés en amont** (scripts séparés, offline) puis **chargés au runtime** par l'API — on ne réentraîne pas à chaque requête.

---

## 2. Modules et responsabilités

| Module | Rôle | Composants techniques |
|---|---|---|
| **1. Dashboard analytique** | Affiche les KPIs globaux | Endpoint `/kpis` (requêtes SQL agrégées) + composants React |
| **2. Prévision des ventes** | Prédit le CA/commandes futurs | Modèle Prophet entraîné offline + endpoint `/predict-sales` |
| **3. Segmentation clients** | Classe les clients en 4 groupes | Feature engineering RFM + K-Means + endpoint `/customer-segments` |
| **4. Détection d'anomalies** | Alerte sur variations anormales | Calcul statistique (z-score) + endpoint `/anomalies` |
| **5. Assistant décisionnel léger** | Répond à des questions prédéfinies | Moteur de règles (mapping question → requête → template) + endpoint `/assistant` |

---

## 3. Structure des fichiers du repo

```
smartcommerce-ai/
│
├── frontend/                          # React
│   ├── public/
│   ├── src/
│   │   ├── assets/                     # logos, icônes
│   │   ├── components/
│   │   │   ├── dashboard/
│   │   │   │   ├── KpiCard.jsx
│   │   │   │   ├── SalesChart.jsx
│   │   │   │   └── TopProductsTable.jsx
│   │   │   ├── forecast/
│   │   │   │   └── ForecastChart.jsx
│   │   │   ├── segments/
│   │   │   │   └── SegmentPieChart.jsx
│   │   │   ├── anomalies/
│   │   │   │   └── AnomalyAlert.jsx
│   │   │   ├── assistant/
│   │   │   │   ├── QuestionButtons.jsx
│   │   │   │   └── AnswerCard.jsx
│   │   │   └── layout/
│   │   │       ├── Navbar.jsx
│   │   │       └── Sidebar.jsx
│   │   ├── pages/
│   │   │   ├── DashboardPage.jsx
│   │   │   ├── ForecastPage.jsx
│   │   │   ├── SegmentsPage.jsx
│   │   │   └── AssistantPage.jsx
│   │   ├── services/
│   │   │   └── api.js                  # instance Axios + appels API
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── tailwind.config.js
│   ├── package.json
│   └── .env                            # URL de l'API
│
├── backend/                           # FastAPI
│   ├── app/
│   │   ├── main.py                     # point d'entrée, montage des routers
│   │   ├── config.py                   # variables d'env, connexion DB
│   │   ├── database.py                 # session SQLAlchemy
│   │   ├── models/                     # modèles ORM (tables)
│   │   │   ├── order.py
│   │   │   ├── customer.py
│   │   │   └── product.py
│   │   ├── schemas/                    # schémas Pydantic (validation/réponses)
│   │   │   ├── kpi_schema.py
│   │   │   ├── forecast_schema.py
│   │   │   └── segment_schema.py
│   │   ├── routers/                    # endpoints par module
│   │   │   ├── kpis.py
│   │   │   ├── forecast.py
│   │   │   ├── segments.py
│   │   │   ├── anomalies.py
│   │   │   └── assistant.py
│   │   ├── ml/                         # logique ML
│   │   │   ├── train_forecast.py       # script offline d'entraînement Prophet
│   │   │   ├── train_segmentation.py   # script offline RFM + K-Means
│   │   │   ├── anomaly_detector.py     # fonction z-score
│   │   │   └── saved_models/           # .pkl / .json des modèles entraînés
│   │   └── assistant/
│   │       ├── rules.py                # mapping question → fonction
│   │       └── templates.py            # phrases-types de réponse
│   ├── requirements.txt
│   └── .env
│
├── data/
│   ├── raw/                            # dataset Olist brut (CSV)
│   ├── processed/                      # données nettoyées
│   └── notebooks/                      # EDA, prototypage
│       ├── 01_exploration.ipynb
│       ├── 02_cleaning.ipynb
│       ├── 03_forecast_prototype.ipynb
│       └── 04_segmentation_prototype.ipynb
│
├── database/
│   └── init.sql                        # création des tables PostgreSQL
│
├── docs/
│   ├── vision_produit.md               # les 11 modules (roadmap)
│   └── architecture.md                 # ce document
│
├── docker-compose.yml                  # bonus fin de projet (optionnel)
├── .gitignore
└── README.md
```

---

## 4. Notes pratiques

- **Un seul backend** (FastAPI) qui fait à la fois API métier et inférence ML → pas de séparation Spring Boot/microservice pour ce MVP, cela évite la complexité réseau
- **Les modèles ML sont versionnés hors Git** (dossier `saved_models/` à mettre dans `.gitignore` si les fichiers sont lourds), sauf si vous utilisez Git LFS
- **`docs/`** sert à stocker la vision produit et la roadmap présentées dans le rapport, séparément du code
- Le dossier **`notebooks/`** sert de bac à sable avant de transformer le code en scripts propres dans `ml/`
