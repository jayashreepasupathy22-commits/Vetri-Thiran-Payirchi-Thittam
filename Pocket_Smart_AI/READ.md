PocketSmart AI is a GenAI-powered budget and recommendation assistant.

It supports:

- Home Interior Planning
- Party Budget Planning
- Jewelry Recommendations
- Optional Jewelry Outfit Image Analysis
- Gemini AI recommendations
- User registration
- User login
- JWT authentication
- Recommendation history
- Dashboard
- SQLite database
- Local fallback recommendations

---

# Technology Stack

Frontend:

- HTML
- CSS
- JavaScript
- Jinja2

Backend:

- Python
- FastAPI
- Uvicorn

Database:

- SQLite

AI:

- Google Gemini API
- google-genai SDK

Authentication:

- JWT
- HttpOnly cookies

---

# Project Structure

```text
pocketsmart_ai/
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
│
├── data/
│
├── tests/
│ └── test_app.py
│
└── app/
    ├── auth.py
    ├── config.py
    ├── database.py
    ├── main.py
    │
    ├── models/
    │ ├── __init__.py
    │ └── schemas.py
    │
    ├── routers/
    │ ├── __init__.py
    │ ├── auth.py
    │ ├── pages.py
    │ └── planners.py
    │
    ├── services/
    │ ├── __init__.py
    │ ├── catalog.py
    │ ├── gemini_utils.py
    │ └── recommendation_service.py
    │
    ├── static/
    │ ├── css/
    │ │ └── style.css
    │ └── js/
    │ └── app.js
    │
    └── templates/
        ├── base.html
        ├── index.html
        ├── login.html
        ├── register.html
        ├── dashboard.html
        ├── history.html
        ├── home_planner.html
        ├── party_planner.html
        ├── jewelry_planner.html
        └── testimonials.html

-