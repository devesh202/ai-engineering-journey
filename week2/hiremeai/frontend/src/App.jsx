import { useCallback, useEffect, useMemo, useState } from 'react'
import Sidebar from './components/Sidebar.jsx'
import ChatView from './components/ChatView.jsx'
import { streamQuestion } from './lib/api.js'

const STORAGE_KEY = 'hiremeai.chats.v1'

function makeId() {
  return typeof crypto !== 'undefined' && crypto.randomUUID
    ? crypto.randomUUID()
    : `id-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`
}

function makeTitle(text) {
  const clean = text.replace(/\s+/g, ' ').trim()
  return clean.length > 34 ? `${clean.slice(0, 34)}…` : clean
}

function loadChats() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) return JSON.parse(raw)
  } catch {
    /* ignore */
  }
  return {}
}

function persistChats(chats) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(chats))
  } catch {
    /* ignore */
  }
}

export default function App() {
  const [chats, setChats] = useState(loadChats)
  const [activeChatId, setActiveChatId] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(false)

  useEffect(() => {
    persistChats(chats)
  }, [chats])

  const activeChat = useMemo(
    () => (activeChatId ? chats[activeChatId] : null),
    [chats, activeChatId],
  )

  const newChat = useCallback(() => {
    setActiveChatId(null)
    setSidebarOpen(false)
  }, [])

  const openChat = useCallback((id) => {
    setActiveChatId(id)
    setSidebarOpen(false)
  }, [])

  const deleteChat = useCallback(
    (id) => {
      setChats((prev) => {
        const next = { ...prev }
        delete next[id]
        return next
      })
      setActiveChatId((prev) => (prev === id ? null : prev))
    },
    [],
  )

  const sendMessage = useCallback(
    async (text) => {
      const trimmed = text.trim()
      if (!trimmed || isLoading) return

      const userMessage = { id: makeId(), role: 'user', content: trimmed }
      const assistantMessage = { id: makeId(), role: 'assistant', content: '' }

      let chatId = activeChatId
      if (chatId) {
        setChats((prev) => ({
          ...prev,
          [chatId]: {
            ...prev[chatId],
            messages: [...prev[chatId].messages, userMessage, assistantMessage],
          },
        }))
      } else {
        chatId = makeId()
        setChats((prev) => ({
          [chatId]: {
            id: chatId,
            title: makeTitle(trimmed),
            createdAt: Date.now(),
            messages: [userMessage, assistantMessage],
          },
          ...prev,
        }))
        setActiveChatId(chatId)
      }

      const patchAssistant = (patch) =>
        setChats((prev) => ({
          ...prev,
          [chatId]: {
            ...prev[chatId],
            messages: prev[chatId].messages.map((m) =>
              m.id === assistantMessage.id ? { ...m, ...patch } : m,
            ),
          },
        }))

      setIsLoading(true)
      try {
        await streamQuestion(trimmed, (fullText) => patchAssistant({ content: fullText }))
      } catch (err) {
        patchAssistant({
          content: `⚠️ ${err.message || 'Something went wrong. Is the backend running?'}`,
          isError: true,
        })
      } finally {
        setIsLoading(false)
      }
    },
    [activeChatId, isLoading],
  )

  return (
    <div className="app">
      <Sidebar
        chats={chats}
        activeChatId={activeChatId}
        onNewChat={newChat}
        onOpenChat={openChat}
        onDeleteChat={deleteChat}
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />
      <ChatView
        chat={activeChat}
        onSend={sendMessage}
        isLoading={isLoading}
        onOpenSidebar={() => setSidebarOpen(true)}
      />
    </div>
  )
}
