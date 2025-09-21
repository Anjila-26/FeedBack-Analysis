# Feedback Analysis System

A modular, full-stack feedback collection and analysis platform.  
Built with **FastAPI** (backend, AI agent, analytics) and **Next.js** (frontend, admin dashboard, feedback form).

---

## Features

- **User Feedback Collection:** Modern web form for collecting ratings, comments, and feature requests.
- **AI-Powered Feedback Analysis:** Uses Pydantic AI agents for sentiment, keyword, and actionable insight extraction.
- **Admin Dashboard:** Visualize feedback, trends, and priority issues.
- **Modular Backend:** Clean API routing, rate limiting, and database integration.
- **Modern Frontend:** Built with Next.js, easily customizable and extendable.


- **Screenshots:**  
  ![Admin Dashboard](Screenshots/Admin%20DashBoard.png)  
  ![Feedback Form](Screenshots/FeedBack%20Form.png)  
  ![Individual Analysis](Screenshots/Individual%20Analysis.png)  
  ![Priority and Security](Screenshots/Prirority%20and%20Security.png)

---

## Project Structure

```
Task1/
├── backend/
│   ├── agent/           # Feedback AI agent logic
│   ├── models/          # Pydantic models
│   ├── route/           # API routers (modular)
│   ├── database.py      # DB logic (SQLite)
│   ├── main.py          # FastAPI app entrypoint
│   └── requirements.txt
├── frontend/
│   ├── app/             # Next.js app pages/components
│   ├── public/          # Static assets
│   ├── package.json
│   └── README.md
└── Screenshots/         # UI screenshots
```

---

## Getting Started

### Backend (FastAPI)

1. **Install dependencies:**
    ```sh
    cd backend
    pip install -r requirements.txt
    ```

2. **Run the backend server:**
    ```sh
    uvicorn main:app --reload
    ```

3. **API Docs:**  
   Visit [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Frontend (Next.js)

1. **Install dependencies:**
    ```sh
    cd frontend
    npm install
    ```

2. **Run the frontend dev server:**
    ```sh
    npm run dev
    ```

3. **Open in browser:**  
   [http://localhost:3000](http://localhost:3000)

---

## API Overview

- `POST /feedback` — Submit feedback
- `GET /feedback/all` — Get all feedback
- `GET /feedback/basic-insights` — Basic analytics
- `GET /feedback/ai-insights` — AI-powered insights
- `GET /feedback/priority-issues` — Priority issues
- `GET /feedback/feature-requests` — Feature requests
- `POST /feedback/analyze/{feedback_id}` — Analyze individual feedback

See `/docs` for full interactive API.

---

## Customization

- **AI Model:**  
  Configure your Gemini/OpenAI API key in environment variables for advanced analysis.
- **Database:**  
  Default is SQLite. Adapt `database.py` for other DBs if needed.
- **Frontend:**  
  Edit `frontend/app/` for UI/UX changes.

---

## License

MIT License

---

---

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [Next.js](https://nextjs.org/)
- [Pydantic AI](https://github.com/pydantic/pydantic-ai)
- [TextBlob](https://textblob.readthedocs.io/en/dev/)