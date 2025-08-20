import React, { useEffect, useState } from 'react'
import { Login } from '../sections/Login'
import { Chat } from '../sections/Chat'

export const App: React.FC = () => {
  const [token, setToken] = useState<string | null>(null)

  useEffect(() => {
    const t = localStorage.getItem('token')
    if (t) setToken(t)
  }, [])

  return (
    <div className="h-full bg-gray-100">
      {!token ? (
        <Login onToken={(t) => { localStorage.setItem('token', t); setToken(t) }} />
      ) : (
        <Chat token={token} onLogout={() => { localStorage.removeItem('token'); setToken(null) }} />
      )}
    </div>
  )
}
