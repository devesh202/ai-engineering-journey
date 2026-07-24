import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import { Sparkles, Copy, Check } from 'lucide-react'

function LoadingDots() {
  return (
    <span className="typing-dots" aria-label="Thinking">
      <span />
      <span />
      <span />
    </span>
  )
}

export default function Message({ message, loading }) {
  const [copied, setCopied] = useState(false)

  if (loading) {
    return (
      <div className="message-row assistant">
        <div className="message-avatar assistant-avatar">
          <Sparkles size={15} />
        </div>
        <div className="message-body">
          <LoadingDots />
        </div>
      </div>
    )
  }

  const isUser = message.role === 'user'
  const isError = message.isError

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(message.content)
      setCopied(true)
      setTimeout(() => setCopied(false), 1500)
    } catch {
      /* ignore */
    }
  }

  if (isUser) {
    return (
      <div className="message-row user">
        <div className="message-body user-body">{message.content}</div>
      </div>
    )
  }

  return (
    <div className={`message-row assistant${isError ? ' error' : ''}`}>
      <div className="message-avatar assistant-avatar">
        <Sparkles size={15} />
      </div>
      <div className="message-body">
        <ReactMarkdown>{message.content}</ReactMarkdown>
        {!isError && (
          <button className="copy-btn" onClick={copy} title="Copy response" aria-label="Copy response">
            {copied ? <Check size={15} /> : <Copy size={15} />}
          </button>
        )}
      </div>
    </div>
  )
}
