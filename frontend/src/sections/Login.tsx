import React, { useState } from 'react'
import { api, API_BASE } from '../api'

export const Login: React.FC<{ onToken: (token: string) => void }> = ({ onToken }) => {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [mode, setMode] = useState<'login'|'register'>('login')
  const [email, setEmail] = useState('')
  const [error, setError] = useState<string | null>(null)

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    try {
      if (mode === 'register') {
        await api.post(`/auth/register`, { username, email, password })
      }
      const form = new URLSearchParams()
      form.append('username', username)
      form.append('password', password)
      const { data } = await api.post(`/auth/token`, form, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } })
      onToken(data.access_token)
    } catch (err: any) {
      const msg = err?.response?.data?.detail || err?.message || 'Request failed'
      setError(typeof msg === 'string' ? msg : JSON.stringify(msg))
    }
  }

  return (
    <div className="h-full flex items-center justify-center">
      <form onSubmit={submit} className="bg-white p-6 rounded shadow w-96 space-y-3">
  <h1 className="text-xl font-semibold">{mode === 'login' ? 'Sign in' : 'Register'}</h1>
  <div className="text-xs text-gray-500">API: {API_BASE}</div>
        {mode === 'register' && (
          <input className="w-full border px-3 py-2 rounded" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
        )}
        <input className="w-full border px-3 py-2 rounded" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
        <input className="w-full border px-3 py-2 rounded" type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
        {error && <div className="text-red-600 text-sm">{error}</div>}
        <button className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">{mode === 'login' ? 'Login' : 'Create account'}</button>
        <button type="button" className="w-full text-sm text-blue-600" onClick={() => setMode(mode === 'login' ? 'register' : 'login')}>
          {mode === 'login' ? 'No account? Register' : 'Have an account? Login'}
        </button>
      </form>
    </div>
  )
}
