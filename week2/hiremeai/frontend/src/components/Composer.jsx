import { useState } from 'react'
import { ArrowUp, Square } from 'lucide-react'

export default function Composer({ onSend, disabled }) {
  const [value, setValue] = useState('')

  const submit = () => {
    if (disabled || !value.trim()) return
    onSend(value)
    setValue('')
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      submit()
    }
  }

  return (
    <div className={`composer${disabled ? ' disabled' : ''}`}>
      <textarea
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ask about this candidate…"
        rows={1}
        autoFocus
      />
      <button
        className={`send-btn${disabled || !value.trim() ? '' : ' active'}`}
        onClick={disabled ? undefined : submit}
        disabled={disabled}
        aria-label="Send message"
      >
        {disabled ? <Square size={16} fill="currentColor" /> : <ArrowUp size={16} strokeWidth={2.5} />}
      </button>
    </div>
  )
}
