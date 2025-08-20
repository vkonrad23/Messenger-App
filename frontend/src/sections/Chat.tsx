import React, { useEffect, useMemo, useRef, useState } from 'react'
import { api, API_BASE } from '../api'

type User = { id: number; username: string }

type Message = {
  id: number
  sender_id: number
  recipient_id: number
  content?: string | null
  created_at: string
  updated_at?: string | null
  deleted: boolean
  attachments: { id: number; file_name: string; file_url: string; uploaded_at: string }[]
}

export const Chat: React.FC<{ token: string, onLogout: () => void }> = ({ token, onLogout }) => {
  const [otherId, setOtherId] = useState<number | ''>('')
  const [messages, setMessages] = useState<Message[]>([])
  const [content, setContent] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [me, setMe] = useState<{ id: number; username: string; email: string } | null>(null)
  const filesRef = useRef<HTMLInputElement | null>(null)
  const recipientRef = useRef<HTMLInputElement | null>(null)

  const auth = useMemo(() => ({ headers: { Authorization: `Bearer ${token}` } }), [token])

  const fetchThread = async () => {
    if (!otherId) return
    const { data } = await api.get<Message[]>(`/messages/thread/${otherId}`, auth)
    // Hide deleted messages from the UI
    setMessages(data.filter(m => !m.deleted))
  }

  useEffect(() => { fetchThread() }, [otherId])

  // Auto-refresh thread every 3s when a recipient is selected
  useEffect(() => {
    if (!otherId) return
    const timer = setInterval(() => {
      fetchThread()
    }, 3000)
    return () => clearInterval(timer)
  }, [otherId, auth])

  // Fetch current user info for clarity (so user sees their own ID)
  useEffect(() => {
    (async () => {
      try {
        const { data } = await api.get<{ id: number; username: string; email: string }>(`/me`, auth)
        setMe(data)
      } catch {
        // ignore
      }
    })()
  }, [auth])

  const send = async (e: React.FormEvent) => {
    e.preventDefault()
    // Basic client-side validation with clear feedback
    if (!otherId) {
      setError('Please enter the recipient User ID and try again.')
      recipientRef.current?.focus()
      return
    }

    const noText = content.trim().length === 0
    const noFiles = !filesRef.current?.files?.length
    if (noText && noFiles) {
      setError('Type a message or attach at least one file.')
      return
    }

    setError(null)
    const form = new FormData()
    form.append('recipient_id', String(otherId))
    if (content) form.append('content', content)
    if (filesRef.current?.files?.length) {
      for (const f of filesRef.current.files) {
        form.append('files', f, f.name)
      }
    }
    // Allow text-only or file-only messages; backend also validates non-empty
    try {
      await api.post(`/messages`, form, { ...auth, headers: { ...auth.headers } })
    } catch (err: any) {
      const detail = err?.response?.data?.detail
      setError(typeof detail === 'string' ? detail : 'Failed to send the message')
      return
    }
    setContent('')
    if (filesRef.current) filesRef.current.value = ''
    fetchThread()
  }

  const remove = async (id: number) => {
    // Optimistically remove from UI immediately
    setMessages((prev) => prev.filter((msg) => msg.id !== id))
    
    try {
      const res = await fetch(`${API_BASE}/messages/${id}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token') || ''}`,
        },
      })

      if (!res.ok) {
        // If delete failed, restore the message and show error
        await fetchThread()
        let detail: string | undefined
        const text = await res.text()
        try {
          const data = JSON.parse(text) as { detail?: string }
          detail = data?.detail
        } catch {
          detail = text
        }
        setError(detail || 'Error deleting message')
      }
    } catch (error) {
      // On network error, restore messages and show error
      await fetchThread()
      console.error('Error deleting message', error)
      setError('Error deleting message')
    }
  }

  const edit = async (id: number) => {
    const newContent = prompt('New text:')
    if (newContent == null) return
  await api.patch(`/messages/${id}`, { content: newContent }, auth)
    fetchThread()
  }

  return (
    <div className="h-full grid grid-rows-[auto_1fr_auto] max-w-3xl mx-auto">
      <header className="p-3 bg-white shadow flex gap-2 items-center">
        <input ref={recipientRef} className="border px-2 py-1 rounded w-40" placeholder="Recipient User ID" value={otherId}
               onChange={e => setOtherId(Number(e.target.value) || '')} />
        <button className="px-3 py-1 bg-blue-600 text-white rounded" onClick={fetchThread}>Open</button>
        <div className="flex-1" />
        <div className="text-sm text-gray-600">
          You: {me ? `${me.username} (ID ${me.id})` : 'loading…'}
        </div>
        <button className="text-red-600" onClick={onLogout}>Logout</button>
      </header>

      <main className="p-3 space-y-2 overflow-auto">
        {error && (
          <div className="mb-2 text-sm text-red-600">{error}</div>
        )}
        {messages.map(m => (
          <div key={m.id} className={`p-3 rounded border ${m.deleted ? 'opacity-60' : ''}`}>
            <div className="text-sm text-gray-500">#{m.id} from {m.sender_id} to {m.recipient_id}</div>
            {m.content && <div className="py-1">{m.content}</div>}
            {m.attachments.length > 0 && (
              <div className="flex gap-2 flex-wrap">
                {m.attachments.map(a => (
                  <a key={a.id} href={`${API_BASE}${a.file_url}`} target="_blank" className="text-blue-600 underline">
                    {a.file_name}
                  </a>
                ))}
              </div>
            )}
            {me?.id === m.sender_id && !m.deleted && (
              <div className="pt-1 flex gap-2 text-sm">
                <button className="text-blue-600" onClick={() => edit(m.id)}>Edit</button>
                <button className="text-red-600" onClick={() => remove(m.id)}>Delete</button>
              </div>
            )}
          </div>
        ))}
      </main>

      <form onSubmit={send} className="p-3 bg-white shadow flex gap-2">
        <input className="flex-1 border px-3 py-2 rounded" placeholder="Type a message" value={content} onChange={e => setContent(e.target.value)} />
        <input type="file" multiple ref={filesRef} />
        <button
          className="px-3 py-2 bg-green-600 text-white rounded disabled:opacity-50"
          disabled={!filesRef.current?.files?.length && content.trim().length === 0}
          title={!otherId ? 'Enter recipient User ID first' : undefined}
        >
          Send
        </button>
      </form>
    </div>
  )
}
