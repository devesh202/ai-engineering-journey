const API_BASE = import.meta.env.VITE_API_BASE ?? ''
const ENDPOINT = API_BASE ? `${API_BASE}/chat` : '/api/chat'

export async function streamQuestion(question, onChunk, signal) {
  const res = await fetch(ENDPOINT, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question }),
    signal,
  })

  if (!res.ok) {
    let detail = `Request failed with status ${res.status}`
    try {
      const err = await res.json()
      if (err.detail) detail = err.detail
    } catch {
      /* ignore */
    }
    throw new Error(detail)
  }

  const reader = res.body.getReader()
  const decoder = new TextDecoder()
  let full = ''
  for (;;) {
    const { done, value } = await reader.read()
    if (done) break
    full += decoder.decode(value, { stream: true })
    onChunk(full)
  }
  full += decoder.decode()
  return full
}
