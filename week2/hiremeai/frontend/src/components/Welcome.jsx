import { Sparkles } from 'lucide-react'

export default function Welcome({ onPick, suggestions }) {
  return (
    <div className="welcome">
      <div className="welcome-avatar">
        <Sparkles size={28} />
      </div>
      <h1 className="welcome-title">HireMeAI</h1>
      <p className="welcome-sub">
        Ask anything about the candidate — skills, experience, projects, education and more.
      </p>
      <div className="suggestions">
        {suggestions.map((s) => (
          <button key={s} className="suggestion-card" onClick={() => onPick(s)}>
            {s}
          </button>
        ))}
      </div>
    </div>
  )
}
