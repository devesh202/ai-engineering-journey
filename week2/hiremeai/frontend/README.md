# HireMeAI Frontend

ChatGPT-style UI for the HireMeAI candidate assistant. A recruiter visits the
site and asks questions about the candidate; the AI answers from the resume via
the FastAPI backend.

Built with React + Vite, `react-markdown` and `lucide-react`.

## Run

1. Start the backend first (from `week2/hiremeai`):

   ```powershell
   .venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
   ```

2. Start the frontend (from `frontend`):

   ```powershell
   npm install
   npm run dev
   ```

   Open http://localhost:5173

The dev server proxies `/api/*` to the backend on `localhost:8000`, so the
frontend needs no CORS setup in development. The backend must run from the
`hiremeai` folder so it can find `backend/resume.pdf`.

The backend also allows cross-origin requests (CORS `*`), so you can point a
build directly at it. Set the backend URL at build time:

```powershell
$env:VITE_API_BASE="http://localhost:8000"
npm run build
```

If `VITE_API_BASE` is unset, the frontend uses the relative `/api/chat` path
(dev proxy).

## Scripts

- `npm run dev` — dev server with HMR
- `npm run build` — production build to `dist/`
- `npm run preview` — preview the production build
- `npm run lint` — oxlint

## Structure

```
src/
  App.jsx            — state, chat/persist logic, layout
  lib/api.js         — fetch wrapper for POST /api/chat
  components/
    Sidebar.jsx      — conversation history sidebar
    ChatView.jsx     — header, message list, composer wrapper
    Welcome.jsx      — landing screen with suggested questions
    Message.jsx      — markdown message / typing indicator
    Composer.jsx     — input box + send button
  index.css          — ChatGPT-style dark theme
```

Conversation history is persisted to `localStorage`.
