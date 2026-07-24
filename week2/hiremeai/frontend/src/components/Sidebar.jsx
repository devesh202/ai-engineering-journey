import { useMemo } from 'react'
import { Plus, SquarePen, Trash2, X, Sparkles } from 'lucide-react'

function startOfDay(ts) {
  const d = new Date(ts)
  d.setHours(0, 0, 0, 0)
  return d.getTime()
}

function groupLabel(ts, now) {
  const today = startOfDay(now)
  const day = startOfDay(ts)
  const diffDays = Math.round((today - day) / 86400000)
  if (diffDays <= 0) return 'Today'
  if (diffDays <= 7) return 'Previous 7 days'
  if (diffDays <= 30) return 'Previous 30 days'
  return 'Older'
}

function ChatRow({ chat, active, onClick, onDelete }) {
  return (
    <div className={`chat-row${active ? ' active' : ''}`}>
      <button className="chat-row-btn" onClick={onClick} title={chat.title}>
        <span className="chat-row-title">{chat.title}</span>
      </button>
      <button
        className="chat-row-del"
        onClick={(e) => {
          e.stopPropagation()
          onDelete()
        }}
        title="Delete chat"
        aria-label="Delete chat"
      >
        <Trash2 size={14} />
      </button>
    </div>
  )
}

export default function Sidebar({
  chats,
  activeChatId,
  onNewChat,
  onOpenChat,
  onDeleteChat,
  open,
  onClose,
}) {
  const groups = useMemo(() => {
    const now = Date.now()
    const items = Object.values(chats).sort((a, b) => b.createdAt - a.createdAt)
    const grouped = []
    for (const chat of items) {
      const label = groupLabel(chat.createdAt, now)
      const last = grouped[grouped.length - 1]
      if (last && last.label === label) {
        last.chats.push(chat)
      } else {
        grouped.push({ label, chats: [chat] })
      }
    }
    return grouped
  }, [chats])

  return (
    <>
      {open && <div className="sidebar-backdrop" onClick={onClose} />}
      <aside className={`sidebar${open ? ' open' : ''}`}>
        <div className="sidebar-header">
          <button className="btn-new-chat" onClick={onNewChat}>
            <Plus size={18} />
            New chat
          </button>
          <button className="icon-btn sidebar-close" onClick={onClose} aria-label="Close sidebar">
            <X size={18} />
          </button>
        </div>

        <nav className="sidebar-nav">
          {groups.length === 0 ? (
            <div className="sidebar-empty">
              <SquarePen size={18} />
              <p>Your chats will appear here.</p>
            </div>
          ) : (
            groups.map((group) => (
              <div key={group.label} className="sidebar-group">
                <div className="sidebar-group-label">{group.label}</div>
                {group.chats.map((chat) => (
                  <ChatRow
                    key={chat.id}
                    chat={chat}
                    active={chat.id === activeChatId}
                    onClick={() => onOpenChat(chat.id)}
                    onDelete={() => onDeleteChat(chat.id)}
                  />
                ))}
              </div>
            ))
          )}
        </nav>

        <div className="sidebar-footer">
          <div className="persona">
            <div className="persona-avatar">
              <Sparkles size={16} />
            </div>
            <div className="persona-info">
              <div className="persona-name">HireMeAI</div>
              <div className="persona-sub">Candidate Assistant</div>
            </div>
          </div>
        </div>
      </aside>
    </>
  )
}
