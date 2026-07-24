import { useEffect, useRef } from 'react'
import { Menu, Sparkles } from 'lucide-react'
import Message from './Message.jsx'
import Composer from './Composer.jsx'
import Welcome from './Welcome.jsx'

const SUGGESTIONS = [
  'Tell me about this candidate',
  'What are their top skills?',
  'Summarize their professional experience',
  'Why should I hire them?',
]

export default function ChatView({ chat, onSend, isLoading, onOpenSidebar }) {
  const scrollRef = useRef(null)
  const messages = chat?.messages ?? []
  const lastContent = messages[messages.length - 1]?.content ?? ''

  useEffect(() => {
    const el = scrollRef.current
    if (el) el.scrollTop = el.scrollHeight
  }, [messages.length, lastContent, isLoading])

  return (
    <main className="chat">
      <header className="chat-header">
        <button className="icon-btn" onClick={onOpenSidebar} aria-label="Open sidebar">
          <Menu size={20} />
        </button>
        <div className="chat-header-title">
          {chat ? (
            <>
              <Sparkles size={16} className="chat-header-spark" />
              {chat.title}
            </>
          ) : (
            'HireMeAI'
          )}
        </div>
        <div className="chat-header-spacer" />
      </header>

      <div className="chat-scroll" ref={scrollRef}>
        {messages.length === 0 ? (
          <Welcome onPick={onSend} suggestions={SUGGESTIONS} />
        ) : (
          <div className="message-list">
            {messages.map((m) => (
              <Message
                key={m.id}
                message={m}
                loading={isLoading && m.role === 'assistant' && !m.content}
              />
            ))}
          </div>
        )}
      </div>

      <div className="composer-wrap">
        <Composer onSend={onSend} disabled={isLoading} />
        <p className="disclaimer">
          HireMeAI can make mistakes. Verify important information directly with the candidate.
        </p>
      </div>
    </main>
  )
}
